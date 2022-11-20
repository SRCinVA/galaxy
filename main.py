from kivy.app import App
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget

class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    line = None  # to put the line in the middle of the window

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        print("INIT W: " + str(self.width) + " H: " + str(self.height)) # from the __init__ function, the window can report its default size
        self.init_vertical_lines() # unclear why you're calling this function from __init__

    def on_parent(self, widget, parent):  # this is when we attach the widget to the app.
        # print("ON PARENT INIT W: " + str(self.width) + " H: " + str(self.height))
        pass

    def on_size(self, *args):  # are these built-in functions?
        print("ON SIZE INIT W: " + str(self.width) + " H: " + str(self.height))
        # self.perspective_point_x = self.width/2
        # self.perspective_point_y = self.height * 0.75
        self.update_vertical_lines()

    def on_perspective_point_x(self, widget, value):  # this method is based on a property in kivy. It's automatically called when the property changes in value.
        # print("PX: " + str(value))
        pass

    def on_perspective_point_y(self, widget, value): # (same as method above)
        # print("PY: " + str(value))
        pass

    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            self.line = Line(points=[100, 0, 100, 100]) # this populates x1, y1, x2, y2 for the line. 

    def update_vertical_lines(self):
        center_x = int(self.width/2)
        self.line.points = [center_x, 0, center_x, 100]

class GalaxyApp(App):
    pass


GalaxyApp().run()
