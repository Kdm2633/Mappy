import pandas as pd
import geopandas as gpd
from pandas import DataFrame, read_csv
import datetime
import folium
import matplotlib.pyplot

from flask import Flask, render_template

app = Flask('app', template_folder='templates', static_folder='static')


@app.route('/')
def hello_world():
    return render_template('map.html')
    #return render_template('index.html')


@app.route('/test')
def homepage():
    return render_template('index.html')


# Refugee Data
refugee_data = pd.read_csv('data/UkraineRefugees.csv')
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
refugee_data = world.merge(refugee_data, how='left', left_on=['name'], right_on=['Name'])
cols = refugee_data.columns[6:]
refugee_data = refugee_data.dropna(subset=cols, how='all')
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 200)
# print(refugee_data)

# Healthcare Facilities Data
healthcare_data = pd.read_csv('data/health_facilities.csv')
ukr_geo = gpd.read_file(
    'data/ukr_geo.json')  #administrative divisions shapefile

print(ukr_geo)
# Mapping
m = folium.Map(
    location=[50.715, 24.213],
    zoom_start=4,
    min_zoom=4,
    max_zoom=7,
    tiles="https://api.mapbox.com/styles/v1/lumii/cl3g4e55100aq14qumgn4whkg/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibHVtaWkiLCJhIjoiY2wzZzN3ZGEyMDVnZjNmcDc3Z3Jodm0wbyJ9.oTc222D0JZekjMQD_1EGYw",
    attr="mapbox")
# folium.GeoJson(data=ukr_map["geometry"]).add_to(m)
# Creating Markers
print("worked 1")
# folium.CircleMarker(location=[50.000, 25.0000], radius=50,
#                     color="#ffffff").add_to(m)
print("worked 2")
folium.Choropleth(
    geo_data=ukr_geo,
    name="choropleth",
    data=healthcare_data,
    columns=["Region", "Health_Facilities"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=.1,
    legend_name="Healthcare Facilities",
).add_to(m)
print("worked 3")

folium.LayerControl().add_to(m)
m.save('./templates/map.html')

# Running comes last
app.run(host='0.0.0.0', port=8080, debug=True)
