# Geolocation Utility

A command-line utility that fetches location information using the OpenWeather Geocoding API.

## Features

- Lookup location information by US zip code
- Lookup location information by city and state combination
- Handle multiple locations in a single request
- Error handling for invalid inputs
- Integration tests

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/geolocation-utility.git
cd geolocation-utility
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The utility can be run from the command line with one or more locations:

```bash
# Single location
python src/geoloc_util.py "Madison, WI"

# Multiple locations
python src/geoloc_util.py "Madison, WI" "12345" "Chicago, IL"

# Using a custom API key
python src/geoloc_util.py --api-key YOUR_API_KEY "Madison, WI"
```

### Input Formats
- City and state: "City, ST" (e.g., "Madison, WI")
- ZIP code: "12345"

## Running Tests

To run the integration tests:

```bash
pytest tests/
```

The tests use the default API key. To use a different key, set the environment variable:

```bash
export OPENWEATHER_API_KEY=your_api_key
pytest tests/
```

## Requirements

- Python 3.7+
- requests
- pytest (for testing)

## Error Handling

The utility handles various error cases:
- Invalid ZIP codes
- Non-existent city/state combinations
- Malformed inputs
- API errors

Each error is reported with the specific location that caused it, allowing other valid locations in the same request to be processed.
