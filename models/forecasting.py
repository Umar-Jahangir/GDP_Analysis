import numpy as np
from statsmodels.tsa.arima.model import ARIMA

def forecast_gdp(gdp_series, years=5):
    """Forecast GDP for next N years using ARIMA"""
    try:
        model = ARIMA(gdp_series, order=(1,1,1)).fit()
        forecast = model.forecast(steps=years)
        return forecast.tolist()
    except:
        # Fallback to simple linear regression if ARIMA fails
        x = np.arange(len(gdp_series))
        coeff = np.polyfit(x, gdp_series, 1)
        return [np.polyval(coeff, len(gdp_series)+i) for i in range(1, years+1)]