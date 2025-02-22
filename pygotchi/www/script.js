// Toggle Sidebar Menu
function toggleMenu() {
    const sidebar = document.getElementById("sidebar");
    const menuIcon = document.querySelector(".menu-icon");

    sidebar.classList.toggle("open"); // Toggle sidebar visibility
    menuIcon.classList.toggle("hidden"); // Hide/Show menu icon
}
// Shake Animation on Image Click
document.getElementById("to-shake").addEventListener("click", function() {
    this.classList.add("shake");
    setTimeout(() => {
        this.classList.remove("shake");
    }, 500);
});

// Websockets relative path
const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const wsHost = window.location.hostname;
const wsPort = window.location.port ? `:${window.location.port}` : ""; // Keep same port if specified

// Web Video API setup
const canvas = document.createElement("canvas");
canvas.id = "canvas-pixels";
canvas.width = 32;
canvas.height = 16;
const ctx = canvas.getContext("2d");
document.getElementById("canvas-pixels").appendChild(canvas);

const wsScreen = new WebSocket(`${wsProtocol}${wsHost}${wsPort}/ws/video`);

wsScreen.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.matrix) {  // Ensure matrix exists before rendering
        drawMatrix(data.matrix);
    }

    if (data.icons) { 
        drawIcons(data.icons);
    }

    if (data.background) {
        updateBackground(data.background);
    }

    if (data.runs !== undefined) {
        let switchElement = document.querySelector("#on-off-switch input");
        if (switchElement.checked !== data.runs) {  // Only update if the state changes
            switchElement.checked = data.runs;
            switchElement.dispatchEvent(new Event("change")); // Trigger the change event
        }
    }
};

// Function to update the UI with the correct background
const mainImage = document.getElementById("main-image");
function updateBackground(background) {
    mainImage.src = `www/img/${background}/background.png`;

    for (let i = 0; i < 8; i++) {
        let icon = document.getElementById(`icon-${i}`);
        if (icon) {
            icon.src = `www/img/${background}/icon${i}.png`;
        }
    }

    // Ensure the select reflects the current background
    selectElement.value = background;
}

// Function to draw pixels
function drawMatrix(matrix) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);  // Clear previous frame
    ctx.fillStyle = "black";

    for (let y = 0; y < matrix.length; y++) {
        for (let x = 0; x < matrix[y].length; x++) {
            if (matrix[y][x]) {
                ctx.fillRect(x, y, 1, 1);
            }
        }
    }
}

// Function to draw icons
function drawIcons(icons) {
    for (let i = 0; i < 8; i++) {
        let icon = document.getElementById(`icon-${i}`);
        if (icon) {
            icon.style.display = icons[i] ? "block" : "none";
        }
    }
}


// Web Audio API setup
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
const oscillator = audioCtx.createOscillator();
oscillator.type = "square"; // Simulating a buzzer
oscillator.start();
oscillator.connected = false; // Custom flag to track connection
let isMuted = false; // Track mute state

// Ensure audio starts only after user interaction
document.addEventListener("click", function startAudio() {
    if (audioCtx.state === "suspended") {
        audioCtx.resume();
    }
    document.removeEventListener("click", startAudio); // Remove event listener after first interaction
});

// WebSocket for audio updates
const wsAudio = new WebSocket(`${wsProtocol}${wsHost}${wsPort}/ws/audio`);

wsAudio.onopen = function() {
    console.log("WebSocket connected!");
};

wsAudio.onerror = function(error) {
    console.error("WebSocket Error:", error);
};

wsAudio.onclose = function() {
    console.log("WebSocket closed.");
};

wsAudio.onmessage = function(event) {
    console.log("Received:", event.data);
    const data = JSON.parse(event.data);
    if (!isMuted) {
        setFrequency(data.freq);
    }
};

// Function to update buzzer frequency
function setFrequency(freq) {
    if (freq > 0 && !isMuted) {
        oscillator.frequency.setValueAtTime(freq, audioCtx.currentTime);
        if (!oscillator.connected) {
            oscillator.connect(audioCtx.destination);
            oscillator.connected = true;
        }
    } else {
        oscillator.disconnect();
        oscillator.connected = false;
    }
}

// Microphone Toggle (🔊 to 🔇)
document.getElementById("mic-btn").addEventListener("click", function() {
    if (this.textContent === "🔊") {
        this.textContent = "🔇"; // Muted
        isMuted = true;
        oscillator.disconnect(); // Ensure buzzer is silent
    } else {
        this.textContent = "🔊"; // Unmuted
        isMuted = false;
        setFrequency(oscillator.frequency.value); // Restore last frequency
    }
});

document.getElementById("A").addEventListener("click", function() {
    fetch("/click?button=A", {
        method: "POST",
        headers: {
            "accept": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data))
    .catch(error => console.error("Error:", error));
});

document.getElementById("B").addEventListener("click", function() {
    fetch("/click?button=B", {
        method: "POST",
        headers: {
            "accept": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data))
    .catch(error => console.error("Error:", error));
});

document.getElementById("C").addEventListener("click", function() {
    fetch("/click?button=C", {
        method: "POST",
        headers: {
            "accept": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data))
    .catch(error => console.error("Error:", error));
});

document.getElementById("AC").addEventListener("click", function() {
    fetch("/click?button=AC", {
        method: "POST",
        headers: {
            "accept": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data))
    .catch(error => console.error("Error:", error));
});

document.getElementById("cpu-reset").addEventListener("click", function() {
    fetch("/cpu", {
        method: "DELETE",
        headers: {
            "accept": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data))
    .catch(error => console.error("Error:", error));
});

document.getElementById("cpu-upload").addEventListener("change", function() {
    let fileInput = this;
    let file = fileInput.files[0];
    if (!file) {
        console.error("No file selected");
        return;
    }
    let formData = new FormData();
    formData.append("file", file);
    fetch("/cpu", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data))
    .catch(error => console.error("Error:", error));
});

document.getElementById("rom-upload").addEventListener("change", function() {
    let fileInput = this;
    let file = fileInput.files[0];
    if (!file) {
        console.error("No file selected");
        return;
    }
    let formData = new FormData();
    formData.append("file", file);
    fetch("/rom", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data))
    .catch(error => console.error("Error:", error));
});

document.querySelector("#on-off-switch input").addEventListener("change", function() {
    if (this.checked) {
        // When switch is ON
        fetch("/manage?do=start", {
            method: "POST",
            headers: {
                "accept": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => console.log("Turned ON:", data))
        .catch(error => console.error("Error:", error));
    } else {
        // When switch is OFF
        fetch("/manage?do=stop", {
            method: "POST",
            headers: {
                "accept": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => console.log("Turned OFF:", data))
        .catch(error => console.error("Error:", error));
    }
});

document.getElementById("cpu-download").addEventListener("click", function() {
    window.location.href = "/cpu";
});

// Event listener for the select dropdown
const selectElement = document.querySelector(".custom-select select");
selectElement.addEventListener("change", function() {
    fetch("/background?theme=" + selectElement.value, {
        method: "POST",
        headers: {
            "accept": "application/json"
        }
    }).catch(error => console.error("Error sending background update:", error));
});
