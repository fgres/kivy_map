import geopandas
import os


from kivy.config import Config # full screen. Config.set should be used before importing any other Kivy modules. Ideally, this means setting them right at the start of your main.py script.
# Config.set('graphics', 'fullscreen', 1)
# somehow the value set here gets two times more!!
Config.set('graphics', 'width', 1440)
Config.set('graphics', 'height', 960)
# https://kivy.org/doc/stable/api-kivy.config.html

# from kivy.logger import Logger, LOG_LEVELS, logger_config_update
# Logger.setLevel(level=2)
Config.set('kivy', 'log_level', 'error')
# Config.write()
from kivy_garden.mapview import MapView, MapMarker
from kivy.app import App
from kivy.graphics import Mesh
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
print("window size initial", Window.size)
from kivy.graphics import Color



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
class MapViewApp(App):

    def build_mesh(self, wid, coords):
        vertices = []
        # vertices.extend([720, 480, 0, 0]) # shows where is the center of the widget
        indices = []

        for i, coord in enumerate(coords):
            x, y = gis.coords_to_point(coord, wid)
            vertices.extend([x, y, 0, 0])
            indices.append(i)
        return Mesh(vertices=vertices, indices=indices)

    def build(self):
        mapview = MapView(zoom=17, lat=54.19216979440788, lon=9.105268718909326)

        print(mapview.get_bbox())

        gis.lat_min, gis.lon_min, gis.lat_max, gis.lon_max = mapview.get_bbox()
        gis.lat_diff = gis.lat_max - gis.lat_min
        gis.lon_diff = gis.lon_max - gis.lon_min

        m0 = MapMarker(lat=54.19216979440788, lon=9.105268718909326)  # Lille
        m1 = MapMarker(lat=gis.lat_min, lon=gis.lon_min)
        m2 = MapMarker(lat=gis.lat_max, lon=gis.lon_max)
        mapview.add_marker(m0)
        mapview.add_marker(m1)
        mapview.add_marker(m2)

        print("***", mapview.get_window_matrix())
        wid = Widget(pos=(0, 0), size=Window.size)
        wid.canvas.add(Color(0, 0, 0))
        # print("==== widget size", wid.size)

        with wid.canvas:
        # geom = gdf.loc[0, 'geometry']
            for polygon in gis.gdf['geometry']:
                self.mesh = self.build_mesh(wid, polygon.exterior.coords)
                self.mesh.mode = 'line_strip' # 'points', 'line_strip', 'line_loop', 'lines', 'triangle_strip', 'triangle_fan'

        layout = BoxLayout(size_hint=(1, None), height=50)
        # for mode in ('triangle_fan', 'points', 'line_strip', 'line_loop', 'lines',
        #         'triangle_strip'):
        #     button = Button(text=mode)
        #     button.bind(on_release=partial(self.change_mode, mode))
        #     layout.add_widget(button)

        # root = BoxLayout(orientation='vertical')
        mapview.add_widget(wid)
        mapview.add_widget(layout)

        return mapview

if __name__ == '__main__':
    SAMPLE_SHAPEFILE_PATH = os.environ['SAMPLE_SHAPEFILE_PATH']
    gis = GIS(SAMPLE_SHAPEFILE_PATH)
    MapViewApp().run()
