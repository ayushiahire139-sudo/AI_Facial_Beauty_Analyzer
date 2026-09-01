async function registerUser() {

    const fullname = document.getElementById("fullname").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (fullname === "" || email === "" || password === "") {
        alert("Please fill all fields.");
        return;
    }

    try {

        const BACKEND_URL = (window.location.port === "3000")
            ? `http://${window.location.hostname}:8000`
            : window.location.origin;

        const response = await fetch(`${BACKEND_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                fullname: fullname,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (data.success) {

            alert("Registration Successful!");

            window.location.href = "login.html";

        } else {

            alert(data.message);

        }

    }

    catch (error) {

        alert("Server Error");

        console.log(error);

    }

}