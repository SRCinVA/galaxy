from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget
from kivy.properties import Clock


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 10 
    V_LINES_SPACING = .25  # 10% of the screen width
    vertical_lines = []  # this will be where we keep the lists of vertical lines

    H_NB_LINES = 15
    H_LINES_SPACING = .1   # this is the percentage in screen height
    horizontal_lines = []  # this will be where we keep the lists of vertical lines

    SPEED = 4
    current_offset_y = 0

    SPEED_X = 12
    current_speed_x = 0
    current_offset_x = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        print("INIT W: " + str(self.width) + " H: " + str(self.height)) # from the __init__ function, the window can report its default size
        self.init_vertical_lines() # unclear why you're calling this function from __init__
        self.init_horizontal_lines()
        Clock.schedule_interval(self.update, 1.0/60.0)  # using the update function for recreating the lines for the scrolling effect. 
                                                        # calling it 60 times per second

    def on_parent(self, widget, parent):  # this is when we attach the widget to the app.
        # print("ON PARENT INIT W: " + str(self.width) + " H: " + str(self.height))
        pass

    def on_size(self, *args):  # are these built-in functions?
        # print("ON SIZE INIT W: " + str(self.width) + " H: " + str(self.height))
        # self.perspective_point_x = self.width/2
        # self.perspective_point_y = self.height * 0.75
        # self.update_vertical_lines() # we'll rely on the update function to take care of this
        # self.update_horizontal_lines() # we'll rely on the update function to take care of this.
        pass

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
        offset = -int(self.V_NB_LINES/2) + 0.5 # the offset from the middle point is negative since we're starting from the left.
        for i in range(0, self.V_NB_LINES): # this loop assigns the lines to the points you've established
            line_x = central_line_x + offset * spacing + self.current_offset_x # builds each line on the x-axis
            
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2] # places each line on the x and y axes
            offset += 1 # to move through each of the 7 lines


    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # this loop will create the spacing for the lines.
            for i in range(0, self.H_NB_LINES): # here, we loop over the horizontal lines
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        central_line_x = int(self.width/2)
        spacing = self.V_LINES_SPACING * self.width
        offset = int(self.V_NB_LINES/2) - 0.5
        
        # the spacing must be the dynamic element here ...
        xmin = central_line_x - offset * spacing + self.current_offset_x
        # this spreads out to the right from the center.
        xmax = central_line_x + offset * spacing + self.current_offset_x
        spacing_y = self.H_LINES_SPACING * self.height

        for i in range(0, self.H_NB_LINES): # this loop assigns the lines to the points you've established
            # builds each line on the y-axis starting from 0, depending on the total height of the window (wo that we can resize it)
            line_y = i * spacing_y - self.current_offset_y # unclear what the offset is doing here.
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2] # places each line on the x and y axes

    def transform(self, x, y):
        # return self.transform_2D(x, y)  # we'll conduct development in 2D, then switch
        return self.transform_perspective(x,y)

    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        lin_y = y * self.perspective_point_y/self.height
        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y # this makes sure the transfor y is capped at a certain point.
        
        diff_x = x-self.perspective_point_x
        diff_y = self.perspective_point_y-lin_y
        factor_y = diff_y/self.perspective_point_y
        factor_y = pow(factor_y, 4) # exponent function

        tr_x = self.perspective_point_x + diff_x * factor_y   # tr_x will have a directly propertional relationship to y.
        tr_y = self.perspective_point_y - factor_y * self.perspective_point_y

        return int(tr_x), int(tr_y) 

    def on_touch_down(self, touch):
        # return super().on_touch_down(touch)
        if touch.x < self.width/2:
            print("<-")
            self.current_speed_x = self.SPEED_X
        else:
            print("->")
            self.current_speed_x = -self.SPEED_X


    def on_touch_up(self, touch):
        # return super().on_touch_up(touch)
        print("UP")
        self.current_speed_x = 0 # we want this to be zero (which implies no movement)

    def update(self, dt):  # the computing here is done in 2D, then later switched to 3D.
        # print("dt: " + str(dt*60))  # dt (delta time) is the difference in the time elapse from the last call of the function.
        time_factor = dt*60  # this tells you how fast it's running compared to a baseline of 1.00 (fucntion is called 60 times per second)
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.SPEED * time_factor  # increment this variable every time update() runs. Creates the impression of moving forward on the grid, by adding space "on top" of each line. 
                                                            # multiplying in time_factor helps us adjust if things slow down. This keeps the game moving evenly.

        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y >= spacing_y: # basically, as soon as the offset exceeds the spacing, you need to create another line for the illusion of the looping line. 
            self.current_offset_y -= spacing_y # # ... you just re-establish the offset as the same as the spacing, which in practice keeps inserting lines.

        self.current_offset_x += self.current_speed_x * time_factor

class GalaxyApp(App):
    pass


GalaxyApp().run()
