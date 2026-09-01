// ==========================================
// AI FACIAL BEAUTY ANALYZER - RESULTS JS
// ==========================================

const BACKEND_URL = (window.location.port === "3000")
    ? `http://${window.location.hostname}:8000`
    : window.location.origin;

// Auth Check on page load
document.addEventListener("DOMContentLoaded", () => {
    const userId = localStorage.getItem("user_id");
    if (!userId) {
        alert("Please login first to view results.");
        window.location.href = "login.html";
        return;
    }
    
    loadAnalysisData();
    setupImageSlider();
});

function loadAnalysisData() {
    const rawData = localStorage.getItem("beautyAnalysis");
    const originalImg = localStorage.getItem("uploadedImage");
    
    if (!rawData) {
        alert("No analysis data found. Please run the analyzer first.");
        window.location.href = "home.html";
        return;
    }

    const data = JSON.parse(rawData);
    console.log("Analysis Output:", data);

    // 1. Render Images
    const originalImageEl = document.getElementById("originalImage");
    const resultImageEl = document.getElementById("resultImage");

    if (originalImg) {
        originalImageEl.src = originalImg;
    }
    if (data.processed_image) {
        resultImageEl.src = `${BACKEND_URL}/${data.processed_image}`;
    }

    // 2. Render Score and Circle Ring
    const score = data.beauty_score ?? 0;
    document.getElementById("beautyScore").textContent = score;
    
    const circle = document.getElementById("scoreCircle");
    if (circle) {
        // Circumference of our circle is 2 * pi * r = 2 * 3.14159 * 65 = 408.4
        const circumference = 408;
        const offset = circumference - (score / 100) * circumference;
        circle.style.setProperty('--offset', `${offset}`);
        circle.style.strokeDashoffset = offset;
    }

    // 3. Badges Information
    document.getElementById("faceShape").textContent = data.face_shape ?? "N/A";
    document.getElementById("skinTone").textContent = data.skin_tone ?? "N/A";
    document.getElementById("estimatedAge").textContent = data.estimated_age ?? "N/A";
    document.getElementById("gender").textContent = data.gender ?? "N/A";
    document.getElementById("emotion").textContent = data.emotion ?? "N/A";

    // 4. Feature Proportions Table
    if (data.eye_analysis) {
        document.getElementById("eyeDistance").textContent = `Distance: ${data.eye_analysis.eye_distance || "N/A"}`;
        document.getElementById("eyeSymmetry").textContent = `Size: ${data.eye_analysis.eye_size || "N/A"} | Symmetry: ${data.eye_analysis.eye_symmetry || "N/A"}`;
    }
    if (data.nose_analysis) {
        document.getElementById("noseWidth").textContent = `Width: ${data.nose_analysis.nose_width || "N/A"}`;
        document.getElementById("noseLength").textContent = `Length: ${data.nose_analysis.nose_length || "N/A"} | Shape: ${data.nose_analysis.nose_shape || "N/A"}`;
    }
    if (data.lip_analysis) {
        document.getElementById("lipWidth").textContent = `Width: ${data.lip_analysis.lip_width || "N/A"}`;
        document.getElementById("lipHeight").textContent = `Height: ${data.lip_analysis.lip_height || "N/A"} | Shape: ${data.lip_analysis.lip_shape || "N/A"}`;
    }
    if (data.jaw_analysis) {
        document.getElementById("jawWidth").textContent = `Width: ${data.jaw_analysis.jaw_width || "N/A"}`;
        document.getElementById("jawShape").textContent = `Shape: ${data.jaw_analysis.jaw_shape || "N/A"}`;
    }

    document.getElementById("symmetryScore").textContent = `Score: ${data.symmetry_score ?? "N/A"}/100`;
    document.getElementById("symmetryRating").textContent = score >= 85 ? "Excellent Balance" : "Good Balance";

    document.getElementById("goldenRatio").textContent = `Score: ${data.golden_ratio_score ?? "N/A"}/100`;
    document.getElementById("goldenRatioRating").textContent = (data.golden_ratio_score ?? 0) >= 80 ? "Highly Proportional" : "Standard Proportions";

    // 5. Recommendations Text
    const recs = data.beauty_report?.recommendations || data.recommendations;
    if (recs) {
        document.getElementById("recSkincare").textContent = recs.skincare || "No specific skin recommendations.";
        document.getElementById("recHairstyle").textContent = recs.hairstyle || "No specific hair recommendations.";
        document.getElementById("recMakeup").textContent = recs.makeup || "No specific cosmetics recommendations.";
        document.getElementById("recLifestyle").textContent = recs.lifestyle || "No specific lifestyle recommendations.";
    }

    // 6. PDF Link Handler
    const downloadBtn = document.getElementById("downloadPdf");
    if (downloadBtn) {
        downloadBtn.onclick = async () => {
            if (data.pdf_report) {
                try {
                    downloadBtn.disabled = true;
                    const originalText = downloadBtn.innerHTML;
                    downloadBtn.innerHTML = "⏳ Generating Download...";
                    
                    const response = await fetch(`${BACKEND_URL}/${data.pdf_report}`);
                    if (!response.ok) throw new Error("Could not download file");
                    
                    const blob = await response.blob();
                    const blobUrl = URL.createObjectURL(blob);
                    
                    const link = document.createElement("a");
                    link.href = blobUrl;
                    link.download = data.pdf_report.split('/').pop() || "beauty_report.pdf";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    // Revoke the Object URL shortly after download to free memory
                    setTimeout(() => URL.revokeObjectURL(blobUrl), 100);
                    
                    downloadBtn.disabled = false;
                    downloadBtn.innerHTML = originalText;
                } catch (err) {
                    console.error("PDF Download error:", err);
                    // Fallback to opening in new window if download fails
                    window.open(`${BACKEND_URL}/${data.pdf_report}`, "_blank");
                    downloadBtn.disabled = false;
                    downloadBtn.innerHTML = "📥 Download PDF Report";
                }
            } else {
                alert("PDF report is not available for this session.");
            }
        };
    }
}

// Interactive slider setup
function setupImageSlider() {
    const container = document.getElementById("sliderContainer");
    const handle = document.getElementById("sliderHandle");
    const afterImg = document.getElementById("resultImage");

    if (!container || !handle || !afterImg) return;

    let isSliding = false;

    function moveSlider(clientX) {
        const rect = container.getBoundingClientRect();
        const x = clientX - rect.left;
        let percentage = (x / rect.width) * 100;

        if (percentage < 0) percentage = 0;
        if (percentage > 100) percentage = 100;

        handle.style.left = `${percentage}%`;
        // Clip-path syntax: polygon(0 0, percentage% 0, percentage% 100%, 0 100%)
        afterImg.style.clipPath = `polygon(0 0, ${percentage}% 0, ${percentage}% 100%, 0 100%)`;
    }

    // Mouse Events
    container.addEventListener("mousedown", () => isSliding = true);
    window.addEventListener("mouseup", () => isSliding = false);
    
    container.addEventListener("mousemove", (e) => {
        if (!isSliding) return;
        moveSlider(e.clientX);
    });

    // Touch Events for Mobile
    container.addEventListener("touchstart", () => isSliding = true);
    window.addEventListener("touchend", () => isSliding = false);
    
    container.addEventListener("touchmove", (e) => {
        if (!isSliding) return;
        if (e.touches.length > 0) {
            moveSlider(e.touches[0].clientX);
        }
    });
}

function goHome() {
    // Keep user credentials but clean analysis
    localStorage.removeItem("beautyAnalysis");
    localStorage.removeItem("uploadedImage");
    window.location.href = "home.html";
}

function logoutUser() {
    localStorage.clear();
    window.location.href = "login.html";
}