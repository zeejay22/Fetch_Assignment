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
   
git clone https://github.com/zeejay22/Fetch_Assignment.git

cd Fetch_Assignment

2. Install dependencies:

pip install -r requirements.txt

## Usage

The utility can be run from the command line with one or more locations:

# Single location
python src/geoloc_util.py "Madison, WI"

# Multiple locations
python src/geoloc_util.py "Madison, WI" "12345" "Chicago, IL"

# Using a custom API key
python src/geoloc_util.py --api-key YOUR_API_KEY "Madison, WI"

### Input Formats
- City and state: "City, ST" (e.g., "Madison, WI")
- ZIP code: "12345"

## Running Tests

To run the integration tests:

pytest tests/

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
