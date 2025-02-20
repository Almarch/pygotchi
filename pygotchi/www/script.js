// Toggle Sidebar Menu
function toggleMenu() {
    const sidebar = document.getElementById("sidebar");
    const menuIcon = document.querySelector(".menu-icon");

    sidebar.classList.toggle("open"); // Toggle sidebar visibility
    menuIcon.classList.toggle("hidden"); // Hide/Show menu icon
}
// Shake Animation on Image Click
document.getElementById("main-image").addEventListener("click", function() {
    this.classList.add("shake");
    setTimeout(() => {
        this.classList.remove("shake");
    }, 500);
});

// Microphone Toggle (🔊 to 🔇)
document.getElementById("mic-btn").addEventListener("click", function() {
    if (this.textContent === "🔊") {
        this.textContent = "🔇"; // Muted
    } else {
        this.textContent = "🔊"; // Unmuted
    }
});

// Web Video API setup
const canvas = document.createElement("canvas");
canvas.width = 32;
canvas.height = 32;
canvas.style.width = "256px";  // Scale for visibility
canvas.style.height = "256px";
document.body.appendChild(canvas);
const ctx = canvas.getContext("2d");

const wsScreen = new WebSocket("ws://localhost:8000/ws/video");

wsScreen.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.matrix) {  // Ensure matrix exists before rendering
        drawMatrix(data.matrix);
    }
};

// Function to draw pixels
function drawMatrix(matrix) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);  // Clear previous frame
    ctx.fillStyle = "black";

    for (let y = 0; y < matrix.length; y++) {
        for (let x = 0; x < matrix[y].length; x++) {
            if (matrix[y][x]) {
                ctx.fillRect(x, y, 1, 1);  // Draw pixel
            }
        }
    }
}

// Web Audio API setup
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
const oscillator = audioCtx.createOscillator();
oscillator.type = "square"; // Simulating a buzzer
oscillator.connect(audioCtx.destination);
oscillator.start();

// WebSocket for audio updates
const wsAudio = new WebSocket("ws://localhost:8000/ws/audio");

wsAudio.onmessage = function(event) {
    const data = JSON.parse(event.data);
    setFrequency(data.freq);
};

// Function to update buzzer frequency
function setFrequency(freq) {
    if (freq > 0) {
        oscillator.frequency.setValueAtTime(freq, audioCtx.currentTime);
    } else {
        oscillator.frequency.setValueAtTime(0, audioCtx.currentTime); // Silence
    }
}
