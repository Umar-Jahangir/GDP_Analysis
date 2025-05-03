import numpy as np
from scipy import stats

def calculate_economic_score(gdp_data):
    """Calculate economic health score (A+ to D)"""
    cv = (np.std(gdp_data) / np.mean(gdp_data)) * 100
    growth_stability = np.std(np.diff(gdp_data) / np.mean(np.diff(gdp_data)))
    skew = abs(stats.skew(gdp_data))
    
    # Weighted scoring
    score = 100 - (cv*0.4 + growth_stability*0.4 + skew*0.2)
    
    # Convert to letter grade
    if score > 90: return "A+"
    elif score > 80: return "A"
    elif score > 70: return "B+"
    elif score > 60: return "B"
    elif score > 50: return "C+"
    elif score > 40: return "C"
    else: return "D"