let token = "";

async function signup() {
    const name = document.getElementById("signup-name").value;
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;

    const res = await fetch("/api/signup", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, email, password})
    });

    const data = await res.json();
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
}

async function login() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const res = await fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await res.json();
    token = data.access_token;

    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
}

// async function getProfile() {
//     const res = await fetch("/api/profile", {
//         method: "GET",
//         headers: {
//             "Authorization": "Bearer " + token
//         }
//     });

//     const data = await res.json();
//     document.getElementById("output").textContent = JSON.stringify(data, null, 2);
// }