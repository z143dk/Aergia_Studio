// Aergia Unified Dashboard - Interactive Logic

// Marvel-Style Intro Logic
async function syncProject() {
    const btn = document.getElementById('sync-btn');
    const originalText = btn.innerText;

    btn.innerText = "⏳ Syncing...";
    btn.disabled = true;
    btn.style.background = "rgba(243, 156, 18, 0.2)";
    btn.style.borderColor = "#f39c12";

    try {
        const response = await fetch('/api/system/git_sync', { method: 'POST' });
        const data = await response.json();

        if (data.error) {
            alert("Sync Failed:\n" + data.error);
            btn.style.background = "rgba(231, 76, 60, 0.2)";
            btn.style.borderColor = "#c0392b";
            btn.innerText = "❌ Error";
        } else {
            console.log(data.log);
            alert("Sync Complete! Check console for log.");
            btn.style.background = "rgba(46, 204, 113, 0.2)";
            btn.style.borderColor = "#2ecc71";
            btn.innerText = "✅ Synced";
        }
    } catch (e) {
        alert("Network Error: " + e);
        btn.innerText = "❌ Net Error";
    }

    // Reset after 3s
    setTimeout(() => {
        btn.innerText = "☁️ Sync Project";
        btn.disabled = false;
        btn.style.background = "rgba(52, 152, 219, 0.2)";
        btn.style.borderColor = "#3498db";
        btn.style.color = "#3498db";
        btn.style.color = "#3498db";
    }, 3000);
}

// Taildrop Direct Sync Logic
async function taildropSync(mode) {
    let btnId = mode === 'secrets' ? 'secrets-btn' : 'taildrop-btn';
    const btn = document.getElementById(btnId);
    const originalText = btn.innerText;

    btn.innerText = "⏳ Sending...";
    btn.disabled = true;

    try {
        const response = await fetch('/api/system/taildrop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: mode })
        });
        const data = await response.json();

        if (data.error) {
            alert("Sync Failed:\n" + data.error);
            btn.innerText = "❌ Error";
        } else {
            console.log(data.message);
            alert(`✅ Success!\n${data.message}`);
            btn.innerText = "✅ Sent";
        }
    } catch (e) {
        alert("Network Error: " + e);
        btn.innerText = "❌ Net Error";
    }

    // Reset
    setTimeout(() => {
        btn.innerText = originalText;
        btn.disabled = false;
    }, 3000);
}

// Rsync Delta Sync Logic
async function deepSync() {
    const btn = document.getElementById('rsync-btn');
    const originalText = btn.innerText;

    btn.innerText = "⚡ Diffing & Syncing...";
    btn.disabled = true;

    try {
        const response = await fetch('/api/system/deep_sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        });
        const data = await response.json();

        if (data.error) {
            alert("Deep Sync Failed:\n" + data.error);
            btn.innerText = "❌ Error";
        } else {
            console.log("Deep Sync Log:", data.log);
            alert(`✅ ${data.message}\n(Check console for explicit files synced)`);
            btn.innerText = "✅ Delta Synced";
        }
    } catch (e) {
        alert("Network Error: " + e);
        btn.innerText = "❌ Net Error";
    }

    // Reset
    setTimeout(() => {
        btn.innerText = originalText;
        btn.disabled = false;
    }, 4000);
}

// Network Status Logic
let isNetworkOnline = false;

async function checkNetworkStatus() {
    const icon = document.getElementById('net-status');
    try {
        const response = await fetch('/api/system/network_status');
        const data = await response.json();

        if (data.status === 'online') {
            isNetworkOnline = true;
            icon.style.background = '#2ecc71'; // Green
            icon.style.boxShadow = '0 0 15px rgba(46, 204, 113, 0.6)';
            icon.title = "Network Online (Tailscale Connected)";
        } else {
            isNetworkOnline = false;
            icon.style.background = '#e74c3c'; // Red
            icon.style.boxShadow = '0 0 15px rgba(231, 76, 60, 0.6)';
            icon.title = "Network Offline - Click to Launch";
        }
    } catch (e) {
        icon.style.background = '#f39c12'; // Orange (Unknown)
        icon.title = "Network Status Unknown";
    }
}

async function handleNetworkClick() {
    if (isNetworkOnline) {
        alert("Network is Online and Healthy! 🟢");
        return;
    }

    // Launch if offline
    const icon = document.getElementById('net-status');
    icon.style.animation = "pulse 1s infinite"; // Add CSS animation class if exists, or just visual cue

    // Manual pulse effect
    icon.style.opacity = '0.5';
    alert("🚀 Launching Tailscale... Please wait.");

    try {
        const response = await fetch('/api/system/network_launch', { method: 'POST' });
        const data = await response.json();
        console.log(data);

        // Poll aggressively for 10 seconds
        let attempts = 0;
        const quickPoll = setInterval(async () => {
            await checkNetworkStatus();
            attempts++;
            if (isNetworkOnline || attempts > 10) {
                clearInterval(quickPoll);
                icon.style.opacity = '1';
                if (isNetworkOnline) alert("Tailscale Connected! ✅");
            }
        }, 2000);

    } catch (e) {
        alert("Launch Error: " + e);
        icon.style.opacity = '1';
    }
}

// Start Polling
setInterval(checkNetworkStatus, 10000); // Every 10s
document.addEventListener('DOMContentLoaded', () => {
    checkNetworkStatus(); // Initial check 
});


// Hive Mind Logic
function toggleHive() {
    const term = document.getElementById('hive-terminal');
    if (term.style.display === 'none') {
        term.style.display = 'block';
        document.getElementById('hive-input').focus();
    } else {
        term.style.display = 'none';
    }
}

function handleHiveEnter(e) {
    if (e.key === 'Enter') {
        sendToHive();
    }
}

async function sendToHive() {
    const input = document.getElementById('hive-input');
    const output = document.getElementById('hive-output');
    const prompt = input.value.trim();

    if (!prompt) return;

    // Append user query
    output.innerText += `\n> ${prompt}\n`;
    output.innerText += `[SYSTEM] Deploying Swarm... (This may take a moment)\n`;
    input.value = '';
    output.scrollTop = output.scrollHeight;

    try {
        const response = await fetch('/api/ask_hive', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        });
        const data = await response.json();

        if (data.error) {
            output.innerText += `[ERROR] ${data.error}\n`;
        } else {
            output.innerText += `\n--- SWARM REPORT ---\n${data.response}\n\n> Ready.\n`;
        }
    } catch (e) {
        output.innerText += `[NETWORK ERROR] ${e}\n`;
    }
    output.scrollTop = output.scrollHeight;
}

function clearHiveLog() {
    const output = document.getElementById('hive-output');
    output.innerText = "🐝 Hive Mind Initialized. Awaiting Input...\n";
}

document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById('intro-overlay');
    const sequence = document.getElementById('intro-sequence');
    const logo = document.getElementById('intro-logo');
    const container = document.querySelector('.container');

    // [PWA FIX] Wait for Interaction
    // If PWA, show a "Start" button to unlock audio and intro
    const isPWA = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;

    // Define music globally within this scope so all functions can use it
    const music = document.getElementById('bg-music');

    // Define flicker globally within this scope so skipIntro can stop it
    let flicker = null;

    // [NEW] Universal Entrance Logic to bypass Autoplay blockers
    window.awakenAergia = function () {
        const entranceOverlay = document.getElementById('entrance-overlay');

        // Hide entrance, show Marvel intro
        entranceOverlay.style.display = 'none';
        overlay.style.display = 'flex'; // It was hidden in HTML
        sequence.style.display = 'block';

        // The crucial step: Trigger audio on user click
        if (music) {
            music.volume = 0.5;
            music.play().then(() => {
                const playBtn = document.getElementById('play-pause-btn');
                if (playBtn) playBtn.textContent = '⏸️';
            }).catch(e => console.log("Audio play failed on awaken:", e));
        }

        startIntro();
    };

    function startIntro() {
        // Gather all icon paths from the grid
        let icons = Array.from(document.querySelectorAll('.god-icon')).map(img => img.src);

        // [RESTORED] Cinematic Intro Frames (Using available banners/wallpapers)
        const introFrames = [
            '/assets/banners/Aergia_Banner.png',
            '/assets/banners/Athena_Banner.png',
            '/assets/banners/Aura_Banner.png',
            '/assets/banners/Chimera_Banner.png',
            '/assets/banners/Hephaestus_Banner.png',
            '/assets/banners/Hermes_Banner.png',
            '/assets/banners/Hestia_Banner.png',
            '/assets/banners/Hyperion_Banner.png',
            '/assets/banners/Kairos_Banner.png',
            '/assets/banners/Midas_Banner.png',
            '/assets/banners/Plutus_Banner.png',
            '/assets/banners/Prometheus_Banner.png',
            // Dedicated Cinema Intro
            '/assets/intro/intro_1.png',
            '/assets/intro/intro_2.png',
            '/assets/intro/intro_3.jpg',
            '/assets/intro/intro_4.png',
            '/assets/intro/intro_5.png',
            '/assets/intro/intro_6.jpg',
            '/assets/intro/intro_7.png',
            '/assets/intro/intro_8.png',
            '/assets/intro/intro_9.jpg',
            '/assets/intro/intro_10.png'
        ];
        // Mix them in to add variety
        icons = icons.concat(introFrames).concat(introFrames);

        // Audio Autoplay Logic
        if (music) {
            music.volume = 0.5;
            music.play().catch(e => console.log("Audio waiting for interaction", e));
        }

        let step = 0;
        const totalSteps = 20; // Increased steps for more "movie" feel
        const intervalTime = 1500; // Slower flicker for drama

        // Start the loop
        flicker = setInterval(() => {
            const randomIcon = icons[Math.floor(Math.random() * icons.length)];
            sequence.style.backgroundImage = `url('${randomIcon}')`;
            step++;

            if (step >= totalSteps) {
                clearInterval(flicker);
                finishIntro();
            }
        }, intervalTime);
    }

    // Expose skipper separately
    window.skipIntro = function () {
        console.log("Intro Skipped");
        if (flicker) clearInterval(flicker);

        // Immediately hide overlay without slow fade
        overlay.style.display = 'none';
        container.style.opacity = '1';
        container.style.animation = 'none';

        // Ensure music plays if it wasn't already
        if (music && music.paused) {
            music.play().then(() => {
                const playBtn = document.getElementById('play-pause-btn');
                if (playBtn) playBtn.textContent = '⏸️';
            }).catch(e => {
                console.log("Autoplay blocked on skip", e);
                const playBtn = document.getElementById('play-pause-btn');
                if (playBtn) playBtn.textContent = '▶️';
            });
        }
    };

    function finishIntro() {
        if (flicker) clearInterval(flicker); // Safety clear

        sequence.style.display = 'none';
        logo.style.opacity = '1';
        logo.style.transform = 'scale(1.2)';

        // Hold logo then fade out
        setTimeout(() => {
            overlay.style.transition = 'opacity 1s ease';
            overlay.style.opacity = '0';

            // Allow UI to appear
            container.style.opacity = '1';

            setTimeout(() => {
                overlay.style.display = 'none';
            }, 1000);
        }, 1500);
    }

    // --- Media Player Logic ---
    const volSlider = document.getElementById('volume-slider');
    const volIcon = document.getElementById('vol-icon');
    const playBtn = document.getElementById('play-pause-btn');
    const lyricsPanel = document.getElementById('lyrics-panel');

    // Global Toggles
    window.togglePlay = function () {
        if (music.paused) {
            music.play();
            playBtn.textContent = '⏸️';
        } else {
            music.pause();
            playBtn.textContent = '▶️';
        }
    };

    window.toggleLyrics = function () {
        if (lyricsPanel.style.display === 'none') {
            lyricsPanel.style.display = 'block';
        } else {
            lyricsPanel.style.display = 'none';
        }
    };

    if (volSlider && music) {
        // Set initial value
        volSlider.value = music.volume;

        volSlider.addEventListener('input', (e) => {
            music.volume = e.target.value;
            updateVolIcon(music.volume);
        });

        // Mute toggle
        volIcon.addEventListener('click', () => {
            if (music.volume > 0) {
                music.dataset.prevVol = music.volume;
                music.volume = 0;
                volSlider.value = 0;
            } else {
                music.volume = music.dataset.prevVol || 0.5;
                volSlider.value = music.volume;
            }
            updateVolIcon(music.volume);
        });

        function updateVolIcon(vol) {
            if (vol == 0) volIcon.textContent = '🔇';
            else if (vol < 0.5) volIcon.textContent = '🔉';
            else volIcon.textContent = '🔊';
        }
    }

    // --- Cinema Sync Logic ---
    // --- Cinema Sync Logic ---
    const cinVideo = document.getElementById('cinema-video');
    const cinAudio = document.getElementById('cinema-audio');
    const cinBtn = document.getElementById('cin-play-btn');

    // 1. Toggle Play/Pause
    window.toggleCinema = function () {
        if (cinVideo.paused) {
            // Start Cinema
            cinVideo.play();
            cinAudio.currentTime = cinVideo.currentTime; // Sync start
            cinAudio.play();
            cinBtn.textContent = '⏸️ Pause';
            cinBtn.style.opacity = '0.8';

            // NOTE: We NO LONGER hide controls here. 
            // CSS :hover handles visibility now.

            // Pause Ambient
            if (music && !music.paused) {
                music.pause();
                window.wasBgPlaying = true;
            }
        } else {
            // Pause Cinema
            cinVideo.pause();
            cinAudio.pause();
            cinBtn.textContent = '▶️ Play Movie';
            cinBtn.style.opacity = '1';

            // Resume Ambient if it was playing
            if (window.wasBgPlaying && music) {
                music.play();
                const playBtn = document.getElementById('play-pause-btn');
                if (playBtn) playBtn.textContent = '⏸️';
            }
        }
    };

    // 2. Restart Logic
    window.restartCinema = function () {
        cinVideo.currentTime = 0;
        cinAudio.currentTime = 0;
        if (cinVideo.paused) {
            window.toggleCinema(); // Start playing if paused
        }
    };

    // 3. Volume Logic (Fixed)
    const cinVolSlider = document.getElementById('cin-volume-slider');
    if (cinVolSlider) {
        cinVideo.volume = 0; // Ensure video is muted (it's muted in HTML too)
        cinAudio.volume = cinVolSlider.value; // Sync audio to slider start

        cinVolSlider.addEventListener('input', (e) => {
            cinAudio.volume = e.target.value;
        });
    }

    // Ensure Sync loop (in case of drift)
    if (cinVideo && cinAudio) {
        cinVideo.addEventListener('seeked', () => {
            cinAudio.currentTime = cinVideo.currentTime;
        });

        // Stop audio when video ends
        cinVideo.addEventListener('ended', () => {
            cinAudio.pause();
            cinAudio.currentTime = 0;
            cinBtn.textContent = '▶️ Replay';

            if (window.wasBgPlaying && music) music.play();
        });
    }

});

// Aergia Unified Dashboard - Interactive Logic

// Background swap on hover
document.querySelectorAll('.god-card').forEach(card => {
    card.addEventListener('mouseenter', function () {
        const banner = this.getAttribute('data-banner');
        const bgLayer = document.getElementById('background-layer');
        if (banner) {
            bgLayer.style.backgroundImage = `url('/${banner}')`;
            bgLayer.style.opacity = '0.4';
        }
    });

    card.addEventListener('mouseleave', function () {
        const bgLayer = document.getElementById('background-layer');
        bgLayer.style.backgroundImage = "url('/assets/wallpapers/The_Opening_Frame.png')";
        bgLayer.style.opacity = '0.3';
    });
});

// Launch module
function launchModule(godId) {
    const statusText = document.getElementById('status-text');
    statusText.textContent = `Launching ${godId}...`;

    // Open target window synchronously to bypass popup blocker
    let newWin = null;
    if (godId === 'ares') {
        newWin = window.open('about:blank', '_blank');
    } else if (godId === 'hestia') {
        newWin = window.open('about:blank', '_blank');
    }

    fetch(`/api/launch/${godId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'launched') {
                statusText.textContent = `✓ ${data.module} launched successfully`;
                statusText.style.color = '#4cd137';
                
                if (godId === 'ares' && newWin) {
                    newWin.location.href = "http://localhost:5051";
                } else if (godId === 'hestia' && newWin) {
                    newWin.location.href = "http://localhost:5000";
                }
                
                setTimeout(() => {
                    statusText.textContent = 'Ready';
                }, 3000);
            } else if (data.status === 'coming_soon') {
                statusText.textContent = `${data.module} - Coming Soon`;
                statusText.style.color = '#fbc531';
                setTimeout(() => {
                    statusText.textContent = 'Ready';
                    statusText.style.color = '#4cd137';
                }, 2000);
            } else if (data.status === 'rest_mode_activated') {
                statusText.textContent = '🌙 Aergia Mode: Rest & Heal...';

                // Cinematic Transition
                const bgLayer = document.getElementById('background-layer');
                const grid = document.querySelector('.pantheon-grid');
                const header = document.querySelector('header');
                const music = document.getElementById('bg-music');

                // Visual Ambience
                // Attempt to use Rest Banner if available, fallback to default logic if needed
                bgLayer.style.backgroundImage = "url('/assets/banners/Aergia_Banner.png')";
                bgLayer.style.opacity = '0.8';
                grid.style.opacity = '0.1';
                grid.style.pointerEvents = 'none'; // Disable grid interactions
                header.style.filter = 'blur(5px)';

                // Audio Ambience
                if (music) {
                    music.volume = 0;
                    music.play();
                    // Gentle Fade In
                    let vol = 0;
                    const fade = setInterval(() => {
                        if (vol < 0.8) {
                            vol += 0.05;
                            music.volume = vol;
                        } else {
                            clearInterval(fade);
                        }
                    }, 200);
                }

                // To exit: Click anywhere
                document.body.onclick = function () {
                    bgLayer.style.opacity = '0.3';
                    bgLayer.style.backgroundImage = "url('/assets/wallpapers/The_Opening_Frame.png')";

                    grid.style.opacity = '1';
                    grid.style.pointerEvents = 'auto';
                    header.style.filter = 'none';
                    statusText.textContent = 'Ready';

                    // Stop Music
                    if (music) {
                        music.pause();
                        music.currentTime = 0;
                    }

                    // Remove this specific listener to avoid conflict
                    document.body.onclick = null;
                };
            } else if (data.error) {
                statusText.textContent = `Error: ${data.error}`;
                statusText.style.color = '#e84118';
            }
        })
        .catch(error => {
            statusText.textContent = `Error: ${error.message}`;
            statusText.style.color = '#e84118';
            console.error('Launch error:', error);
        });
}

// Keyboard shortcuts
document.addEventListener('keydown', function (e) {
    // [FIX] Press 'Escape' to close Hive Terminal
    if (e.key === 'Escape') {
        const term = document.getElementById('hive-terminal');
        if (term.style.display !== 'none') {
            toggleHive();
            return;
        }
    }

    // [FIX] Ignore ALL shortcuts if typing in an input field (Hive Terminal, etc.)
    // [FIX] Ignore ALL shortcuts if typing in an input field (Hive Terminal, etc.)
    if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') {
        return;
    }

    // Press 'R' for Rest Mode (Aergia)
    if (e.key === 'r' || e.key === 'R') {
        launchModule('aergia');
    }
    // Press 'H' for Hephaestus (Code)
    if (e.key === 'h' || e.key === 'H') {
        launchModule('hephaestus');
    }

    // Press 'Space' to Toggle UI (Hide/Show)
    if (e.code === 'Space') {
        // Ignore if typing
        if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') return;

        const container = document.querySelector('.container');
        if (container.style.opacity === '0') {
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        } else {
            container.style.opacity = '0';
            container.style.transform = 'translateY(20px)';
        }
    }

    // Press 'M' for Cinema Mode (Mini Movie)
    if (e.code === 'KeyM') {
        toggleCinemaMode();
    }
});

function toggleCinemaMode() {
    const cinemaOverlay = document.getElementById('cinema-overlay');
    const cinemaVideo = document.getElementById('cinema-video');
    const bgMusic = document.getElementById('bg-music');
    const closeBtn = document.getElementById('close-cinema');

    if (cinemaOverlay.style.display === 'none') {
        // OPEN CINEMA
        cinemaOverlay.style.display = 'flex';
        if (bgMusic) bgMusic.pause(); // Pause ambient theme
        cinemaVideo.currentTime = 0;
        cinemaVideo.play();

        // Close handler
        closeBtn.onclick = () => {
            cinemaOverlay.style.display = 'none';
            cinemaVideo.pause();
            if (bgMusic) bgMusic.play(); // Resume theme
        };
    } else {
        // CLOSE CINEMA (Toggle)
        cinemaOverlay.style.display = 'none';
        cinemaVideo.pause();
        if (bgMusic) bgMusic.play();
    }
}

console.log('🧿 Aergia Dashboard Loaded');

// --- MISSION CONTROL INTEGRATION ---

// Telemetry State
const mockMetrics = {
  ares: { threat: 'Low', scans: 0, status: 'Active Monitoring' },
  midas: { pnl: '+$420.50', positions: 3, status: 'Scanning Markets' },
  hermes: { latency: '12ms', nodes: 2, status: 'Connected' }
};

let currentFilter = 'all';

// Setup Telemetry Loop
setInterval(() => {
  mockMetrics.ares.scans += Math.floor(Math.random() * 5);
  mockMetrics.ares.threat = Math.random() > 0.9 ? 'Elevated' : 'Low';
  
  let pnlChange = (Math.random() * 10 - 3).toFixed(2);
  let currentPnl = parseFloat(mockMetrics.midas.pnl.replace(/[^0-9.-]+/g,""));
  let newPnl = currentPnl + parseFloat(pnlChange);
  mockMetrics.midas.pnl = newPnl >= 0 ? `+$${newPnl.toFixed(2)}` : `-$${Math.abs(newPnl).toFixed(2)}`;
  
  mockMetrics.hermes.latency = Math.floor(Math.random() * 20 + 5) + 'ms';
  
  updateMetricsUI();
}, 3000);

function updateMetricsUI() {
    ['ares', 'midas', 'hermes'].forEach(id => {
        const container = document.getElementById(`metrics-${id}`);
        if (!container) return;
        const m = mockMetrics[id];
        let metricsHtml = '';

        if(id === 'ares') {
            const pulseClass = m.threat === 'Elevated' ? 'danger' : '';
            metricsHtml = `<div style="margin-top: 10px; font-size: 0.8rem; color: #a0aec0; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; width:100%; text-align: left;">
            Status: <span class="status-pulse ${pulseClass}"></span><span style="color:#ef4444">${m.status}</span><br>Threat: ${m.threat}<br>Port Scans: ${m.scans}
            <div class="live-progress-container"><div class="live-progress-bar" style="background: var(--agent-ares)"></div></div>
            </div>`;
        }
        if(id === 'midas') {
            metricsHtml = `<div style="margin-top: 10px; font-size: 0.8rem; color: #a0aec0; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; width:100%; text-align: left;">
            Status: <span class="status-pulse"></span><span style="color:#fbbf24">${m.status}</span><br>PNL: <span style="color:${m.pnl.startsWith('+') ? '#10b981' : '#ef4444'}">${m.pnl}</span><br>Active Positions: ${m.positions}
            <div class="live-progress-container"><div class="live-progress-bar" style="background: var(--agent-midas)"></div></div>
            </div>`;
        }
        if(id === 'hermes') {
            metricsHtml = `<div style="margin-top: 10px; font-size: 0.8rem; color: #a0aec0; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; width:100%; text-align: left;">
            Status: <span class="status-pulse"></span><span style="color:#10b981">${m.status}</span><br>Latency: ${m.latency}<br>Nodes: ${m.nodes}
            <div class="live-progress-container"><div class="live-progress-bar" style="background: var(--agent-hermes)"></div></div>
            </div>`;
        }

        container.innerHTML = metricsHtml;
    });
}

// Sidebar Navigation Logic
document.addEventListener('DOMContentLoaded', () => {
  const navBtns = document.querySelectorAll('.nav-btn');
  const viewTitle = document.getElementById('current-view-title');
  const cards = document.querySelectorAll('.agent-card');

  navBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      navBtns.forEach(b => b.classList.remove('active'));
      const target = e.currentTarget;
      target.classList.add('active');
      
      currentFilter = target.getAttribute('data-filter');
      viewTitle.textContent = target.textContent.trim();
      
      // Filter Grid
      cards.forEach(card => {
        if (currentFilter === 'all' || card.getAttribute('data-id') === currentFilter) {
            card.style.display = 'flex';
            // re-trigger animation
            card.classList.remove('fade-in');
            void card.offsetWidth; // trigger reflow
            card.classList.add('fade-in');
        } else {
            card.style.display = 'none';
        }
      });
    });
  });

  const refreshBtn = document.getElementById('refresh-btn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      showToast('Syncing telemetry...');
      checkNetworkStatus(); // from existing script
    });
  }

  // Initial render of metrics
  updateMetricsUI();
});

// UI Helper
function showToast(message, type = 'info') {
  const toastContainer = document.getElementById('toast-container');
  if (!toastContainer) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  
  const icon = type === 'error' ? '⚠️' : '✅';
  const color = type === 'error' ? '#ef4444' : '#3b82f6';
  toast.style.borderLeftColor = color;
  
  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
  
  toastContainer.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'fadeOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
