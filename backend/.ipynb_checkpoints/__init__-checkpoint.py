
import requests
import pandas as pd


def cargo_price_calculator(height, depth, length, weight, kg_price=3500, m3_price=3000):
    if height <= 0 or depth <= 0 or length <= 0:
        raise ValueError("Hemjee buruu")

    if weight <= 0:
        raise ValueError("Jin buruu")

    volume = (height * depth * length) / 5000
    chargeable_weight = max(volume, weight)

    return chargeable_weight * kg_price


def alt_mungunii_une(start_date, end_date):
    url = "https://www.mongolbank.mn/mn/gold-and-silver-price/data"

    params = {
        "startDate": start_date,
        "endDate": end_date
    }

    response = requests.post(url, params=params)
    response.raise_for_status()

    result = response.json()

    if "data" not in result:
        print("data oldsongui")
        return pd.DataFrame()

    df = pd.DataFrame(result["data"])
    return df

    