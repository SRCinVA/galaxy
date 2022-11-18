from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        print("INIT W: " + str(self.width) + " H: " + str(self.height)) # from the __init__ function, the window can report its default size

    def on_parent(self, widget, parent):  # this is when we attach the widget to the app.
        # print("ON PARENT INIT W: " + str(self.width) + " H: " + str(self.height))
        pass

    def on_size(self, *args):  # are these built-in functions?
        print("ON SIZE INIT W: " + str(self.width) + " H: " + str(self.height))


class GalaxyApp(App):
    pass


GalaxyApp().run()
