// State
let allAgents = {};
let currentFilter = 'all';

// Mock Live Data generation for specific agents to make the test-drive dynamic
const mockMetrics = {
  ares: { threat: 'Low', scans: 0, status: 'Active Monitoring' },
  midas: { pnl: '+$420.50', positions: 3, status: 'Scanning Markets' },
  hermes: { latency: '12ms', nodes: 2, status: 'Connected' }
};

setInterval(() => {
  mockMetrics.ares.scans += Math.floor(Math.random() * 5);
  mockMetrics.ares.threat = Math.random() > 0.9 ? 'Elevated' : 'Low';
  
  let pnlChange = (Math.random() * 10 - 3).toFixed(2);
  let currentPnl = parseFloat(mockMetrics.midas.pnl.replace(/[^0-9.-]+/g,""));
  let newPnl = currentPnl + parseFloat(pnlChange);
  mockMetrics.midas.pnl = newPnl >= 0 ? `+$${newPnl.toFixed(2)}` : `-$${Math.abs(newPnl).toFixed(2)}`;
  
  mockMetrics.hermes.latency = Math.floor(Math.random() * 20 + 5) + 'ms';
  
  if(currentFilter === 'all' || ['ares', 'midas', 'hermes'].includes(currentFilter)) {
    renderAgents();
  }
}, 3000);

// Elements
const agentsGrid = document.getElementById('agents-grid');
const navBtns = document.querySelectorAll('.nav-btn');
const viewTitle = document.getElementById('current-view-title');
const refreshBtn = document.getElementById('refresh-btn');
const toastContainer = document.getElementById('toast-container');
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');
const bgLayer = document.getElementById('background-layer');

// Init
async function init() {
  setupEventListeners();
  await fetchAgents();
  checkNetwork();
  setInterval(checkNetwork, 10000);
}

// Fetch Agents from Dashboard API
async function fetchAgents() {
  try {
    const res = await fetch('http://localhost:5050/api/pantheon');
    if (!res.ok) throw new Error('API unreachable');
    allAgents = await res.json();
    renderAgents();
  } catch (error) {
    showToast('Dashboard API offline. Falling back to local Mission Control demo mode.', 'error');
    // Full Pantheon Fallback
    allAgents = {
        'athena': { name: 'Athena', title: 'Wisdom & General Chat', icon: 'assets/icons/Athena_Icon.png', banner: 'assets/banners/Athena_Banner.png', description: 'General purpose AI assistant powered by ChatLLM' },
        'prometheus': { name: 'Prometheus', title: 'Deep Reasoning & Research', icon: 'assets/icons/Prometheus_Icon.png', banner: 'assets/banners/Prometheus_Banner.png', description: 'Advanced reasoning using Gemini for complex analysis' },
        'hephaestus': { name: 'Hephaestus', title: 'Code Creation & Building', icon: 'assets/icons/Hephaestus_Icon.png', banner: 'assets/banners/Hephaestus_Banner.png', description: 'Code generation and project building with Antigravity' },
        'aergia': { name: 'Aergia', title: 'Rest & Healing', icon: 'assets/icons/Aergia_Icon.png', banner: 'assets/banners/Aergia_Banner.png', description: 'The lazy genius - rest, reflection, and restoration' },
        'hermes': { name: 'Hermes', title: 'Travel & Connection', icon: 'assets/icons/Hermes_Icon.png', banner: 'assets/banners/Hermes_Banner.png', description: 'Connect to Tailscale Network (Satellite Mode)' },
        'aura': { name: 'Aura', title: 'Energy & Wind', icon: 'assets/icons/Aura_Icon.png', banner: 'assets/banners/Aura_Banner.png', description: 'System monitoring and energy management' },
        'hestia': { name: 'Hestia', title: 'Hearth & Home', icon: 'assets/icons/Hestia_Icon.png', banner: 'assets/banners/Hestia_Banner.png', description: 'Local file management and home automation' },
        'hyperion': { name: 'Hyperion', title: 'AI Director & Oversight', icon: 'assets/icons/Hyperion_Icon.png', banner: 'assets/banners/Hyperion_Banner.png', description: 'AI video director and creative orchestration' },
        'midas': { name: 'Midas', title: 'Financial Engine', icon: 'assets/icons/Midas_Icon.png', banner: 'assets/banners/Midas_Banner.png', description: 'Financial tracking and value optimization' },
        'chimera': { name: 'Chimera', title: 'Video & Media Engine', icon: 'assets/icons/Chimera_Icon.png', banner: 'assets/banners/Chimera_Banner.png', description: 'AI video generation powered by FAL.ai' },
        'morai': { name: 'Morai', title: 'The Fates & Destiny', icon: 'assets/icons/Morai_Icon.png', banner: 'assets/banners/Morai_Banner.png', description: 'Weaving the threads of destiny and execution' },
        'kairos': { name: 'Kairos', title: 'Time & Scheduling', icon: 'assets/icons/Kairos_Icon.png', banner: 'assets/banners/Kairos_Banner.png', description: 'Task scheduling and temporal orchestration' },
        'plutus': { name: 'Plutus', title: 'Legacy & Final Output', icon: 'assets/icons/Plutus_Icon.png', banner: 'assets/banners/Plutus_Banner.png', description: 'Final output generation and legacy archiving' },
        'ares': { name: 'Ares', title: 'Cyber Defense', icon: 'assets/icons/Ares_Icon.png', banner: 'assets/banners/Ares_Banner.png', description: 'Find Evil! - Protocol SIFT / Nemo Claw' },
        'edge': { name: 'Edge AI', title: 'Local Offline Intelligence', icon: 'assets/icons/Prometheus_Icon.png', banner: 'assets/banners/Prometheus_Banner.png', description: 'Run open-weights models (Gemma/Hermes) locally for free via Ollama' }
    };

    renderAgents();
    console.error(error);
  }
}

// Network Check
async function checkNetwork() {
  try {
    const res = await fetch('http://localhost:5050/api/system/network_status');
    const data = await res.json();
    if (data.status === 'online') {
      statusIndicator.style.background = '#10b981';
      statusIndicator.style.boxShadow = '0 0 8px #10b981';
      statusText.textContent = 'Node Connected';
    } else {
      statusIndicator.style.background = '#ef4444';
      statusIndicator.style.boxShadow = '0 0 8px #ef4444';
      statusText.textContent = 'Node Offline';
    }
  } catch(e) {
    statusIndicator.style.background = '#fbbf24';
    statusIndicator.style.boxShadow = '0 0 8px #fbbf24';
    statusText.textContent = 'API Unreachable';
  }
}

// Render Logic
function renderAgents() {
  agentsGrid.innerHTML = '';
  
  const targetIds = currentFilter === 'all' 
    ? Object.keys(allAgents) 
    : [currentFilter];

  targetIds.forEach(id => {
    if (!allAgents[id]) return;
    const agent = allAgents[id];
    
    // We point images back to the dashboard server
    const imgUrl = `http://localhost:5050/${agent.icon}`;
    
    const card = document.createElement('div');
    card.className = 'agent-card glass-panel fade-in';
    card.setAttribute('data-id', id);
    
    // Background Swap Logic (Dashboard Integration)
    card.addEventListener('mouseenter', () => {
        if(agent.banner) {
            bgLayer.style.backgroundImage = `url('http://localhost:5050/${agent.banner}')`;
            bgLayer.style.opacity = '0.5';
        }
    });
    card.addEventListener('mouseleave', () => {
        bgLayer.style.backgroundImage = `url('http://localhost:5050/assets/wallpapers/The_Opening_Frame.png')`;
        bgLayer.style.opacity = '0.3';
    });
    
    let metricsHtml = '';
    if (mockMetrics[id]) {
      const m = mockMetrics[id];
      if(id === 'ares') metricsHtml = `<div style="margin-top: 10px; font-size: 0.8rem; color: #a0aec0; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; width:100%;">Status: <span style="color:#ef4444">${m.status}</span><br>Threat: ${m.threat}<br>Port Scans: ${m.scans}</div>`;
      if(id === 'midas') metricsHtml = `<div style="margin-top: 10px; font-size: 0.8rem; color: #a0aec0; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; width:100%;">Status: <span style="color:#fbbf24">${m.status}</span><br>PNL: <span style="color:${m.pnl.startsWith('+') ? '#10b981' : '#ef4444'}">${m.pnl}</span><br>Active Positions: ${m.positions}</div>`;
      if(id === 'hermes') metricsHtml = `<div style="margin-top: 10px; font-size: 0.8rem; color: #a0aec0; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; width:100%;">Status: <span style="color:#10b981">${m.status}</span><br>Latency: ${m.latency}<br>Nodes: ${m.nodes}</div>`;
    }

    card.innerHTML = `
      <div class="icon-container">
        <img src="${imgUrl}" alt="${agent.name}" class="god-icon" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'60\\' height=\\'60\\' fill=\\'%23555\\'><circle cx=\\'30\\' cy=\\'30\\' r=\\'30\\'/></svg>'">
      </div>
      <div class="agent-info">
        <h3>${agent.name}</h3>
        <p>${agent.title}</p>
      </div>
      <p class="agent-description">${agent.description}</p>
      ${metricsHtml}
      <div class="agent-actions">
        <button class="launch-btn" onclick="launchAgent('${id}')">Execute Protocol</button>
      </div>
    `;
    
    agentsGrid.appendChild(card);
  });
}

// Actions
window.launchAgent = async function(id) {
  try {
    showToast(`Initializing ${allAgents[id]?.name || id} Protocol...`);
    const res = await fetch(`http://localhost:5050/api/launch/${id}`);
    const data = await res.json();
    
    if (res.ok) {
      showToast(`${allAgents[id]?.name} Launched Successfully!`);
    } else {
      showToast(`Error: ${data.error}`, 'error');
    }
  } catch (err) {
    showToast(`Failed to connect to orchestrator.`, 'error');
    console.error(err);
  }
}

// Navigation
function setupEventListeners() {
  navBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      navBtns.forEach(b => b.classList.remove('active'));
      const target = e.currentTarget;
      target.classList.add('active');
      
      currentFilter = target.getAttribute('data-filter');
      viewTitle.textContent = target.textContent.trim();
      
      renderAgents();
    });
  });

  refreshBtn.addEventListener('click', () => {
    fetchAgents();
    checkNetwork();
    showToast('Syncing telemetry...');
  });
}

// UI Helpers
function showToast(message, type = 'info') {
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

// Start
document.addEventListener('DOMContentLoaded', init);
