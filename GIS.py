import geopandas
from kivy.core.window import Window
import os
from dotenv import load_dotenv
load_dotenv()

class GIS:
    def __init__(self, coords=None):
        SAMPLE_SHAPEFILE_PATH = os.environ['SAMPLE_SHAPEFILE_PATH'] 
        self.gdf = geopandas.read_file(SAMPLE_SHAPEFILE_PATH)#.to_crs(epsg=3857)

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

    def coords_to_point(self, wid, lon, lat):
        target_size = 100
        #longtitude 9 something
        x = (lon - self.bbox['lon_min']) * target_size / (self.bbox['lon_max'] - self.bbox['lon_min']) + (wid.size[0] - target_size)/2

        #latitude 54 something
        y = (lat - self.bbox['lat_min']) * target_size / (self.bbox['lat_max'] - self.bbox['lat_min']) + (wid.size[1] - target_size)/2

        # print("translated points to", x, y)
        return x, y