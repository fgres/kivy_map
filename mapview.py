import geopandas


from kivy.config import Config # full screen. Config.set should be used before importing any other Kivy modules. Ideally, this means setting them right at the start of your main.py script.
# Config.set('graphics', 'fullscreen', 1)
# somehow the value set here gets two times more!!
Config.set('graphics', 'width', 1440)
Config.set('graphics', 'height', 960)
# https://kivy.org/doc/stable/api-kivy.config.html
# print("window size", Window.size) # window.size is (width, height)
from kivy.logger import Logger
# Logger.setLevel(level=2)
Config.set('kivy', 'log_level', 'debug')
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarker
from kivy.app import App
from kivy.graphics import Mesh
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
print("window size initial", Window.size)
from kivy.graphics import Color

class GIS:
    def __init__(self, coords=None):

        self.gdf = geopandas.read_file("/Users/onlinelehretechnik/uniMinijob/GISdata/bestandsgebaeude_export.shp")#.to_crs(epsg=3857)

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

class MapViewApp(App):

    def build_mesh(self, wid, coords):
        vertices = []
        # vertices.extend([720, 480, 0, 0]) # shows where is the center of the widget
        indices = []

        for i, coord in enumerate(coords):
            x, y = gis.coords_to_point(wid, coord[0], coord[1])
            vertices.extend([x, y, 0, 0])
            indices.append(i)
        return Mesh(vertices=vertices, indices=indices)

    def build(self):
        mapview = MapView(zoom=17, lat=54.19216979440788, lon=9.105268718909326)

        wid = Widget(pos=(0, 0), size=Window.size)
        wid.canvas.add(Color(0, 0, 0))
        # print("==== widget size", wid.size)

        gis.set_bbox(mapview.get_bbox())
        m0 = MapMarker(lat=54.19216979440788, lon=9.105268718909326)  # Lille
        print('!!!!', type(gis.coords['lat_min']))
        m1 = MapMarker(lat=gis.bbox['lat_min'], lon=gis.bbox['lon_min'])  
        m2 = MapMarker(lat=gis.bbox['lat_max'], lon=gis.bbox['lon_max'])  
        mapview.add_marker(m0)
        mapview.add_marker(m1)
        mapview.add_marker(m2)
        with wid.canvas:
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
        # print(mapview.get_bbox())

        # mapview.on_touch_down(
            # print(Window.mouse_pos)
            # print(mapview.get_latlon_at(Window.mouse_pos))
        # )

        return mapview

if __name__ == '__main__':
    gis = GIS()
    MapViewApp().run()