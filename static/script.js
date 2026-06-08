function fileUploaded() {
document.getElementById("uploadText").innerText = "Image Uploaded ✓";
}


function openHistory() {
document.getElementById("historyPanel").classList.add("active");
}

function closeHistory() {
document.getElementById("historyPanel").classList.remove("active");
}

// Load particles.js
particlesJS.load('particles-js','https://cdn.jsdelivr.net/npm/particles.js/demo/particles.json');