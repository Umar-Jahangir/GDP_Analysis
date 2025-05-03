# GDP_Analysis

# GDP Analysis Tool

A web application for analyzing GDP statistics with:
- Automated calculations (mean, growth rates, etc.)
- Interactive visualizations
- PDF report generation

## Technologies
- Python (Flask backend)
- HTML/CSS/JS (Frontend)
- NumPy/SciPy (Statistics)


# 📊 GDP Analysis Tool

A Flask web application for analyzing GDP statistics with automated calculations, visualizations, and PDF report generation.

![GDP Analysis Screenshot](https://via.placeholder.com/800x400?text=GDP+Analysis+Tool+Screenshot)

## 🚀 Features
- Statistical analysis (mean, median, growth rates)
- Interactive charts (trends, distributions)
- PDF report generation
- Multi-country comparison

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- [wkhtmltopdf](https://wkhtmltopdf.org/) (for PDF generation)

### Setup
```bash
# Clone repository
git clone https://github.com/Umar-Jahangir/GDP_Analysis.git
cd GDP_Analysis

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Flask development server
python app.py