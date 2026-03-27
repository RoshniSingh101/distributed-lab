const API_BASE = 'http://localhost:8080';

export const SystemAPI = {
    async getStats() {
        try {
            const response = await fetch(`${API_BASE}/stats`);
            return await response.json();
        } catch (error) {
            console.error("Coordinator Offline", error);
            return null;
        }
    },
    
    async writeData(key, value) {
        return await fetch(`${API_BASE}/data`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key, value })
        });
    }, 

    async setMode(modeName) {
        const response = await fetch(`${API_BASE}/mode`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: modeName })
        });
        return await response.json();
    },
    async getHealth() {
        try {
            const response = await fetch(`${API_BASE}/health`);
            return await response.json();
        } catch (e) {
            return null;
        }
    }
};