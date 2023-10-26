from kivy.core.window import Window
from kivy.graphics import Mesh, Color, Rectangle
from kivy.uix.button import Button, Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy_garden.mapview import MapView, MapMarker, MapMarkerPopup

from shapely.geometry import Polygon as spolygon

from GIS import gis

Builder.load_string('''
<ShapefileRenderer>
    canvas:
        Color
            rgba: 0.5,0.5,0.5,0.5
        Rectangle:
            pos: self.center_x, self.center_y
            size: 100, 100
          
<CustomMapView>:
    Label:
        font_size: 45
        background_color: (1,1,1,1)
        canvas.before:
            Color:
                rgba: self.background_color
            Rectangle:
                size: self.size
                pos: self.pos
''')

class ShapefileRenderer(FloatLayout):
    #a widget for shapefile. Shapefile is rendered on a separate widget for easy removal
    pass

class CustomMapView(MapView):
    def __init__(self, *args, **kwargs):
        super(CustomMapView, self).__init__(*args, **kwargs)
        gis.set_bbox(self.get_bbox())
        # self.add_bbox_map_makers()

        self.wid = Widget(pos=(0, 0), size=Window.size)
        self.wid.canvas.add(Color(0, 0, 0))
        gis.set_widget(self.wid)

        self.shapefileRenderer = ShapefileRenderer()
        self.add_widget(self.shapefileRenderer)

        self.render_mesh()
        gis.isInitialRender = False

        self.add_widget(self.wid)
        
        self.add_building_info_marker()

    def add_building_info_marker_basic(self, *arg):
        m0 = MapMarkerPopup(lat=54.19216979440788, lon=9.105268718909326)  # Lille
        m0.add_widget(Button(text="building A"))
        self.add_marker(m0)

    def add_building_info_marker(self):

        for index, building_info in gis.gdf.iterrows():
            P = spolygon(building_info['geometry'].exterior.coords)
            m0 = MapMarkerPopup(lat=P.centroid.y.item(), lon=P.centroid.x.item(), source="./visual_material/red_circle_20px.png")
            label=(Label())
            
            with label.canvas.before:
                Color(0.5, 0.5, 0.5, 1)
                Rectangle(pos=label.pos, size=label.size)

            # text for popup marker for individual building
            label.text = f"\
                {building_info['Kataster_S']} {building_info['Kataster_H']}\
            "
            
            label.text_size=label.size
            label.size=label.texture_size

            # with label.canvas.before:
            #     Color(0.5, 0.5, 0.5, 1)
            #     Rectangle(pos=label.pos, size=label.size)

            m0.add_widget(label)
            self.add_marker(m0)

        # for polygon in gis.gdf['geometry']:
        #     P = spolygon(polygon.exterior.coords)
        #     m0 = MapMarkerPopup(lat=P.centroid.y.item(), lon=P.centroid.x.item(), source="./visual_material/red_circle_20px.png")
        #     m0.add_widget(Button(text="building A"))
        #     self.add_marker(m0)
        

    def add_bbox_map_makers(self):
        m1 = MapMarker(lat=gis.bbox['lat_min'], lon=gis.bbox['lon_min'])  
        m2 = MapMarker(lat=gis.bbox['lat_max'], lon=gis.bbox['lon_max'])  
        self.add_marker(m1)
        self.add_marker(m2)
        
    def build_mesh(self, coords):
        vertices = []
        # vertices.extend([720, 480, 0, 0]) # shows where is the center of the widget
        indices = []

        for i, coord in enumerate(coords):
            x, y = gis.coords_to_point(coord[0], coord[1])
            vertices.extend([x, y, 0, 0])
            indices.append(i)

        self.temp_mesh = Mesh(vertices=vertices, indices=indices)
        self.temp_mesh.mode = 'triangle_fan' # the style of shapefile rendering. can take these values: 'points', 'line_strip', 'line_loop', 'lines', 'triangle_strip', 'triangle_fan'

    def render_mesh(self):
        with self.shapefileRenderer.canvas:
            Color(1, 0, 0, 0.3)
        # geom = gdf.loc[0, 'geometry']
            for polygon in gis.gdf['geometry']:
                # call build_mesh() per building
                self.build_mesh(polygon.exterior.coords)
        return
    
    def on_touch_down(self, touch): 
        # touch <MouseMotionEvent spos=(0.5798138869005011, 0.6323877068557919) pos=(1620.5798138869004, 1070.6323877068558)>
        self.last_pos_x = touch.pos[0]
        self.last_pos_y = touch.pos[1]
        if super().on_touch_down(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        return True

    def recreate_shapefileRenderer(self):
        # remove the widget for shapefile and recreate
        self.remove_widget(self.shapefileRenderer)
        self.shapefileRenderer = ShapefileRenderer()
        self.add_widget(self.shapefileRenderer)

    def refresh_shapefile(self, *args): # clock gives some args so here it receives *args eventhough it's not needed in the function
        self.recreate_shapefileRenderer()
        # self.remove_widget(self.shapefileRenderer)
        gis.set_bbox(self.get_bbox())
        # self.add_bbox_map_makers()
        self.render_mesh()


    # fire only touch_down and touch_up event
    def on_touch_move(self, touch):
        self.refresh_shapefile()

        if super().on_touch_move(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        return

    def on_touch_up(self, touch):
        self.refresh_shapefile()
        if super().on_touch_up(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        return 
    
    def on_touch_down(self, touch):
        self.refresh_shapefile()
        if super().on_touch_down(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        return 

    def on_transform(self, *args):
        # called when zoomed
        if gis.isInitialRender == False:
            self.refresh_shapefile()
        super().on_transform(args); 


    
