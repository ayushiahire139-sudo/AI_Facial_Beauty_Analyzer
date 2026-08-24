async function registerUser() {

    const fullname = document.getElementById("fullname").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (fullname === "" || email === "" || password === "") {
        alert("Please fill all fields.");
        return;
    }

    try {

        const response = await fetch("http://127.0.0.1:8000/register", {

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