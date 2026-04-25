from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .user_models import User
from .cache import redis_client
from .auth import hash_password, verify_password, create_access_token, decode_access_token
from .schemas import UserLogin, UserCreate
import json

app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods
#     allow_headers=["*"],  # Allow all headers
# )

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.get("/")
def health():
    return {"status": "API Gateway is running"}

# -------------------------------
# Signup
# -------------------------------
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return "Signup successfully"

# -------------------------------
# Login
# -------------------------------
@app.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return "Login successfully"

# -------------------------------
# Protected profile endpoint
# -------------------------------

@app.get("/profile")
def profile(authorization: str = Header(None), db: Session = Depends(get_db)):
    # 1️ Check for Authorization header
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.split(" ")[1]

    # Decode JWT
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload["sub"])

    # 3️ Check Redis cache
    cached = redis_client.get(f"user:{user_id}")
    if cached:
        return {"source": "cache", "data": json.loads(cached)}

    # 4️ Query database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    data = {"id": user.id, "name": user.name, "email": user.email}

    # 5️ Store in Redis (with expiration)
    redis_client.setex(f"user:{user_id}", 3600, json.dumps(data))  # cache for 1 hour

    return {"source": "database", "data": data}