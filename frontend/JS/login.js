async function loginUser() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    console.log("Email:", email);
    console.log("Password:", password);

    const response = await fetch("http://127.0.0.1:8000/login", {
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
        window.location.href = "home.html";
    } else {
        alert(data.message);
    }
}