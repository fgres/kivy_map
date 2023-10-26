import geopandas
from kivy.core.window import Window
import os
from dotenv import load_dotenv
load_dotenv()

from kivy.core.window import Window
""" reference for shapefile column
columns = {
        'Kataster_C': 'string',  # Code
        'Kataster_S': 'string',  # Straße
        'Kataster_H': 'string',  # Hausnummer
        # 'Kataster_B': 'float',  # Baujahr
        'Kataster_6': 'float',  # Nettogrundfläche
        'Kataster13': 'float',  # spez. Wärmeverbrauch
        'Kataster15': 'float',  # spez. Stromverbrauch
        'Kataster_E': 'string',  # Energieträger
        'Kataster_A': 'string',  # Gebäudetyp
        'Kataster_W' : 'int'
}
"""

crs = "EPSG:3857"

def read_shapefile(file, layer=None, columns=None):
    df = geopandas.read_file(file, layer=layer).to_crs(crs=crs)
    if columns:
        df = df.astype(columns)
        return df.loc[:, ['geometry', *columns.keys()]]
    return df

class GIS:
    def __init__(self, coords=None):
        self.isInitialRender = True 
        SAMPLE_SHAPEFILE_PATH = os.environ['SAMPLE_SHAPEFILE_PATH'] 
        

        self.gdf = geopandas.read_file(SAMPLE_SHAPEFILE_PATH)#.astype(columns)#.set_index('Kataster_C').to_crs(crs=crs)

        # if no coords provided, take polygons max extents as frame
        if coords is None:
            self.coords = {
                'lon_min' : self.gdf.bounds['minx'].min(), # 9.1091775 # 1014029  # easternmost longitude
                'lon_max' : self.gdf.bounds['maxx'].max(), # 9.0995835 # 1012961  # westernmost longitude
                'lat_min' : self.gdf.bounds['miny'].min(), # 54.1962362 # 7207409  # northermost latitude
                'lat_max' : self.gdf.bounds['maxy'].max() # 54.1884733 # 7205932  # southernmost latitude,
            }

        else:
            self.coords = {
                'lon_min' : coords[0],
                'lon_max' : coords[1],
                'lat_min' : coords[2],
                'lat_max' : coords[3]
            }

        print("initialized GIS class with coords:", self.coords)

    def set_bbox(self, coords):
        self.bbox = {
            'lat_min' : coords[0],
            'lon_min' : coords[1],
            'lat_max' : coords[2],
            'lon_max' : coords[3]
        }

        # print("updated GIS bounding box with coords:", self.coords)
    def set_widget(self, widget):
        self.widget = widget

    def coords_to_point(self, lon, lat):
        # at the booting of the app, the resolution of the window is not set as it is defined at mapview.py. self.isInitialRender is used to differentiate the calculation of shapefile rendering 
        if self.isInitialRender == True:
            target_display_size = [100, 100]
        else:
            target_display_size = Window.size
        #longtitude 9 something
        if self.bbox['lon_max'] == self.bbox['lon_min']: # sometimes lon_max and lon_min is both 180 so here it assumes that it means 360 instead of 0
            lon_diff = 360
        else:
            lon_diff = self.bbox['lon_max'] - self.bbox['lon_min']
        x = (lon - self.bbox['lon_min']) * target_display_size[0] / (lon_diff) + (self.widget.size[0] - target_display_size[0])/2

        #latitude 54 something
        y = (lat - self.bbox['lat_min']) * target_display_size[1] / (self.bbox['lat_max'] - self.bbox['lat_min']) + (self.widget.size[1] - target_display_size[1])/2

        # print("translated points to", x, y)
        return x, y

gis = GIS()