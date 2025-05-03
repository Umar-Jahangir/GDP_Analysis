from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pdfkit
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

app = Flask(__name__)

# Helper function for safe mode calculation
def safe_mode(data):
    try:
        mode_result = stats.mode(data, keepdims=True)
        if len(mode_result.mode) > 0 and mode_result.count[0] > 1:
            return float(mode_result.mode[0])
        return None
    except:
        return None

# Main analysis function
def analyze_gdp(years, gdp_values):
    years = np.array(years)
    gdp = np.array(gdp_values)
    
    # Validate data isn't empty
    if len(gdp) == 0:
        return {
            'error': 'No GDP data provided',
            'mean': 0,
            'median': 0,
            'mode': None,
            'range': 0,
            'std_dev': 0,
            'cv': 0,
            'growth_rates': []
        }
    
    # Calculate statistics safely
    results = {
        'mean': float(np.mean(gdp)) if len(gdp) > 0 else 0,
        'median': float(np.median(gdp)) if len(gdp) > 0 else 0,
        'mode': safe_mode(gdp),
        'range': float(np.ptp(gdp)) if len(gdp) > 0 else 0,
        'std_dev': float(np.std(gdp, ddof=1)) if len(gdp) > 1 else 0,
        'cv': (np.std(gdp, ddof=1)/np.mean(gdp)*100) if len(gdp) > 1 and np.mean(gdp) != 0 else 0,
        'growth_rates': [
            {'years': f"{years[i]}–{years[i+1]}", 
             'rate': float((gdp[i+1]-gdp[i])/gdp[i]*100)}
            for i in range(len(gdp)-1)
        ] if len(gdp) > 1 else []
    }
    return results
    
    # Route for main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        years = request.form.getlist('year[]')
        gdps = request.form.getlist('gdp[]')
        
        if len(years) != len(gdps) or len(years) < 2:
            return render_template('index.html', error="Invalid data input")
            
        try:
            years = [int(y) for y in years]
            gdps = [float(g) for g in gdps]
        except ValueError:
            return render_template('index.html', error="Invalid number format")
        
        return redirect(url_for('results', years=years, gdps=gdps))
    
    return render_template('index.html')

@app.route('/generate-pdf')
def generate_pdf():
    years = request.args.getlist('years', type=int)
    gdps = request.args.getlist('gdps', type=float)
    
    if len(years) != len(gdps) or len(years) == 0:
        return "Error: Invalid data for PDF generation", 400

    if 'error' in stats:
        return stats['error'], 400

    stats = analyze_gdp(years, gdps)
    
    # Generate plot specifically for PDF
    plt.figure(figsize=(8, 4))
    plt.plot(years, gdps, marker='o')
    plt.title('GDP Trend')
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)
    plot_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    # Render HTML
    html = render_template('report_template.html',
                         years=years,
                         gdp_values=gdps,
                         stats=stats,
                         plot_data=plot_base64)

    # PDF config
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    
    try:
        pdf = pdfkit.from_string(html, False, configuration=config)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=gdp_report.pdf'
        return response
    except Exception as e:
        return str(e), 500

# Route for results page
@app.route('/results')
def results():
    years = request.args.getlist('years', type=int)
    gdps = request.args.getlist('gdps', type=float)
    
    if len(years) != len(gdps) or len(years) < 1:
        flash('Please provide valid year/GDP pairs')
        return redirect(url_for('index'))

    # Calculate statistics
    stats = analyze_gdp(years, gdps)
    plot_data = generate_plots(years, gdps)
    
    # Initialize forecast with empty defaults
    forecast_data = {
        'forecast': [],
        'forecast_years': []
    }
    
    # Only generate forecast if enough data exists
    if len(gdps) >= 3:  # Minimum 3 points for ARIMA
        try:
            forecast_values = forecast_gdp(gdps)
            forecast_data['forecast'] = [float(x) for x in forecast_values]
            forecast_data['forecast_years'] = list(range(years[-1]+1, years[-1]+6))
        except Exception as e:
            print(f"Forecast error: {str(e)}")

    return render_template('results.html',
                         years=years,
                         gdp_values=gdps,
                         stats=stats,
                         plot_data=plot_data,
                         **forecast_data)

def generate_plots(years, gdp):
    plt.figure(figsize=(14, 6))
    
    # Line Plot
    plt.subplot(1, 3, 1)
    plt.plot(years, gdp, marker='o', color='blue')
    plt.title('GDP Over Years')
    plt.xlabel('Year')
    plt.ylabel('GDP (Billion USD)')
    
    # Histogram
    plt.subplot(1, 3, 2)
    plt.hist(gdp, bins=5, color='orange', edgecolor='black')
    plt.title('GDP Distribution')
    plt.xlabel('GDP')
    plt.ylabel('Frequency')
    
    # Box Plot
    plt.subplot(1, 3, 3)
    plt.boxplot(gdp, patch_artist=True)
    plt.title('GDP Spread')
    
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)