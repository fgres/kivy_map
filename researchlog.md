# research log

## transform shapefile while zooming
the problem is that zooming in/out calls an event "on_transform" at the begining of zooming (though usually it's sequential) and at the end of the zoom, the basemap is zoomed and the shape file is not zoomed (or the last the zoomed size when it's sequential). so to disguise this glitch, in the build function at mapview.py Clock calls refresh_shapefile intervally

## how to get the meta data from shapefile
see:
https://github.com/quarree100/qScope_frontend/blob/main/q100viz/buildings.py
def load_data(self, create_clusters=False):


## 28.09.2023
new: instead of manipulating vertecies, now it creates a child widget and display shapefile there. when move event fires the child widgets get recreated. Might be that the process is heavy but so far it kinda works. 

ref:
https://kivy.org/doc/stable/api-kivy.uix.widget.html#kivy.uix.widget.Widget.remove_widget

old ref:
https://kivy.org/doc/stable/api-kivy.graphics.tesselator.html
"self.canvas.add"



## 20.09.2023 remove old shapefile render
very difficult.
https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html

"The list attributes of the graphics instruction classes (e.g. Triangle.points, Mesh.indices etc.) are not Kivy properties but Python properties. As a consequence, the graphics will only be updated when the list object itself is changed and not when list values are modified."

when I tried "del self.mesh", it doesn't affect to the current render.

## 20.09.2023 shapefile renders very small except the initial render
apparently the initial bbox value and non initial bbox value is different
initial bbox value = coordinate of the center 100x100px
non inital bbox value = coordinate of the four corners of the visible area