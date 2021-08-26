import pygame
import application.gui as gui
import application.gui.base as base
from logging import getLogger
from weakref import ref
from subprocess import run, PIPE, DEVNULL
from collections import OrderedDict
import re
from pygame import gfxdraw
from pygame import mouse

def get_screen_resolution(log):
    try:
        xrandr = run(['xrandr'], stdout=PIPE, stderr=DEVNULL,
                     encoding='utf8').stdout
        res = re.search('\s*(\d+x\d+).*\*', xrandr).group(1).split('x')
        res = [int(i) for i in res]
    except BaseException as e:
        log.exception('Failed to get screen resolution, using 400x600: {e}')
        return [500, 500]
    log.info(f'Screen resolution: {res[0]}x{res[1]}')
    return res


def init(fullscreen=False, hide_cursor=False):
    log = getLogger('main.gui')
    pygame.init()
    pygame.mouse.set_visible(True)
    log.debug('Pygame initialized')
    #res = get_screen_resolution(log)
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if hide_cursor:
        # create an invisble cursor image
        pygame.mouse.set_cursor((8, 8), (0, 0),
                                (0, 0, 0, 0, 0, 0, 0, 0),
                                (0, 0, 0, 0, 0, 0, 0, 0))
#    if fullscreen:
#        return pygame.display.set_mode((400,600), flags | pygame.FULLSCREEN)

    return pygame.display.set_mode((800, 480), flags)


def quit():
    pygame.quit()


class Group(OrderedDict):

    def __init__(self, *args, **kwargs):
        self.log = getLogger('main.group')
        OrderedDict.__init__(self, *args, **kwargs)

    @property
    def clickable_elements(self):
        def is_clickable(e):
            return isinstance(e, base.Clickable) or isinstance(e, Group)
        elements = [(k, v) for k, v in self.items() if is_clickable(v)]
        return OrderedDict(elements)

    @property
    def mouse_sentive_elements(self):
        def is_mouse_sensitive(e):
            mse = isinstance(e, base.MouseMotionSensitive)
            return mse or isinstance(e, Group)
        elements = [(k, v) for k, v in self.items() if is_mouse_sensitive(v)]
        return OrderedDict(elements)

    def draw(self):
        for element in self.values():
            try:
                element.draw()
            except BaseException as e:
                self.log.exception(f'Failed to draw element: {e}')

    def click_down(self, pos, catched):
        for e in reversed(self.clickable_elements.values()):
            try:
                catched = e.click_down(pos, catched) or catched
            except BaseException as e:
                self.log.exception(f'Failed to exec click down: {e}')
        return catched

    def click_up(self, pos, catched):
        for e in reversed(self.clickable_elements.values()):
            try:
                catched = e.click_up(pos, catched) or catched
            except BaseException as e:
                self.log.exception(f'Failed to exec click up: {e}')
        return catched

    def mouse_motion(self, pos, catched):
        for e in reversed(self.mouse_sentive_elements.values()):
            try:
                catched = e.mouse_motion(pos, catched) or catched
            except BaseException as e:
                self.log.exception(f'Failed to exec mouse motion: {e}')
        return catched


class Layer(Group):

    def __init__(self, app, bg_color=(200, 200, 255)):
        super().__init__()
        self._app = ref(app)
        self.bg_color = bg_color
        self.log = getLogger('main.layer')

    @property
    def app(self):
        return self._app()

    @property
    def screen(self):
        return self.app.screen

    def draw(self):
        self.screen.fill(self.bg_color)
        Group.draw(self)


class Text(base.Element):

    # TODO tune default font_size
    def __init__(self, layer, pos, text='blabla', font_size=18, color=(0, 0, 0),
                 gray_color=(160, 160, 160), always_gray=False,
                 font='fonts/texgyreheros-regular.otf'):
        super().__init__(layer, pos)
        self.fg_color = color
        self.gray_color = gray_color
        self.always_gray = always_gray
        self.font_size = font_size
        self.font = pygame.font.Font(font, self.font_size)
        self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        self._text = t
        self.surf, self.rect = self.text_objects(t, self.fg_color)
        self.gray_surf, _ = self.text_objects(t, self.gray_color)
        self.rect.center = self.pos

    def text_objects(self, text, color):
        surf = self.font.render(text, True, color)
        return surf, surf.get_rect()

    def draw(self, gray=False):
        if gray or self.always_gray:
            self.screen.blit(self.gray_surf, self.rect)
        else:
            self.screen.blit(self.surf, self.rect)


class Image(base.Element):

    def __init__(self, layer, pos, path, w=None, h=None):
        super().__init__(layer, pos)
        self.img = pygame.image.load(path)
        iw, ih = self.img.get_width(), self.img.get_height()
        r = iw / ih
        if not w and not h:
            w, h = iw, ih
        elif not w:
            w, h = round(h * r), h
        elif not h:
            w, h = w, round(w / r)
        self.size = w, h
        self.img = pygame.transform.scale(self.img, self.size)

    def draw(self):
        p = self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2
        self.screen.blit(self.img, p)


class Rectangle(base.Element):

    def __init__(self, layer, pos, size, color=(255, 0, 0)):
        base.Element.__init__(self, layer, pos)
        self.size = size
        self.bg_color = color

    def draw(self, force_color=None):
        c, s = self.pos, self.size
        x, y = c[0] - s[0] / 2, c[1] - s[1] / 2
        color = force_color if force_color else self.bg_color
        pygame.draw.rect(self.screen, color, [x, y, *s])


class Button(Rectangle, Text, base.RectangleClickable):

    def __init__(self, layer, pos, size, text, action, disabled=False):
        Rectangle.__init__(self, layer, pos, size, (230, 220, 220))
        Text.__init__(self, layer, pos, text)
        base.RectangleClickable.__init__(self, pos, size)
        self.action = action
        self.disabled = disabled
        self.is_pressed = False

    def draw(self):
        if self.disabled:
            Rectangle.draw(self, (200, 200, 200))
            Text.draw(self, gray=True)
        elif self.is_pressed:
            Rectangle.draw(self, (210, 210, 210))
            Text.draw(self)
        else:
            Rectangle.draw(self)
            Text.draw(self)

    def on_click_down(self, inside, catched):
        if not catched and inside:
            self.is_pressed = True
            return True
        return False

    def on_click_up(self, inside, catched):
        if self.is_pressed and not self.disabled and inside:
            self.action()
        self.is_pressed = False
        return False


class Circle(base.Element):

    def __init__(self, layer, pos, radius, color=(255, 100, 100),
                 thickness=4):
        base.Element.__init__(self, layer, pos)
        self.radius = radius
        self.color = color
        self.thickness = thickness

    def draw(self, force_color=None):
        color = force_color if force_color else self.color
        # draw multiple circles to thicken the line
        gfxdraw.aacircle(self.screen, *self.pos, self.radius-1, color)
        gfxdraw.aacircle(self.screen, *self.pos, self.radius, color)
        gfxdraw.aacircle(self.screen, *self.pos, self.radius+1, color)
        #pygame.draw.circle(self.screen, color, self.pos, self.radius,
                           #self.thickness)


class DetectionCircle(Circle, base.Draggable, base.CircleClickable):

    def __init__(self, layer, pos, radius, color=(255, 100, 100)):
        base.Draggable.__init__(self, layer, pos)
        base.CircleClickable.__init__(self, pos, radius)
        Circle.__init__(self, layer, pos, radius, color)
        self.is_selected = False

    def draw(self):
        if self.is_selected or self.dragging:
            Circle.draw(self, (20, 200, 0))
        else:
            Circle.draw(self)

    def on_click_down(self, inside, catched):
        if catched or not inside:
            return False
        self.layer.select_circle(self)
        self.drag_start()
        return True

    def on_click_up(self, inside, catched):
        if inside and not catched and self.dragging:
            self.drag_stop()
            return True
        self.drag_stop()
        return False


class LoadingBar(base.Element):

    def __init__(self, layer, pos, size, bg_color=(42, 42, 42),
                 fg_color=(200, 200, 200), padding=1, progress=0):
        super().__init__(layer, pos)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self._progress = progress
        self.size = size
        self.padding = padding

    @property
    def progression(self):
        return self._progress

    @progression.setter
    def progression(self, v):
        self._progress = max(0, min(1, v))

    def draw(self):
        c, s, p, v = self.pos, self.size, self.padding, self.progression
        x, y = c[0] - s[0]/2, c[1] - s[1]/2
        xp, yp = x + p, y + p
        wp, hp = v * (s[0] - 2 * p), s[1] - 2 * p
        pygame.draw.rect(self.screen, self.bg_color, (x, y, *s))
        pygame.draw.rect(self.screen, self.fg_color, (xp, yp, wp, hp))


class Video(base.Element):

    def __init__(self, layer):
        super().__init__(layer, (0, 0))

    def draw(self):
        if self.app.live_image is None:
            return
        self.screen.blit(self.app.live_image, (0, 0))


class Slider(base.Draggable, base.RectangleClickable):

    def __init__(self, layer, pos, size, vmin, vmax, action,
                 padding=20, line_width=4):
        base.Draggable.__init__(self, layer, pos)
        base.RectangleClickable.__init__(self, pos, size)
        self.padding = padding
        self.line_width = line_width
        self.vmin = vmin
        self.vmax = vmax
        self.action = action
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        self.action(self.vmin + v * (self.vmax - self.vmin))

    def set(self, v):
        self.value = (v - self.vmin) / (self.vmax - self.vmin)

    def draw(self):
        self.draw_line()
        self.draw_dot()

    def draw_line(self):
        x, y = self.pos
        w, h = self.size[0] - 2 * self.padding, self.line_width
        x, y = x - w / 2, y - h / 2
        pygame.draw.rect(self.screen, (42, 42, 42), [x, y, w, h])

    def draw_dot(self):
        w = self.size[0] - 2 * self.padding
        x = round(self.pos[0] + (self.value - 0.5) * w)
        y = self.pos[1]
        gfxdraw.filled_circle(self.screen, x, y, 16,
                              (100, 255, 100))
        # pygame.draw.circle(self.screen, (100, 255, 100), (x, y), 16)

    def mouse_motion(self, pos, catched):
        if self.dragging:
            x = pos[0] - (self.pos[0] - self.size[0] / 2)
            self.value = min(max(x / self.size[0], 0), 1)
