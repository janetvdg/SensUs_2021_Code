from weakref import ref


class Element:

    def __init__(self, layer, pos):
        self._layer = ref(layer)
        self.pos = pos

    @property
    def layer(self):
        return self._layer()

    @property
    def app(self):
        return self.layer.app

    @property
    def screen(self):
        return self.layer.screen

    def draw(self):
        raise NotImplementedError()


class Clickable:

    def click_down(self, pos, catched):
        return self.on_click_down(self.is_in(pos), catched) or catched

    def click_up(self, pos, catched):
        return self.on_click_up(self.is_in(pos), catched) or catched

    def is_in(self, pos):
        return False

    def on_click_down(self, inside, catched):
        return False

    def on_click_up(self, inside, catched):
        return False


class MouseMotionSensitive:

    def mouse_motion(self, pos, catched):
        pass


class Draggable(Element, MouseMotionSensitive):

    def __init__(self, layer, pos):
        Element.__init__(self, layer, pos)
        self.dragging = False

    def drag_start(self):
        self.dragging = True

    def drag_stop(self):
        self.dragging = False

    def mouse_motion(self, pos, catched):
        if self.dragging:
            self.pos = pos

    def on_click_down(self, inside, catched):
        if inside:
            self.drag_start()
            return True

    def on_click_up(self, inside, catched):
        self.drag_stop()
        return False


class RectangleClickable(Clickable):

    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def is_in(self, pos):
        c, s = self.pos, self.size
        x1 = c[0] - s[0]/2
        y1 = c[1] - s[1]/2
        x2 = c[0] + s[0]/2
        y2 = c[1] + s[1]/2
        if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
            return True
        return False


class CircleClickable(Clickable):

    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def is_in(self, pos):
        dx, dy = pos[0] - self.pos[0], pos[1] - self.pos[1]
        r2 = dx**2 + dy**2
        # TODO: circle enough large ?
        if r2 <= self.radius**2:
            return True
        return False
