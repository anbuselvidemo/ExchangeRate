import requests
import json
from datetime import datetime
from statistics import mean
import os
from dotenv import load_dotenv,dotenv_values
load_dotenv()

# Loading values from environment variables
API_KEY = os.getenv("API_KEY")
URL = os.getenv("URL")
BASE_SYMBOL = os.getenv("BASE_SYMBOL")
QUOTE_SYMBOL = os.getenv("QUOTE_SYMBOL")
INTERVAL = os.getenv("INTERVAL")
OUTPUT_SIZE = os.getenv("OUTPUT_SIZE")
SYMBOL = str(BASE_SYMBOL) + "/" + str(QUOTE_SYMBOL)

# Function to fetch data from the API
def fetch_rates():
    url = os.getenv('URL')
    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "outputsize": OUTPUT_SIZE,
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        #print(f"Sample response :{response.json()}")
        return response.json()
    else:
        print("Error fetching data from API.")
        return None

# Function to cleanup the data with basic preprocessing
def preprocess_rates(data):
    processed_values = []
    if not data:
        return []  # Return an empty list if input data is empty
    if "values" not in data:
        print("Data format error: 'values' key not found.")
        return processed_values
    values = data["values"]
    # Filter out entries with missing values or non-numeric "close" values
    for entry in values:
        # The twelvedata api provides daily open, intraday high, intraday low and close rates, using close as the standard practice
        if all(key in entry for key in ["datetime", "open", "high", "low", "close"]):
            close_value = entry.get("close")
            try:
                entry["close"] = float(close_value)
                processed_values.append(entry)
            except ValueError:
                print(f"Ignoring entry with non-numeric 'close' value: {entry}")
                continue  # Skip to the next entry if 'close' value is non-numeric
    #print(f"Sample values:{processed_values}")
    return processed_values
# Function to perform data analysis
def analyze_rates(data):
    if data:
        # Extracting exchange rates
        exchange_rates = [entry["close"] for entry in data]
        # Finding best and worst exchange rates
        best_rate = max(exchange_rates)
        worst_rate = min(exchange_rates)
        # Calculating average exchange rate for the month
        average_rate = round(mean(exchange_rates),4)
        return best_rate, worst_rate, average_rate
    else:
        print("No data available for analysis.")
        return None, None, None

# Main function
def main():
    # Fetch data from API
    raw_data = fetch_rates()
    # Preprocess the data
    processed_data = preprocess_rates(raw_data)
    # Perform data analysis
    best_rate, worst_rate , average_rate = analyze_rates(processed_data)

    if best_rate and worst_rate  and average_rate:
        # Output the results in JSON format
        output_data = {
            "date": datetime.today().strftime('%Y-%m-%d'),
            "base_currency": BASE_SYMBOL,
            "quote_currency": QUOTE_SYMBOL,
            "period": OUTPUT_SIZE,
            "best_exchange_rate": best_rate,
            "worst_exchange_rate": worst_rate,
            "average_exchange_rate": average_rate
        }
        print(json.dumps(output_data, indent=4))

if __name__ == "__main__":
    main()
