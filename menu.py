from kivy.uix.relativelayout import RelativeLayout

class MenuWidget(RelativeLayout):
    def on_touch_down(self, touch):  # we'll manage this function from here, but run it from main.py(?)
        if self.opacity == 0:
            return False  # if opacity = 0, we won't do anything with touch.
        return super(RelativeLayout, self).on_touch_down(touch)
