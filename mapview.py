
from kivy.config import Config # full screen. Config.set should be used before importing any other Kivy modules. Ideally, this means setting them right at the start of your main.py script.
# Config.set('graphics', 'fullscreen', 1)
# somehow the value set here gets two times more!!
Config.set('graphics', 'width', 1440)
Config.set('graphics', 'height', 960)
# https://kivy.org/doc/stable/api-kivy.config.html

# from kivy.logger import Logger, LO.G_LEVELS, logger_config_update
from kivy.logger import Logger
# Logger.setLevel(level=2)
Config.set('kivy', 'log_level', 'debug')
# Config.write()
from kivy_garden.mapview import MapView, MapMarker, MapLayer
from kivy.graphics import Mesh

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
print("window size initial", Window.size)
from kivy.graphics import Color

from GIS import GIS
from custom_map_view import CustomMapView

class MapViewApp(App):

    def initialize_gis(self, bbox):
        gis.lat_min, gis.lon_min, gis.lat_max, gis.lon_max = bbox # get_bbox() returns (54.19185593800895, 9.104732277106336, 54.19248364842369, 9.105805160712293)
        gis.lat_diff = gis.lat_max - gis.lat_min
        gis.lon_diff = gis.lon_max - gis.lon_min

    def add_map_makers(self, mapview):
        m0 = MapMarker(lat=54.19216979440788, lon=9.105268718909326)  # Lille
        m1 = MapMarker(lat=gis.lat_min, lon=gis.lon_min)
        m2 = MapMarker(lat=gis.lat_max, lon=gis.lon_max)
        mapview.add_marker(m0)
        mapview.add_marker(m1)
        mapview.add_marker(m2)
        return mapview

    def build_mesh(self, wid, coords):
        vertices = []
        # vertices.extend([720, 480, 0, 0]) # shows where is the center of the widget
        indices = []

        for i, coord in enumerate(coords):
            x, y = gis.coords_to_point(coord, wid)
            vertices.extend([x, y, 0, 0])
            indices.append(i)

        self.mesh = Mesh(vertices=vertices, indices=indices)
        self.mesh.mode = 'line_strip' # 'points', 'line_strip', 'line_loop', 'lines', 'triangle_strip', 'triangle_fan'

    def render_mesh(self, ):
        return

    def build(self):
        mapview = CustomMapView(zoom=17, lat=54.19216979440788, lon=9.105268718909326)

        self.initialize_gis(mapview.get_bbox())
        mapview = self.add_map_makers(mapview)

        wid = Widget(pos=(0, 0), size=Window.size)
        wid.canvas.add(Color(0, 0, 0))

        with wid.canvas:
        # geom = gdf.loc[0, 'geometry']
            for polygon in gis.gdf['geometry']:
                self.build_mesh(wid, polygon.exterior.coords)

        layout = BoxLayout(size_hint=(1, None), height=50)
        mapview.add_widget(wid)
        mapview.add_widget(layout)

        return mapview

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()
    SAMPLE_SHAPEFILE_PATH = os.environ['SAMPLE_SHAPEFILE_PATH'] 
    gis = GIS(SAMPLE_SHAPEFILE_PATH)
    MapViewApp().run()
