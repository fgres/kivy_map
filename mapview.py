from kivy_garden.mapview import MapView
from kivy.app import App
from kivy.uix.widget import Widget

class MapViewApp(App):
    def build(self):
        mapview = MapView(zoom=18, lat=54.19216979440788, lon=9.105268718909326)
        return mapview

MapViewApp().run()