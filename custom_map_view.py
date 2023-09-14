from kivy_garden.mapview import MapView
from kivy.graphics import Mesh
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.boxlayout import BoxLayout

from GIS import gis

class CustomMapView(MapView):
    def __init__(self, *args, **kwargs):
        self.mesh_list = []
        super(CustomMapView, self).__init__(*args, **kwargs)
        gis.set_bbox(self.get_bbox())
                
        # mapview = self.add_map_makers(mapview)

        self.wid = Widget(pos=(0, 0), size=Window.size)
        print("@@@@@@@@INITIAL WIDGET SIZE", self.wid.size)
        self.wid.canvas.add(Color(0, 0, 0))
        gis.set_widget(self.wid)
        print("!!!!!!!!initial wid", self.wid)

        self.render_mesh()

        layout = BoxLayout(size_hint=(1, None), height=50)
        self.add_widget(self.wid)
        self.add_widget(layout)

    def build_mesh(self, coords):
        vertices = []
        # vertices.extend([720, 480, 0, 0]) # shows where is the center of the widget
        indices = []

        for i, coord in enumerate(coords):
            x, y = gis.coords_to_point(coord[0], coord[1])
            vertices.extend([x, y, 0, 0])
            indices.append(i)

        temp_mesh = Mesh(vertices=vertices, indices=indices)
        temp_mesh.mode = 'line_strip' # 'points', 'line_strip', 'line_loop', 'lines', 'triangle_strip', 'triangle_fan'
        # print("$$$$$$$$$$$$$$MESH POS", self.mesh.pos)
        self.mesh_list.append(temp_mesh) 

    def render_mesh(self):
        with self.wid.canvas:
        # geom = gdf.loc[0, 'geometry']
            for polygon in gis.gdf['geometry']:
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
    
    # fire only touch_down and touch_up event
    def on_touch_move(self, touch):
        print("!!!!!!!!ON TOUCH MOVE")

        gis.set_bbox(self.get_bbox())
        # gis.set_widget(self.wid)

        self.render_mesh()
        # self.next_pos_x = touch.pos[0]
        # self.next_pos_y = touch.pos[1]
        # x_move = self.next_pos_x - self.last_pos_x
        # y_move = self.next_pos_y - self.last_pos_y
        # self.last_pos_x = touch.pos[0]
        # self.last_pos_y = touch.pos[1]
        # print(x_move, y_move)
        # for _mesh in self.mesh_list:
        #     new_positions = []
        #     list_id = 0
        #     for i in _mesh.vertices:
        #         print(_mesh)
        #         if list_id % 2 == 0:
        #             _mesh[list_id] =+ x_move
        #         else:
        #             _mesh[list_id] =+ y_move
        #         new_positions.append(i)
        #         list_id =+ 1

        #     _mesh.vertices = new_positions




        if super().on_touch_move(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        return

    def on_touch_up(self, touch):
        if super().on_touch_up(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        return 
    

    def on_transform(self, *args):
        print("Hello!"); 
        super().on_transform(args); 


    
