from kivy.app import App
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget

class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 7  # we'll use 7 lines in total
    V_LINES_SPACING = .1  # 10% of the screen width
    vertical_lines = []  # this will be where we keep the lists of vertical lines

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
            # self.line = Line(points=[100, 0, 100, 100]) # this populates x1, y1, x2, y2 for the line. 
            for i in range(0, self.V_NB_LINES): # this loop will create the spacing for the lines.
                self.vertical_lines.append(Line()) # (I believe) as you create the spaces you'll be appending them to the Line list. 

    def update_vertical_lines(self):
        central_line_x = int(self.width/2)
        # self.line.points = [center_x, 0, center_x, 100]
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES/2) # the offset from the middle point is negative since we're starting from the left.
        for i in range(0, self.V_NB_LINES): # this loop assigns the lines to the points you've established
            line_x = central_line_x + offset * spacing # builds each line on the x-axis
            self.vertical_lines[i].points = [line_x, 0, line_x, self.height] # places each line on the x and y axes
            offset += 1 # to move through each of the 7 lines

class GalaxyApp(App):
    pass


GalaxyApp().run()
