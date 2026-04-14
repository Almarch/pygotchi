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

    if (navigator.vibrate) {
        navigator.vibrate(500);
    }

    setTimeout(() => {
        this.classList.remove("shake");
    }, 500);
});

// Websockets relative path
const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const wsHost = window.location.hostname;
const wsPort = window.location.port ? `:${window.location.port}` : ""; // Keep same port if specified

// Web Video API setup
const PIXEL_SIZE = 7;
const GAP = 1;
const CELL = PIXEL_SIZE + GAP;
const LCD_ON = "#1c2a0a";
const LCD_OFF = "rgba(80, 100, 20, 0.06)";

const canvas = document.createElement("canvas");
canvas.id = "canvas-pixels";
canvas.width  = 32 * CELL - GAP;
canvas.height = 16 * CELL - GAP;
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

    if (data.care !== undefined) {
        let carebotCheckbox = document.querySelector("#carebot");
        if (carebotCheckbox.checked !== data.care) {
            carebotCheckbox.checked = data.care;
            carebotCheckbox.dispatchEvent(new Event("change"));
        }
    }
};

// Function to update the UI with the correct background
const mainImage = document.getElementById("main-image");
async function updateBackground(background) {
    mainImage.src = `www/img/${background}/background.png`;
    await colorizeIcons(background);
}

// Function to draw pixels
function drawMatrix(matrix) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let y = 0; y < 16; y++) {
        for (let x = 0; x < 32; x++) {
            const lit = matrix[y]?.[x];
            ctx.fillStyle = lit ? LCD_ON : LCD_OFF;
            ctx.beginPath();
            ctx.roundRect(x * CELL, y * CELL, PIXEL_SIZE, PIXEL_SIZE, 1.5);
            ctx.fill();
        }
    }
}

// Function to draw icons
async function colorizeIcons(background) {
    for (let i = 0; i < 8; i++) {
        const img = new Image();
        img.src = `www/img/${background}/icon${i}.png`;

        await new Promise(resolve => {
            if (img.complete) resolve();
            else img.onload = resolve;
        });

        for (const [id, color] of [
            [`tama-icon-${i}-on`,  LCD_ON],
            [`tama-icon-${i}-off`, LCD_OFF]
        ]) {
            const offscreen = new OffscreenCanvas(img.naturalWidth, img.naturalHeight);
            const ctx = offscreen.getContext("2d");
            ctx.drawImage(img, 0, 0);
            ctx.globalCompositeOperation = "source-in";
            ctx.fillStyle = color;
            ctx.fillRect(0, 0, offscreen.width, offscreen.height);

            const blob = await offscreen.convertToBlob();
            document.getElementById(id).src = URL.createObjectURL(blob);
        }
    }
}

function drawIcons(icons) {
    for (let i = 0; i < 8; i++) {
        const on  = document.getElementById(`tama-icon-${i}-on`);
        const off = document.getElementById(`tama-icon-${i}-off`);
        if (!on || !off) continue;
        on.style.display  = icons[i] ? "block" : "none";
        off.style.display = icons[i] ? "none"  : "block";
    }
}


// Web Audio API setup
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
const oscillator = audioCtx.createOscillator();
const gainNode = audioCtx.createGain();
oscillator.type = "square"; // Simulating a buzzer
gainNode.gain.value = 0.5; // Default volume
oscillator.connect(gainNode);
oscillator.start();
oscillator.connected = false; // Custom flag to track connection

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
    setFrequency(data.freq);
};

// Function to update buzzer frequency
function setFrequency(freq) {
    if (freq > 0) {
        oscillator.frequency.setValueAtTime(freq, audioCtx.currentTime);
        if (!oscillator.connected) {
            gainNode.connect(audioCtx.destination);
            oscillator.connected = true;
        }
    } else {
        gainNode.disconnect();
        oscillator.connected = false;
    }
}

// Volume slider UI update
const slider = document.getElementById('volume-slider');
const volIcon = document.querySelector('.volume-control .fa-icon');
let lastVolume = slider.value;

function updateVolume() {
    slider.style.setProperty('--val', slider.value * 100 + '%');
    volIcon.classList.toggle('fa-icon-volume-xmark-solid', slider.value == 0);
    volIcon.classList.toggle('fa-icon-volume-solid', slider.value != 0);
    setVolume(slider.value);
}

function setVolume(volume) {
    gainNode.gain.setValueAtTime(volume, audioCtx.currentTime);
}

slider.addEventListener('input', () => {
    if (slider.value > 0) lastVolume = slider.value;
    updateVolume();
});

volIcon.addEventListener('click', () => {
    slider.value = slider.value > 0 ? 0 : lastVolume;
    updateVolume();
});

// Action buttons
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

    if(navigator.vibrate) {
        navigator.vibrate(10);
    }
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

    if(navigator.vibrate) {
        navigator.vibrate(10);
    }
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
    
    if(navigator.vibrate) {
        navigator.vibrate(10);
    }
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
    
    if(navigator.vibrate) {
        navigator.vibrate(50);
    }
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

const carebotCheckbox = document.querySelector("#carebot");
const carebotIcon = document.querySelector('label[for="carebot"] .fa-icon');
let resetTimer = null;

carebotCheckbox.addEventListener("change", function() {

    carebotIcon.classList.toggle('fa-icon-heart-regular', !this.checked);
    carebotIcon.classList.toggle('fa-icon-heart-solid', this.checked);

    if (this.checked) {
        // Annule timer reset si actif
        if (resetTimer) {
            clearTimeout(resetTimer);
            resetTimer = null;
        }
        fetch("/carebot?do=start", {
            method: "POST",
            headers: { "accept": "application/json" }
        })
        .then(response => response.json())
        .then(data => console.log("Carebot started:", data))
        .catch(error => console.error("Error:", error));
    } else {
        // reset after 1 sec
        resetTimer = setTimeout(() => {
            fetch("/carebot?do=reset", {
                method: "POST",
                headers: { "accept": "application/json" }
            })
            .then(response => response.json())
            .then(data => console.log("Carebot reset:", data))
            .catch(error => console.error("Error:", error));
        }, 1000);

        // Send stop otherwise
        fetch("/carebot?do=stop", {
            method: "POST",
            headers: { "accept": "application/json" }
        })
        .then(response => response.json())
        .then(data => console.log("Carebot stopped:", data))
        .catch(error => console.error("Error:", error));
    }
});

document.getElementById("cpu-download").addEventListener("click", function() {
    window.location.href = "/cpu";
});

