


def multiple_geoplot(gdf, columns, axes, **kargs):
    for i, col in enumerate(columns):
        gdf.plot(column=col, ax=axes[i], **kargs)

    return axes




def convert_to_geojson(shapefile):
    reader = shapefile.Reader(shapefile, encoding='latin-1')
    fields = reader.fields[1:]
    
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", \
        geometry=geom, properties=atr)) 

    # write the GeoJSON file

    geojson = open("pyshp-demo.json", "w")
    geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()

    for feature in municipios['features']:
        geo_id = feature['properties']['id']
        feature['id'] = str(geo_id)