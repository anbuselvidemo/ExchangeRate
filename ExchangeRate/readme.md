Python script that uses the [twelvedata](https://twelvedata.com) api to fetch the exchange rates of the selected Base and Quote currencies for the past 30 days and outputs the best, worst and average exchange rates.

**Setup Instructions:**

Copy the code to a folder and Open a terminal, navigate to the directory containing your Dockerfile and Python script, and run the following command to build the Docker image:

`docker build -t exchange-rate-analysis .`

Once the Docker image is built, you can run it as a Docker container :

`docker run exchange-rate-analysis `

**Parameters:**

The parameters are defined in the .env file as below. This ensures that sensitive information like API keys are not hard-coded into the program and can be easily managed.


`BASE_SYMBOL = "EUR"

QUOTE_SYMBOL = "USD"

INTERVAL = "1day"

OUTPUT_SIZE = "30"

API_KEY = "demo"

URL = "https://api.twelvedata.com/time_series"`

**API_KEY** needs to be replaced to work with other currencies. The _demo_ **API_KEY** only supports exchange rates for **EUR** vs **USD**.
Additional parameters can be used such as timezone, by default Australia/Sydney timezone has been used. 


**Fetching Exchange Rate** 

The _fetch_rates()_ function uses the requests library in Python to make an HTTP GET request to the API endpoint while passing the constructed parameters as query parameters in the request URL. It also performs simple error validation to ensure the request is successful.
	`Url:  https://api.twelvedata.com/time_series
             Parameters: {'symbol': 'EUR/USD',
                                  'interval': '1day',
                                  'outputsize': '3', 
                                  ‘'apikey': 'demo'}`

**Sample Response :**

`{
	"meta": {
		"symbol": "EUR/USD",
		"interval": "1day",
		"currency_base": "Euro",
		"currency_quote": "US Dollar",
		"type": "Physical Currency"
	},
	"values": [
		{
			"datetime": "2024-04-15",
			"open": "1.06490",
			"high": "1.06650",
			"low": "1.06310",
			"close": "1.06350"
		},
		{
			"datetime": "2024-04-12",
			"open": "1.07300",
			"high": "1.07300",
			"low": "1.06225",
			"close": "1.06400"
		},
		{
			"datetime": "2024-04-11",
			"open": "1.07435",
			"high": "1.07570",
			"low": "1.06990",
			"close": "1.07265"
		}
	],
	"status": "ok"
}`

Preprocessing Data

The _preprocess_rates()_ function will perform some basic validation of json data such as datatype conversion , missing keys, invalid data etc and returns the processed values. 

**Sample Output :**

`[{'datetime': '2024-04-15', 'open': '1.06490', 'high': '1.06650', 'low': '1.06310', 'close': 1.0631}, {'datetime': '2024-04-12', 'open': '1.07300', 'high': '1.07300', 'low': '1.06225', 'close': 1.064}, {'datetime': '2024-04-11', 'open': '1.07435', 'high': '1.07570', 'low': '1.06990', 'close': 1.07265}]`

When the API request fails or returns unexpected data. Error message is logged and exceptions are handled.

**Analyze Data:**

The _analyze_rates()_ function uses the close values for the 30 days interval and determines the best rate, worst rate, and average exchange rate for the period. 

**Tests**

Tests have been added in _test_exchange_rates.py_ to cll individual functions with different input parameters, checking for errors, and verifying the correctness of the output data.


If the API request is successful and data is obtained, then the final output is returned. This includes metadata such as the currencies used, current date and time periodchecked. 

**Sample Output:**

`{
    "date": "2024-04-15",
    "base_currency": "EUR",
    "quote_currency": "USD",
    "period": "30",
    "best_exchange_rate": 1.0947,
    "worst_exchange_rate": 1.0638,
    "average_exchange_rate": 1.0826
}`
# CurrencyExchangeRate
