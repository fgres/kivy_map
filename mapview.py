import geopandas


from kivy.config import Config # full screen. Config.set should be used before importing any other Kivy modules. Ideally, this means setting them right at the start of your main.py script.
# Config.set('graphics', 'fullscreen', 1)
# somehow the value set here gets two times more!!
Config.set('graphics', 'width', 720)
Config.set('graphics', 'height', 480)
# https://kivy.org/doc/stable/api-kivy.config.html
# print("window size", Window.size) # window.size is (width, height)

from kivy_garden.mapview import MapView
from kivy.app import App
from kivy.graphics import Mesh
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
print("window size initial", Window.size)
from kivy.graphics import Color

class ROI:
    def __init__(self):
        self.lat_max = 54.1962362 # 7207409  # northernmost latitude
        self.lat_min = 54.1884733 # 7205932  # southernmost latitude
        self.lat_diff = self.lat_max - self.lat_min
        self.lon_max = 9.1091775 # 1014029  # easternmost longitude
        self.lon_min = 9.0995835 # 1012961  # westernmost longitude
        self.lon_diff = self.lon_max - self.lon_min

class MapViewApp(App):
    def coords_to_point(self, coord, wid):
        #longtitude 9 something
        x = (coord[0] - roi.lon_min) * wid.size[0] / roi.lon_diff
        
        #latitude 54 something
        y = (coord[1] - roi.lat_min) * wid.size[1] / roi.lat_diff
        
        return x, y
    def build_mesh(self, wid, coords):
        vertices = []
        # vertices.extend([720, 480, 0, 0]) # shows where is the center of the widget
        indices = []

        for i, coord in enumerate(coords):
            x, y = self.coords_to_point(coord, wid)
            vertices.extend([x, y, 0, 0])
            indices.append(i)
        return Mesh(vertices=vertices, indices=indices)
        
    def build(self):
        mapview = MapView(zoom=16, lat=54.19216979440788, lon=9.105268718909326)

        wid = Widget(pos=(0, 0), size=Window.size)
        wid.canvas.add(Color(0, 0, 0))
        # print("==== widget size", wid.size)
        gdf = geopandas.read_file("bestandsgebaeude_export.shp")
        with wid.canvas:
        # geom = gdf.loc[0, 'geometry']
            for polygon in gdf['geometry']:
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
    roi = ROI()
    MapViewApp().run()