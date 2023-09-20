
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

from kivy.app import App
from kivy.app import App
from kivy.core.window import Window
print("window size initial", Window.size)

from custom_map_view import CustomMapView

class MapViewApp(App):

    def build(self):
        mapview = CustomMapView(zoom=17, lat=54.19216979440788, lon=9.105268718909326)

        return mapview

if __name__ == '__main__':
    MapViewApp().run()
