import json

def load_geojson(path):

    with open(path, "r") as fp:
        geojson = json.load(fp)
        
    for feature in geojson['features']:
        geo_id = feature['properties']['id']
        feature['id'] = geo_id

    return geojson