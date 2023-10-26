
from kivy.config import Config # full screen. Config.set should be used before importing any other Kivy modules. Ideally, this means setting them right at the start of your main.py script.
Config.set('graphics', 'width', 1440)
Config.set('graphics', 'height', 960)
# https://kivy.org/doc/stable/api-kivy.config.html

from kivy.logger import Logger
# Logger.setLevel(level=2)
Config.set('kivy', 'log_level', 'debug')
# Config.write()

from kivy.app import App
from kivy.core.window import Window
print("window size initial", Window.size)
from kivy.clock import Clock

from custom_map_view import CustomMapView

class MapViewApp(App):

    def build(self):
        mapview = CustomMapView(zoom=17, lat=54.19216979440788, lon=9.105268718909326)
        Clock.schedule_interval(mapview.refresh_shapefile, 0.5) #refresh_shapefile() is called intervally to remove rendering glitchs
        return mapview

if __name__ == '__main__':
    MapViewApp().run()
