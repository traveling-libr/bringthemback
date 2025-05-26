import geopandas as gpd
import json

"""
GEO DATA
"""
elslpath = 'https://raw.githubusercontent.com/traveling-libr/bringThemBack/refs/heads/main/data/geoBoundaries-SLV-ADM0.geojson'
elsl_geo = gpd.read_file(elslpath)

# Prepare geographic data
# Load as JSON object
elsl_to_json = elsl_geo.to_json()
elsl_geojson = json.loads(elsl_to_json)

elsl_gdf = gpd.GeoDataFrame.from_features(elsl_geojson['features'])