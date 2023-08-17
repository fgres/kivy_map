'''
Mesh test
=========

This demonstrates the use of a mesh mode to distort an image. You should see
a line of buttons across the bottom of a canvas. Pressing them displays
the mesh, a small circle of points, with different mesh.mode settings.
'''
import geopandas

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Mesh
from kivy.core.window import Window
from functools import partial
from math import cos, sin, pi

class ROI:
    def __init__(self):
        self.lon_max = 9.1091775 # 1014029  # easternmost longitude
        self.lon_min = 9.0995835 # 1012961  # westernmost longitude
        self.lon_diff = self.lon_max - self.lon_min
        self.lat_max = 54.1962362 # 7207409  # northermost latitude
        self.lat_min = 54.1884733 # 7205932
        self.lat_diff = self.lat_max - self.lat_min

class MeshTestApp(App):

    def coords_to_point(self, coord, wid):
        x = (coord[0] - roi.lon_min) * (roi.lon_max) * Window.size[0]
        y = (coord[1] - roi.lat_min) * (roi.lat_max) * Window.size[1]
        return x, y

    def change_mode(self, mode, *largs):
        self.mesh.mode = mode

    def build_mesh(self, wid, coords):
        """ returns a Mesh of a rough circle. """
        vertices = []
        indices = []

        for i, coord in enumerate(coords):
            x, y = self.coords_to_point(coord, wid)
            vertices.extend([x, y, 0, 0])
            # indices.append(i)
            print(x,y)
        return Mesh(vertices=vertices, indices=indices)

    def build(self):
        wid = Widget()
        gdf = geopandas.read_file("/home/dunland/github/qScope/data/GIS/Shapefiles/bestandsgebaeude_export.shp")
        with wid.canvas:
        # geom = gdf.loc[0, 'geometry']
            for polygon in gdf['geometry']:
                self.mesh = self.build_mesh(wid, polygon.exterior.coords)
                # self.mesh.mode = mode

        layout = BoxLayout(size_hint=(1, None), height=50)
        for mode in ('triangle_fan', 'points', 'line_strip', 'line_loop', 'lines',
                'triangle_strip'):
            button = Button(text=mode)
            button.bind(on_release=partial(self.change_mode, mode))
            layout.add_widget(button)

        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(layout)

        return root


if __name__ == '__main__':
    roi = ROI()
    MeshTestApp().run()