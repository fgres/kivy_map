import geopandas
from kivy.core.window import Window

class GIS:
    def __init__(self, shp):

        self.gdf = geopandas.read_file(shp)#.to_crs(epsg=3857)

        self.lat_max = 54.1962362 # 7207409  # northernmost latitude
        self.lat_min = 54.1884733 # 7205932  # southernmost latitude
        self.lat_diff = self.lat_max - self.lat_min
        self.lon_max = 9.1091775 # 1014029  # easternmost longitude
        self.lon_min = 9.0995835 # 1012961  # westernmost longitude
        self.lon_diff = self.lon_max - self.lon_min

    def coords_to_point(self, coord, wid):
        target_size = 100
        x = (coord[0] - self.lon_min) * target_size / self.lon_diff + (wid.size[0] - target_size)/2

        y = (coord[1] - self.lat_min) * target_size / self.lat_diff + (wid.size[1] - target_size)/2

        return x, y

    # def set_bbox(self, coords):

    #     self.lat_min = coords[0]
    #     self.lon_min = coords[1]
    #     self.lat_max = coords[2]
    #     self.lon_max = coords[3]

    #     print("updated GIS bounding box with coords:", self.coords)