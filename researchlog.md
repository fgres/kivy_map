# research log


## 20.09.2023 remove old shapefile render
very difficult.
https://kivy.org/doc/stable/api-kivy.graphics.vertex_instructions.html

"The list attributes of the graphics instruction classes (e.g. Triangle.points, Mesh.indices etc.) are not Kivy properties but Python properties. As a consequence, the graphics will only be updated when the list object itself is changed and not when list values are modified."

when I tried "del self.mesh", it doesn't affect to the current render.

## 20.09.2023 shapefile renders very small except the initial render
apparently the initial bbox value and non initial bbox value is different
initial bbox value = coordinate of the center 100x100px
non inital bbox value = coordinate of the four corners of the visible area