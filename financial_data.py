import pandas as pd


FINANCIAL_DATA = {

    "RELIANCE": {
        "sector": "Conglomerate",
        "revenue_growth": 12.4,
        "operating_margin": 17.8,
        "net_margin": 8.9
    },

    "TCS": {
        "sector": "IT",
        "revenue_growth": 6.8,
        "operating_margin": 26.4,
        "net_margin": 19.2
    },

    "INFY": {
        "sector": "IT",
        "revenue_growth": 4.2,
        "operating_margin": 24.1,
        "net_margin": 18.3
    },

    "HDFCBANK": {
        "sector": "Banking",
        "revenue_growth": 15.1,
        "operating_margin": 31.2,
        "net_margin": 18.7
    },

    "ICICIBANK": {
        "sector": "Banking",
        "revenue_growth": 17.3,
        "operating_margin": 32.1,
        "net_margin": 19.1
    },

    "ITC": {
        "sector": "FMCG",
        "revenue_growth": 8.1,
        "operating_margin": 35.7,
        "net_margin": 27.4
    },

    "HINDUNILVR": {
        "sector": "FMCG",
        "revenue_growth": 5.6,
        "operating_margin": 23.8,
        "net_margin": 17.2
    },

    "MARUTI": {
        "sector": "Automobile",
        "revenue_growth": 12.8,
        "operating_margin": 11.9,
        "net_margin": 8.4
    },

    "SUNPHARMA": {
        "sector": "Pharma",
        "revenue_growth": 10.7,
        "operating_margin": 26.8,
        "net_margin": 20.1
    },

    "BHARTIARTL": {
        "sector": "Telecom",
        "revenue_growth": 13.5,
        "operating_margin": 51.4,
        "net_margin": 11.7
    }
}


def get_metrics():

    rows = []

    for company, metrics in FINANCIAL_DATA.items():

        rows.append({
            "Company": company,
            "Sector": metrics["sector"],
            "Revenue Growth (%)": metrics["revenue_growth"],
            "Operating Margin (%)": metrics["operating_margin"],
            "Net Margin (%)": metrics["net_margin"]
        })

    return pd.DataFrame(rows)
