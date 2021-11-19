from math import radians, cos, sin, asin, sqrt
import pandas as pd


# https://medium.com/analytics-vidhya/finding-nearest-pair-of-latitude-and-longitude-match-using-python-ce50d62af546
def dist(lat1, long1, lat2, long2):
    # Calculate the great circle distance between two points on the earth (specified in decimal degrees)
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [float(lat1), float(long1), float(lat2), float(long2)])
    # haversine formula
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km



def find_twenty_closest(user_lat_long, properties):
    closest_twenty_properties = []
    lat1 = user_lat_long["lat"]
    lon1 = user_lat_long["lon"]

    all_properties_df = pd.DataFrame(columns=["pk", "distance"])

    #find the distance of all the properties
    for count, property in enumerate(properties):
        lat2 = property.lat
        lon2 = property.lon
        distance = dist(lat1, lon1, lat2, lon2)
        all_properties_df.loc[count, "pk"] = property.pk
        all_properties_df.loc[count, "distance"] = distance
    #sort the properties for the closest
    sorted_properties = all_properties_df.sort_values(by="distance", ascending=False).tail(3)
    closest_twenty_properties = sorted_properties["pk"].tolist()

    return closest_twenty_properties