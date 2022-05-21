import pandas as pd
import geopandas as gpd
from pandas import DataFrame, read_csv
import datetime
import folium


from flask import Flask, render_template
app = Flask('app', template_folder='templates', static_folder='static')

@app.route('/')
def hello_world():
  return render_template('map.html')
  #return render_template('index.html')

@app.route('/test')
def homepage():
 return render_template('index.html')

  
# Data
refugee_data = pd.read_csv('data/UkraineRefugees.csv')

# refugee_data['year'] = pd.DatetimeIndex(refugee_data['Date']).year
# refugee_data['month'] = pd.DatetimeIndex(refugee_data['Date']).month
# refugee_data['day'] = pd.DatetimeIndex(refugee_data['Date']).day

# refugee_list = []
# for x in refugee_data['day']:
#   day = x
    # refugee_list.append(datetime.date(2022,2,day).strftime('%B'))
# refugee_data.head()
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
refugee_data = world.merge(refugee_data, how='left', left_on=['name'], right_on=['Name'])
cols = refugee_data.columns[6:]  
refugee_data = refugee_data.dropna(subset=cols, how='all')
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 200)
print(refugee_data)

# Mapping 
m = folium.Map(location=[50.715, 24.213], zoom_start=5, tiles="https://api.mapbox.com/styles/v1/lumii/cl3g4e55100aq14qumgn4whkg/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibHVtaWkiLCJhIjoiY2wzZzN3ZGEyMDVnZjNmcDc3Z3Jodm0wbyJ9.oTc222D0JZekjMQD_1EGYw", attr="mapbox")



# Running comes last 
app.run(host='0.0.0.0', port=8080, debug=True)

