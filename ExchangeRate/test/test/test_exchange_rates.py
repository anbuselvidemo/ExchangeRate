from fetch_exchange_rates import analyze_rates, preprocess_rates


# Test case when data is None
def test_analyze_rates_with_none():
    assert analyze_rates(None) == (None, None, None)

# Test case when data is an empty list
def test_analyze_rates_with_empty_list():
    assert analyze_rates([]) == (None, None, None)

# Test case when data contains numeric exchange rates
def test_analyze_rates_with_valid_data():
    data = [{"close": 1.5}, {"close": 2.5}, {"close": 3.5}]
    assert analyze_rates(data) == (3.5, 1.5, 2.5)


# Test case when data is None
def test_preprocess_rates_with_none():
    assert preprocess_rates(None) == []

# Test case when input data is an empty list
def test_preprocess_rates_with_empty_list():
    assert preprocess_rates({"values": []}) == []

# Test case when data contains both numeric and non-numeric "close" values
def test_preprocess_rates_with_mixed_data():
    data = {
        "values": [
            {"datetime": "2022-01-01", "open": "1.0", "high": "1.1", "low": "0.9", "close": "1.05"},
            {"datetime": "2022-01-01", "open": "1.0", "high": "1.1", "low": "0.9", "close": "missing"},
            {"datetime": "2022-01-03", "open": "1.2", "high": "1.3", "low": "1.1", "close": "1.25"}
        ]
    }
    expected_result = [
        {"datetime": "2022-01-01", "open": "1.0", "high": "1.1", "low": "0.9", "close": 1.05},
        {"datetime": "2022-01-03", "open": "1.2", "high": "1.3", "low": "1.1", "close": 1.25}
    ]
    assert preprocess_rates(data) == expected_result

# Test case when data has missing "close" values
def test_preprocess_data_with_missing_close():
    data = {
        "values": [
            {"datetime": "2022-01-01", "open": "1.0", "high": "1.1", "low": "0.9", "close": "1.05"},
            {"datetime": "2022-01-01", "open": "1.0", "high": "1.1", "low": "0.9"},
            {"datetime": "2022-01-03", "open": "1.2", "high": "1.3", "low": "1.1", "close": "1.25"}
        ]
    }
    expected_result = [
        {"datetime": "2022-01-01", "open": "1.0", "high": "1.1", "low": "0.9", "close": 1.05},
        {"datetime": "2022-01-03", "open": "1.2", "high": "1.3", "low": "1.1", "close": 1.25}
    ]
    assert preprocess_rates(data) == expected_result

# Test case when data has numeric "close" values
def test_preprocess_data_with_valid_data():
    data = {
        "values": [
            {"datetime": "2022-01-01", "open": "1.0", "high": "1.1", "low": "0.9", "close": "1.05"},
            {"datetime": "2022-01-03", "open": "1.2", "high": "1.3", "low": "1.1", "close": "1.25"}
        ]
    }
    expected_result = [
        {"datetime": "2022-01-01", "open": "1.0", "high": "1.1", "low": "0.9", "close": 1.05},
        {"datetime": "2022-01-03", "open": "1.2", "high": "1.3", "low": "1.1", "close": 1.25}
    ]
    assert preprocess_rates(data) == expected_result