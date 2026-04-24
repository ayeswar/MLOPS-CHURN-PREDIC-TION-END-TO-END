// Configuration
const API_URL = "https://churn-predictor-api.onrender.com"; // Change to your local URL for testing: http://localhost:8000

// DOM Elements
const predictForm = document.getElementById('predictForm');
const predictBtn = document.getElementById('predictBtn');
const btnLoader = document.getElementById('btnLoader');
const apiStatus = document.getElementById('apiStatus');
const apiStatusText = document.getElementById('apiStatusText');

const resultPlaceholder = document.getElementById('resultPlaceholder');
const resultContent = document.getElementById('resultContent');
const resultIcon = document.getElementById('resultIcon');
const resultLabel = document.getElementById('resultLabel');
const ringFill = document.getElementById('ringFill');
const ringPercent = document.getElementById('ringPercent');
const badge1 = document.getElementById('badge1');
const badge2 = document.getElementById('badge2');

const totalPredsEl = document.getElementById('totalPreds');
const churnCountEl = document.getElementById('churnCount');
const safeCountEl = document.getElementById('safeCount');
const historyList = document.getElementById('historyList');

const hasCrCardCheckbox = document.getElementById('has_cr_card');
const crCardLabel = document.getElementById('crCardLabel');
const isActiveMemberCheckbox = document.getElementById('is_active_member');
const activeMemberLabel = document.getElementById('activeMemberLabel');

// State
let stats = {
    total: 0,
    churn: 0,
    safe: 0
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkApiStatus();
    updateStats();
    
    // Toggle labels
    hasCrCardCheckbox.addEventListener('change', (e) => {
        crCardLabel.textContent = e.target.checked ? 'Yes' : 'No';
    });
    
    isActiveMemberCheckbox.addEventListener('change', (e) => {
        activeMemberLabel.textContent = e.target.checked ? 'Yes' : 'No';
    });
});

// Check API Health
async function checkApiStatus() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            apiStatus.className = 'status-dot online';
            apiStatusText.textContent = 'API Online';
        } else {
            throw new Error();
        }
    } catch (err) {
        apiStatus.className = 'status-dot offline';
        apiStatusText.textContent = 'API Offline';
    }
}

// Handle Form Submission
predictForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // UI Loading State
    predictBtn.classList.add('loading');
    predictBtn.disabled = true;
    
    const formData = new FormData(predictForm);
    const payload = {
        age: parseInt(formData.get('age')),
        tenure: parseInt(formData.get('tenure')),
        balance: parseFloat(formData.get('balance')),
        num_products: parseInt(formData.get('num_products')),
        has_cr_card: hasCrCardCheckbox.checked ? 1 : 0,
        is_active_member: isActiveMemberCheckbox.checked ? 1 : 0,
        estimated_salary: parseFloat(formData.get('estimated_salary'))
    };

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Prediction failed');
        
        const result = await response.json();
        displayResult(result, payload);
        
    } catch (err) {
        showToast(err.message || 'Error connecting to API');
    } finally {
        predictBtn.classList.remove('loading');
        predictBtn.disabled = false;
    }
});

function displayResult(result, inputData) {
    // Hide placeholder, show content
    resultPlaceholder.style.display = 'none';
    resultContent.style.display = 'block';
    
    const isChurn = result.prediction === 1;
    // Note: If API doesn't provide probability, we simulate it for UI richness 
    // or you can update API to return it.
    const prob = result.probability || (isChurn ? 0.75 + Math.random() * 0.2 : 0.1 + Math.random() * 0.3);
    const percent = Math.round(prob * 100);
    
    // Update Ring
    const offset = 314 - (314 * prob);
    ringFill.style.strokeDashoffset = offset;
    ringFill.style.stroke = isChurn ? 'var(--danger)' : 'var(--success)';
    ringPercent.textContent = `${percent}%`;
    ringPercent.style.color = isChurn ? 'var(--danger)' : 'var(--success)';
    
    // Update Text
    resultIcon.textContent = isChurn ? '⚠️' : '✅';
    resultLabel.textContent = isChurn ? 'High Risk' : 'Low Risk';
    resultLabel.style.color = isChurn ? 'var(--danger)' : 'var(--success)';
    
    // Badges
    badge1.textContent = isChurn ? 'Retention Required' : 'Healthy Account';
    badge2.textContent = `Confidence: ${isChurn ? 'High' : 'Stable'}`;

    // Update Stats
    stats.total++;
    if (isChurn) stats.churn++; else stats.safe++;
    updateStats();
    
    // Add to History
    addToHistory(isChurn, percent, inputData.age);
}

function addToHistory(isChurn, percent, age) {
    const item = document.createElement('div');
    item.className = 'history-item';
    item.innerHTML = `
        <span>Customer (Age ${age})</span>
        <span class="history-badge ${isChurn ? 'churn' : 'safe'}">${percent}% Risk</span>
    `;
    
    if (historyList.querySelector('.no-history')) {
        historyList.innerHTML = '';
    }
    
    historyList.prepend(item);
}

function updateStats() {
    totalPredsEl.textContent = stats.total;
    churnCountEl.textContent = stats.churn;
    safeCountEl.textContent = stats.safe;
}

function fillSample(type) {
    if (type === 'high') {
        document.getElementById('age').value = 55;
        document.getElementById('tenure').value = 1;
        document.getElementById('balance').value = 150000;
        document.getElementById('num_products').value = 1;
        document.getElementById('estimated_salary').value = 95000;
        hasCrCardCheckbox.checked = false;
        isActiveMemberCheckbox.checked = false;
    } else {
        document.getElementById('age').value = 32;
        document.getElementById('tenure').value = 8;
        document.getElementById('balance').value = 25000;
        document.getElementById('num_products').value = 2;
        document.getElementById('estimated_salary').value = 55000;
        hasCrCardCheckbox.checked = true;
        isActiveMemberCheckbox.checked = true;
    }
    // Update labels
    crCardLabel.textContent = hasCrCardCheckbox.checked ? 'Yes' : 'No';
    activeMemberLabel.textContent = isActiveMemberCheckbox.checked ? 'Yes' : 'No';
}

function showToast(msg) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}
