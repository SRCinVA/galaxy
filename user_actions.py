from kivy.uix.relativelayout import RelativeLayout


def keyboard_closed(self):  # not sure what this is doing ... ??
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            # not sure why he's doing this ...
            self.current_speed_x = self.SPEED_X

        elif keycode[1] == 'right':
            self.current_speed_x = -self.SPEED_X  # how does "negative speed" work ...?
        return True

def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0    

def on_touch_down(self, touch):
        # return super().on_touch_down(touch)
    if touch.x < self.width/2:
        # print("<-")
        self.current_speed_x = self.SPEED_X
    else:
        # print("->")
        self.current_speed_x = -self.SPEED_X
    return super(RelativeLayout, self).on_touch_down(touch)  # don't follow his explanation here ...


def on_touch_up(self, touch):
    # return super().on_touch_up(touch)
    print("UP")
    self.current_speed_x = 0 # we want this to be zero (which implies no movement)
    
