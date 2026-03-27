import { SystemAPI } from './api.js';
import { UI } from './components.js';

async function refreshDashboard() {
    const data = await SystemAPI.getStats();
    if (!data) return;

    document.getElementById('mode-display').innerText = `Mode: ${data.mode}`;
    UI.updateStatus('uptime-val', data.uptime_percent);
    document.getElementById('sla-val').innerText = data.sla_status;
    document.getElementById('req-count').innerText = data.total_reqs;
}

// Initial setup
document.getElementById('app-root').innerHTML = `
    ${UI.renderMetric('uptime-val', 'Availability', '0%')}
    ${UI.renderMetric('sla-val', 'SLA Status', 'Initialising...')}
    ${UI.renderMetric('req-count', 'Total Requests', '0')}
`;

setInterval(refreshDashboard, 1000);

// stress testing to automate hits sent to web app for total requests
document.getElementById('stress-test').addEventListener('click', async () => {
    for(let i=0; i<100; i++) {
        SystemAPI.writeData(`key-${i}`, `val-${i}`);
    }
    alert("Sent 100 requests to the cluster!");
});

// event listener for changing the mode (strong, eventual, and quorum)
document.querySelectorAll('.mode-btn').forEach(button => {
    button.addEventListener('click', async () => {
        const mode = button.getAttribute('data-mode');
        const result = await SystemAPI.setMode(mode);
        console.log("Mode changed to:", result.current_mode);
        // Visual feedback
        refreshDashboard(); 
    });
});

// Check node health in conjunction with quorum to see what's going on
async function updateNodeLights() {
    const health = await SystemAPI.getHealth();
    console.log("Health Data Received:", health);
    if (!health) return;

    // Loop through the 3 nodes and update their CSS classes
    ['node-1', 'node-2', 'node-3'].forEach(nodeId => {
        const el = document.getElementById(`status-${nodeId}`);
        if (health[nodeId] === 'online') {
            el.classList.add('online');
            el.classList.remove('offline');
        } else {
            el.classList.add('offline');
            el.classList.remove('online');
        }
    });
}

// Run health checks every 2 seconds
setInterval(updateNodeLights, 2000);