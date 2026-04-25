#---------------------------------
#    1- Builder
#---------------------------------

FROM python:3.11-slim AS Builder

WORKDIR /app

COPY requirements.txt .

# 1- Install build dependencies 
# 2- Install requirements for project
RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# -----------------------------
# Stage 2: Final Image
# -----------------------------

FROM python:3.11-slim

WORKDIR /app

# Copy installed packages in builder
COPY --from=Builder /install /usr/local

# Copy program files to image
COPY ./app ./app

# Change the root user
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Set PYTHONPATH to include /app
ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]






