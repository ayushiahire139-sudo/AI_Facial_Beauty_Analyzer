// ==========================================
// AI FACIAL BEAUTY ANALYZER - HOME/UPLOAD JS
// ==========================================

// Authentication check on page load
document.addEventListener("DOMContentLoaded", () => {
    const userId = localStorage.getItem("user_id");
    if (!userId) {
        alert("Please login first to access the analyzer.");
        window.location.href = "login.html";
        return;
    }
    setupDragAndDrop();
});

const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const previewContainer = document.getElementById("previewContainer");
const uploadZone = document.getElementById("uploadZone");
const loadingOverlay = document.getElementById("loadingOverlay");

function triggerFileInput() {
    imageInput.click();
}

// Setup drag and drop event listeners
function setupDragAndDrop() {
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
        }, false);
    });

    uploadZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) {
            imageInput.files = files;
            handleFileSelect(files[0]);
        }
    }, false);
}

// Preview selected image
imageInput.addEventListener("change", function () {
    if (this.files && this.files[0]) {
        handleFileSelect(this.files[0]);
    }
});

function handleFileSelect(file) {
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result;
            uploadZone.style.display = "none";
            previewContainer.style.display = "block";
            
            // Save Base64 representation of original image in localStorage
            // This is safe to transfer between pages and won't get revoked!
            localStorage.setItem("uploadedImage", e.target.result);
        };
        reader.readAsDataURL(file);
    }
}

function removePreview(event) {
    event.stopPropagation();
    imageInput.value = "";
    previewImage.src = "";
    previewContainer.style.display = "none";
    uploadZone.style.display = "block";
    localStorage.removeItem("uploadedImage");
}

// Analyze Face Function
async function analyzeFace() {
    const file = imageInput.files[0];
    if (!file) {
        alert("Please select or drop an image first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    // Show loading spinner
    loadingOverlay.style.display = "flex";

    try {
        const response = await fetch("http://127.0.0.1:8000/detect-landmarks", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Analysis Result:", data);

        if (!data.success) {
            alert(data.message || "Face analysis failed. Please try a clearer front-facing photo.");
            loadingOverlay.style.display = "none";
            return;
        }

        // Save analysis results in localStorage
        localStorage.setItem("beautyAnalysis", JSON.stringify(data));

        // Redirect to results dashboard
        window.location.href = "result.html";
    } catch (error) {
        console.error("Analysis Error:", error);
        loadingOverlay.style.display = "none";
        alert(
            "Connection failed.\n\n" +
            "Could not connect to the analysis engine. Please ensure the backend server is running at http://127.0.0.1:8000."
        );
    }
}

// Logout user
function logoutUser() {
    localStorage.clear();
    window.location.href = "login.html";
}