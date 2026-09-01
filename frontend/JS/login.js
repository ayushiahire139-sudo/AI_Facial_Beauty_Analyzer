async function loginUser() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    console.log("Email:", email);
    console.log("Password:", password);

    const BACKEND_URL = (window.location.port === "3000")
        ? `http://${window.location.hostname}:8000`
        : window.location.origin;

    const response = await fetch(`${BACKEND_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const data = await response.json();

    console.log(data);

    if (data.success) {
        alert("Login Successful!");
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("fullname", data.fullname);
        localStorage.setItem("email", data.email);
        window.location.href = "home.html";
    } else {
        alert(data.message);
    }
}