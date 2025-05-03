// Dynamic form generation
function updateFields() {
    const count = parseInt(document.getElementById('year-count').value);
    const container = document.getElementById('data-fields');
    container.innerHTML = '';
    
    for (let i = 0; i < count; i++) {
        const fieldGroup = document.createElement('div');
        fieldGroup.className = 'form-group';
        fieldGroup.innerHTML = `
            <h3>Year ${i+1}</h3>
            <div class="input-row">
                <div>
                    <label for="year-${i}">Year:</label>
                    <input type="number" id="year-${i}" name="year[]" required>
                </div>
                <div>
                    <label for="gdp-${i}">GDP (Billion USD):</label>
                    <input type="number" id="gdp-${i}" name="gdp[]" step="0.01" required>
                </div>
            </div>
        `;
        container.appendChild(fieldGroup);
    }
}

// Multi-country comparison
async function runComparison() {
    const select = document.getElementById('country-select');
    const selected = Array.from(select.selectedOptions).map(opt => opt.value);
    
    if (selected.length === 0) {
        alert('Please select at least one country');
        return;
    }
    
    try {
        const response = await fetch('/api/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ countries: selected })
        });
        
        const data = await response.json();
        displayComparisonResults(data);
    } catch (error) {
        console.error('Comparison failed:', error);
        alert('Failed to compare countries');
    }
}

function displayComparisonResults(data) {
    const container = document.getElementById('comparison-results');
    let html = '<div class="comparison-grid">';
    
    data.forEach(country => {
        html += `
            <div class="country-card">
                <h3>${country.name}</h3>
                <p>Mean GDP: ${country.data.mean.toFixed(2)}B USD</p>
                <p>Growth Rate: ${country.data.growth_rates.slice(-1)[0].rate.toFixed(2)}%</p>
                <p>Economic Health: <span class="grade-${country.data.economic_score.toLowerCase()}">
                    ${country.data.economic_score}
                </span></p>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
    
    // Initialize Plotly comparison chart
    renderComparisonChart(data);
}

function renderComparisonChart(data) {
    const plotData = data.map(country => ({
        x: country.data.years,
        y: country.data.gdp_values,
        type: 'scatter',
        mode: 'lines+markers',
        name: country.name
    }));
    
    Plotly.newPlot('comparison-chart', plotData, {
        title: 'GDP Comparison',
        xaxis: { title: 'Year' },
        yaxis: { title: 'GDP (Billion USD)' }
    });
}

// Initialize form on load
document.addEventListener('DOMContentLoaded', () => {
    updateFields();
    
    // Set default values for demo purposes
    const currentYear = new Date().getFullYear();
    for (let i = 0; i < 5; i++) {
        const yearInput = document.getElementById(`year-${i}`);
        const gdpInput = document.getElementById(`gdp-${i}`);
        if (yearInput) yearInput.value = currentYear - 4 + i;
        if (gdpInput) gdpInput.value = (1000 + i * 150).toFixed(2);
    }
});