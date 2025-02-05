import pytest
from src.geoloc_util import GeoLocationUtility
import os

API_KEY = os.getenv('OPENWEATHER_API_KEY', 'f897a99d971b5eef57be6fafa0d83239')

@pytest.fixture
def geo_util():
    return GeoLocationUtility(API_KEY)

def test_zip_code_lookup(geo_util):
    """Test looking up location by zip code."""
    result = geo_util.get_location_info('10001')
    
    assert result['input'] == '10001'
    assert result['type'] == 'zip'
    assert result['country'] == 'US'
    assert isinstance(result['latitude'], float)
    assert isinstance(result['longitude'], float)
    assert result['name']  # Location name should exist

def test_city_state_lookup(geo_util):
    """Test looking up location by city, state combination."""
    result = geo_util.get_location_info('Madison, WI')
    
    assert result['input'] == 'Madison, WI'
    assert result['type'] == 'city_state'
    assert result['country'] == 'US'
    assert result['state'] == 'Wisconsin'
    assert isinstance(result['latitude'], float)
    assert isinstance(result['longitude'], float)
    assert result['name'] == 'Madison'

def test_multiple_locations(geo_util):
    """Test looking up multiple locations at once."""
    locations = ['Madison, WI', '10001', 'Chicago, IL']
    results = geo_util.get_multiple_locations(locations)
    
    assert len(results) == 3
    assert all('error' not in result for result in results)
    assert all(isinstance(result['latitude'], float) for result in results)
    assert all(isinstance(result['longitude'], float) for result in results)

def test_invalid_zip_code(geo_util):
    """Test handling of invalid zip code."""
    result = geo_util.get_location_info('00000')
    assert 'error' in result

def test_invalid_city_state(geo_util):
    """Test handling of invalid city/state combination."""
    result = geo_util.get_location_info('NonExistent, XX')
    assert 'error' in result

def test_malformed_input(geo_util):
    """Test handling of malformed input."""
    result = geo_util.get_location_info('InvalidInput')
    assert 'error' in result