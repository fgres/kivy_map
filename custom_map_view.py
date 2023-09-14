from kivy_garden.mapview import MapView

class CustomMapView(MapView):

    def on_touch_down(self, touch): 
        # touch <MouseMotionEvent spos=(0.5798138869005011, 0.6323877068557919) pos=(1620.5798138869004, 1070.6323877068558)>
        if super().on_touch_down(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        return True
    
    # fire only touch_down and touch_up event
    def on_touch_move(self, touch):
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

    
