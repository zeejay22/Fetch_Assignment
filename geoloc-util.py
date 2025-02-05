import requests
import argparse
from typing import List, Dict
import re

class InputValidationError(Exception):
    """Custom exception for input validation errors."""
    pass

class GeoLocationUtility:
    BASE_URL = "http://api.openweathermap.org/geo/1.0"
    
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _validate_zip_code(self, zip_code: str) -> bool:
        """
        Validate if the input is a valid US zip code.
        Returns True if valid, raises InputValidationError if invalid.
        """
        zip_code = zip_code.strip()
        if not zip_code:
            raise InputValidationError("Zip code cannot be empty")
        if not re.match(r'^\d{5}$', zip_code):
            raise InputValidationError(
                "Invalid zip code format. Must be exactly 5 digits"
            )
        return True

    def _validate_city_state(self, location: str) -> tuple:
        """
        Validate and parse city-state combination.
        Returns (city, state) tuple if valid, raises InputValidationError if invalid.
        """
        if not location or not location.strip():
            raise InputValidationError("Location cannot be empty")
        
        # Split and clean the parts
        parts = [part.strip() for part in location.split(',')]
        
        if len(parts) != 2:
            raise InputValidationError(
                "Invalid city-state format. Must be 'City, ST'"
            )
            
        city, state = parts
        
        if not city:
            raise InputValidationError("City name cannot be empty")
            
        if not state:
            raise InputValidationError("State code cannot be empty")
            
        if len(state) != 2:
            raise InputValidationError(
                "State must be a 2-letter code (e.g., NY, CA)"
            )
            
        # Remove special characters from city name
        city = re.sub(r'[^a-zA-Z\s-]', '', city)
        if not city.strip():
            raise InputValidationError(
                "City name contains invalid characters"
            )
            
        return city, state.upper()

    def _is_zip_code(self, location: str) -> bool:
        """Check if the location string looks like a zip code."""
        return bool(re.match(r'^\s*\d{5}\s*$', location))

    def _get_by_zip(self, zip_code: str) -> Dict:
        """Get location information by zip code."""
        try:
            self._validate_zip_code(zip_code)
            url = f"{self.BASE_URL}/zip"
            params = {
                'zip': f"{zip_code.strip()},US",
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise InputValidationError(f"Zip code {zip_code} not found")
            raise

    def _get_by_city_state(self, location: str) -> Dict:
        """Get location information by city, state combination."""
        city, state = self._validate_city_state(location)
        url = f"{self.BASE_URL}/direct"
        
        params = {
            'q': f"{city},{state},US",
            'limit': 1,
            'appid': self.api_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            raise InputValidationError(
                f"No results found for {city}, {state}"
            )
            
        return data[0]

    def get_location_info(self, location: str) -> Dict:
        """Get location information for a single location."""
        try:
            if self._is_zip_code(location):
                data = self._get_by_zip(location)
                return {
                    'input': location,
                    'name': data.get('name'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'country': data.get('country'),
                    'type': 'zip',
                    'status': 'success'
                }
            else:
                data = self._get_by_city_state(location)
                return {
                    'input': location,
                    'name': data.get('name'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'country': data.get('country'),
                    'state': data.get('state'),
                    'type': 'city_state',
                    'status': 'success'
                }
        except InputValidationError as e:
            return {
                'input': location,
                'error': str(e),
                'status': 'validation_error'
            }
        except Exception as e:
            return {
                'input': location,
                'error': str(e),
                'status': 'error'
            }

    def get_multiple_locations(self, locations: List[str]) -> List[Dict]:
        """Get information for multiple locations."""
        return [self.get_location_info(location) for location in locations]


def main():
    parser = argparse.ArgumentParser(
        description='Geolocation Utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Zip code:
    %(prog)s "12345"
  City and state:
    %(prog)s "New York, NY"
  Multiple locations:
    %(prog)s "Chicago, IL" "90210" "Miami, FL"
        """
    )
    parser.add_argument(
        'locations', 
        nargs='+', 
        help='List of locations (zip codes or city,state combinations)'
    )
    parser.add_argument(
        '--api-key', 
        default='f897a99d971b5eef57be6fafa0d83239',
        help='OpenWeatherMap API key'
    )
    
    args = parser.parse_args()
    
    util = GeoLocationUtility(args.api_key)
    results = util.get_multiple_locations(args.locations)
    
    for result in results:
        print(f"\nLocation: {result['input']}")
        if result['status'] == 'success':
            print(f"Name: {result['name']}")
            print(f"Latitude: {result['latitude']}")
            print(f"Longitude: {result['longitude']}")
            if result.get('state'):
                print(f"State: {result['state']}")
        else:
            print(f"Error: {result['error']}")

if __name__ == '__main__':
    main()