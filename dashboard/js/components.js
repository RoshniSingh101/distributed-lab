export const UI = {
    renderMetric(id, label, value, statusClass = '') {
        return `
            <div class="metric-card ${statusClass}">
                <div class="label">${label}</div>
                <div class="value" id="${id}">${value}</div>
            </div>
        `;
    },

    updateStatus(elementId, value, threshold = 99.9) {
        const el = document.getElementById(elementId);
        if (!el) return;
        el.innerText = value;
        // Visual feedback: Red if availability drops below SLA
        const numValue = parseFloat(value);
        el.className = numValue < threshold ? 'value danger' : 'value success';
    }
};