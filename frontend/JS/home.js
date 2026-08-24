const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("previewImage");

// Preview Image
imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (file) {

        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";

    }

});

// Analyze Button
async function analyzeFace() {

    const file = imageInput.files[0];

    if (!file) {
        alert("No Image Selected");
        return;
    }

    alert("Step 1");

    const formData = new FormData();
    formData.append("file", file);

    alert("Step 2");

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/detect-landmarks",
            {
                method: "POST",
                body: formData
            }
        );

        alert("Step 3");

        const data = await response.json();

        alert("Step 4");

        console.log(data);

        alert(data.message);

    }
    catch(error){

        alert("ERROR");

        console.log(error);

    }

}