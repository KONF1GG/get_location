from geopy.geocoders import Nominatim

def get_location(address):
    geolocator = Nominatim(user_agent='MyGeaopyUA')
    location = geolocator.geocode(address)

    if location:
        if location.raw.get('class') == 'building':
            return location.latitude, location.longitude
        else:
            print('It is not a building')
            return None
    else:
        print('location is empty on NominAPI')
        return None

# address = "Агаповский  Агаповка Дальняя 10"
# loc = get_location(address)
# if loc:
#     latitude, longitude = get_location(address)
#     print(f"Latitude: {latitude}, Longitude: {longitude}")