from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform # to determine if the platform is desktop or mobile
from kivy.core.window import Window  # this needs to come after the configuration settings (can't remember why ...)
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget
from kivy.properties import Clock
from kivy.graphics.vertex_instructions import Quad

class MainWidget(Widget):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 4
    V_LINES_SPACING = .1  # 10% of the screen width
    vertical_lines = []  # this will be where we keep the lists of vertical lines

    H_NB_LINES = 15
    H_LINES_SPACING = .1   # this is the percentage in screen height
    horizontal_lines = []  # this will be where we keep the lists of vertical lines

    SPEED = 1
    current_offset_y = 0
    current_y_loop = 0

    SPEED_X = 12
    current_speed_x = 0
    current_offset_x = 0

    NB_TILES = 8
    tiles = []
    tiles_coordinates = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        print("INIT W: " + str(self.width) + " H: " + str(self.height)) # from the __init__ function, the window can report its default size
        self.init_vertical_lines() # unclear why you're calling this function from __init__
        self.init_horizontal_lines()
        self.init_tiles()
        self.generate_tiles_coordinates()

        if self.is_desktop():  # we only need to configure the keyboard if it's a desktop.
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down=self.on_keyboard_down)
            self.keyboard.bind(on_key_up=self.on_keyboard_up) # also need to know when we release the key

        Clock.schedule_interval(self.update, 1.0/60.0)  # using the update function for recreating the lines for the scrolling effect. 
                                                        # calling it 60 times per second

    def is_desktop(self):  # we call this function above in the init()
        if platform in ("Linux", "win", "macosx"):
            return True # meaning, it's a desktop computer
        else:
            return False


    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())  # not sure why Quad() is embedded in append() ...

    def generate_tiles_coordinates(self):
        for i in range(0, self.NB_TILES):
            self.tiles_coordinates.append((0, i)) # these will be in a straight line, so x is 0, and y is populated by looping through the index (?)


    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            # self.line = Line(points=[100, 0, 100, 100]) # this populates x1, y1, x2, y2 for the line. 
            for i in range(0, self.V_NB_LINES): # this loop will create the spacing for the lines.
                self.vertical_lines.append(Line()) # (I believe) as you create the spaces you'll be appending them to the Line list. 

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x  # not sure why this is better than int(self.width/2)
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5  # whatever the index is, we want to be halfway on the left.
        line_x = central_line_x + offset * spacing + self.current_offset_x # self.current_offset_x tells us how far from the true center_x we need to go.
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y # current_offset_y is what creates the illusion of movement in the game. As the index increases, you populate the horizontal lines upwards
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop  # this re-assigns the tile to the next spot in the index. As a result, it disappears off the screen.
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y
    
    def update_tiles(self):
        for i in range(0, self.NB_TILES): # you loop through the tuples and break out tile coordinates from each.
            tile = self.tiles[i] # unclear why he did this ...
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)
            # Actually, we are not doing this:
            # xmax, ymin = self.get_tile_coordinates(self.ti_x + 1, self.ti_y - 1)
            # xmin, ymax = self.get_tile_coordinates(self.ti_x - 1, self.ti_y + 1)
            
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]


    def update_vertical_lines(self): # setting up the range of indices is a bit tricky, as shown below.
        start_index = -int(self.V_NB_LINES/2) + 1 # negative because we're starting the index at -1 (making 0 the middle)
        for i in range(start_index, start_index + self.V_NB_LINES): # this loop assigns the lines to the points you've established
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2] # places each line on the x and y axes

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # this loop will create the spacing for the lines.
            for i in range(0, self.H_NB_LINES): # here, we loop over the horizontal lines
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        start_index = -int(self.V_NB_LINES/2) + 1
        end_index = start_index + self.V_NB_LINES -1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.H_NB_LINES): # this loop assigns the lines to the points you've established
            # builds each line on the y-axis starting from 0, depending on the total height of the window (wo that we can resize it)
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2] # places each line on the x and y axes

    def update(self, dt):  # the computing here is done in 2D, then later switched to 3D.
        # print("dt: " + str(dt*60))  # dt (delta time) is the difference in the time elapse from the last call of the function.
        time_factor = dt*60  # this tells you how fast it's running compared to a baseline of 1.00 (fucntion is called 60 times per second)
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.current_offset_y += self.SPEED * time_factor  # increment this variable every time update() runs. Creates the impression of moving forward on the grid, by adding space "on top" of each line. 
                                                            # multiplying in time_factor helps us adjust if things slow down. This keeps the game moving evenly.

        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y >= spacing_y: # basically, as soon as the offset exceeds the spacing, you need to create another line for the illusion of the looping line. 
            self.current_offset_y -= spacing_y # # ... you just re-establish the offset as the same as the spacing, which in practice keeps inserting lines.
            self.current_y_loop += 1

        # self.current_offset_x += self.current_speed_x * time_factor

class GalaxyApp(App):
    pass


GalaxyApp().run()
