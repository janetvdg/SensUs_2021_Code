import application.gui as gui
from itertools import count


class Layer(gui.Layer):

    background = None

    def __init__(self, app):
        bg_color = (200, 200, 100) if app.debug else (255, 255, 255)
        gui.Layer.__init__(self, app, bg_color)
        if self.background is None:
            self.background = gui.Image(self, [800/2, 480/2],
                                        'images/wallpaper.png',
                                        h=480)

    def set_layer(self, l):
        self.app.active_layer = l

    def create_background(self):
        self['bg'] = self.background
        
#If want to move the list of buttons donw, just need to change the value of the offset
    def create_buttons_list(self, buttons):
        w_btn = 300
        h_btn = 50
        pitch = 75
        x_img = 220
        x_btn = 400
        y0 = round(600/2 - (len(buttons) - 1) / 2 * pitch)
        offset = 0
        for n, (k, title, path, action) in enumerate(buttons):
            y = offset + y0 + n * pitch
            self['img_' + k] = gui.Image(self, [x_img, y], path, h=h_btn)
            self[k] = gui.Button(self, [x_btn, y], [w_btn, h_btn], title,
                                 action)

    def create_small_buttons_list(self, buttons):
        w_btn = 300
        h_btn = 35
        pitch = 45
        x_btn = 400
        y0 = round(480/2 - (len(buttons) - 1) / 2 * pitch)
        for n, (k, title, action) in enumerate(buttons):
            y = y0 + n * pitch
            self[k] = gui.Button(self, [x_btn, y], [w_btn, h_btn], title,
                                 action)

    def create_next_button(self, target, text='Next', size=[150, 40],
                           disabled=False):
        pos = (800 - 100, 480 - 40)
        self['next'] = gui.Button(self, pos, size, text,
                                  lambda: self.set_layer(target),
                                  disabled=disabled)

    def create_back_button(self, target, text='Back', size=[150, 40]):
        pos = (0 + 100, 480 - 40)
        self['back'] = gui.Button(self, pos, size, text,
                                  lambda: self.set_layer(target))

    def create_title(self, title):
        self['title'] = gui.Text(self, (400, 50), title, font_size=35)
        
    def create_text(self, text):
        self['text'] = gui.Text(self, (400, 100), text, font_size=20)


class OverLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self['ip'] = gui.Text(self, (400, 16), '-', font_size=11)
        self['fps'] = gui.Text(self, (100, 16), '?? fps', font_size=11)

    # overwrite draw to avoid drawing the background
    def draw(self):
        gui.Group.draw(self)


class WelcomeLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        #self['logo'] = gui.Image(self, (220, 200),'images/SenSwiss_logo.png',h=300)
        #self['text'] = gui.Text(self, (220, 500),'Team SenSwiss from EPFL',font_size=25, color=(218, 41, 28))
        self['background'] = gui.Image(self, [800/2, 480/2],"images/backgroundSenSwiss.jpeg", h=480)
        
        
        
    def click_down(self, pos, catched):
        self.app.active_layer = 'main'
        return True


class MainLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        btn_list = [
            ('measure', 'New measure', 'images/measure.png',
             lambda: self.set_layer('focus')),
            ('manual', 'User manual', 'images/help.png',
             lambda: self.set_layer('manual')),
            ('contact', 'Contact Support', 'images/phone.png',
             lambda: self.set_layer('contact')),
        ]
        self.create_background()
        self.create_title('Welcome')
        self['text'] = gui.Text(self, (400,100),
                                'Influenza saliva test',
                                font_size=20, color=(0, 0, 0))
        self.create_buttons_list(btn_list)
        self.create_back_button('welcome','Back')

class ManualLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_title('User manual')
        self.create_back_button('main')
        self['text'] = gui.Text(self, (400, 100),
                                'Put image of manual...',
                                font_size=25, color=(0, 0, 0))
        self['text'] = gui.Text(self, (400, 300),
                                'Do something more...',
                                font_size=25, color=(0, 0, 0))

'''
class ChipLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        btn_list = [
            ('instructions', 'Instructions', 'images/questions.png',
             lambda: self.set_layer('tutorial1')),
            ('skip', 'Skip instructions', 'images/continue.png',
             lambda: self.set_layer('insert')),
        ]
        self.create_background()
        self.create_title('Prepare the cartridge') #Changed
        self.create_buttons_list(btn_list)
        self.create_back_button('main', 'Cancel')
''' 

class ContactLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_background()
        self.create_title('In case of problem, please contact us')
        self.create_back_button('main')
        self['rect'] = gui.Rectangle(self, (400, 260), (500, 200),
                                     color=(255, 255, 255))
        self['phone_img'] = gui.Image(self, (200, 200),
                                      'images/phone.png', h=50)
        self['phone'] = gui.Text(self, (450, 200),
                                 'Phone: 078 842 25 20')
        self['mail_img'] = gui.Image(self, (200, 300),
                                     'images/mail.png', h=50)
        self['mail'] = gui.Text(self, (450, 300),
                                'Email: teamEPFSens@gmail.com')
'''
class TutorialLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_title('ADD USER MANUAL')
        #self.create_next_button('tutorial2')
        self.create_back_button('main')
        self['img'] = gui.Image(self, [400, 270],
                                'images/tuto1.png',
                                h=300)


class Tutorial2Layer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_next_button('tutorial3')
        self.create_back_button('tutorial1', 'Previous')
        self['img'] = gui.Image(self, [400, 220],
                                'images/tuto2.png',
                                h=300)


class Tutorial3Layer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_next_button('tutorial4')
        self.create_back_button('tutorial2', 'Previous')
        self['img'] = gui.Image(self, [400, 220],
                                'images/tuto3.png',
                                h=300)


class Tutorial4Layer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_next_button('tutorial5')
        self.create_back_button('tutorial3', 'Previous')
        self['img'] = gui.Image(self, [400, 220],
                                'images/tuto4.png',
                                h=300)


class Tutorial5Layer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_next_button('insert', 'Start')
        self.create_back_button('tutorial4', 'Previous')
        self['img'] = gui.Image(self, [400, 220],
                                'images/tuto5.png',
                                h=300)



class InsertLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_title('Insert the chip')
        self.create_next_button('focus', 'Done')
        self.create_back_button('main')
        # TODO create correct insert_chip.png
        self['img'] = gui.Image(self, [400, 280],
                                'images/insert_chip.png',
                                h=300)
'''

class FocusLayer(Layer):

    # TODO: add a stream object in initGui
    def __init__(self, app):
        super().__init__(app)
        self['wait_stream'] = gui.Text(self, (400, 240),
                                       'Loading video...',
                                       always_gray=True)
        self['stream'] = gui.Video(self)
        self.create_title('Please set the focus')
        self.create_next_button('acquisition', 'Done')
        self.create_back_button('main')


class AcquisitionLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self['wait_stream'] = gui.Text(self, (400, 240),
                                       'Loading video...',
                                       always_gray=True)
        self['stream'] = gui.Video(self)
        self['circles'] = gui.Group()
        self.create_title('Acquisition')
        self.create_next_button('analysis', disabled=False)
        self.create_back_button('focus', 'Cancel')

        x0 = 740
        y0 = 60
        s = 40
        self['add'] = gui.Button(self, (x0-s/2, y0-s/2), (s, s), '+',
                                 lambda: self.new_circle((100, 100), 42))
        self['rem'] = gui.Button(self, (x0+s/2, y0-s/2), (s, s), '−',
                                 lambda: self.rem_selected_circles())
        self['reset'] = gui.Button(self, (x0, y0+s/2), (2*s, s), 'Reset',
                                   lambda: self.set_circles([]))
        self['size'] = gui.Slider(self, (400, 480 - 50), (350, 64), 10, 200,
                                  lambda r: self.set_selected_circles_radius(r))
        self['progress'] = gui.LoadingBar(self, (400, 120), (300, 8))

    def select_circle(self, c):
        for v in self['circles'].values():
            v.is_selected = False
            print('unselected')
        if c:
            c.is_selected = True
            print('selected_one cricle')
            self['size'].set(c.radius)

    def get_new_key(self):
        for i in count():
            if i not in self['circles']:
                return i

    def get_selected_circles(self):
        return { k:v for k, v in self['circles'].items() if v.is_selected}

    def get_spots_coordinates(self):
        circles = [(4*c.pos[0], 4*(c.pos[1]+26.5), 4*c.radius) for c in self['circles'].values()]
        return circles

    def set_circles(self, circles):
        circles = [gui.DetectionCircle(self, p, r) for p, r in circles]
        circles = [(self.get_new_key(), c) for c in circles]
        self['circles'] = gui.Group(circles)

    def new_circle(self, p, r):
        circle = gui.DetectionCircle(self, p, r)
        self['circles'][self.get_new_key()] = circle

    def rem_selected_circles(self):
        for k in self.get_selected_circles():
            del self['circles'][k]

    def set_selected_circles_radius(self, r):
        for k in self.get_selected_circles():
            self['circles'][k].radius = round(r)

    def click_down(self, pos, catched):
        catched = super().click_down(pos, catched)
        if not catched:
            self.select_circle(None)
        return catched


class AnalysisLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_title('Results')
        self.create_back_button('focus', 'Cancel')
        # self['progress'] = gui.LoadingBar(self, (400, 300), (300, 8))

        self['concentration'] = gui.Text(self, (500, 200), font_size=25, color=(0, 0, 0),
                     gray_color=(0, 0, 0), always_gray=False)
        self['slope'] = gui.Text(self, (500, 300), font_size=25, color=(0, 0, 0),
                     gray_color=(0, 0, 0), always_gray=False)
        self['swiss'] = gui.Text(self, (500, 390), text='(Swiss precision)', font_size=18, color=(0, 0, 0),
                     gray_color=(0, 0, 0), always_gray=False)
        self.create_next_button('focus', text='New measure')


class ProfilesLayer(Layer):

    def __init__(self, app):
        super().__init__(app)

        def nope():
            pass

        btn_list = [
            ('bourban', 'Bourban Emile', nope),
            ('conti', 'Conti Mark', nope),
            ('cucu', 'Cucu Raluca', nope),
            ('giezendanner', 'Giezendanner Ludovic', nope),
            ('perier', 'Perier Marion', nope),
            ('schalk', 'Schalk Katia', nope),
            ('viatte', 'Viatte Clara', nope),
        ]
        self.create_background()
        self.create_small_buttons_list(btn_list)
        self.create_back_button('main')


class HelpLayer(Layer):

    def __init__(self, app):
        super().__init__(app)

        self.create_background()
        self.create_title('In case of problem, please contact us')
        self.create_back_button('main')
        self['rect'] = gui.Rectangle(self, (400, 260), (500, 200),
                                     color=(255, 255, 255))
        self['phone_img'] = gui.Image(self, (200, 200),
                                      'images/phone.png', h=50)
        self['phone'] = gui.Text(self, (450, 200),
                                 'Phone: 078 842 25 20')
        self['mail_img'] = gui.Image(self, (200, 300),
                                     'images/mail.png', h=50)
        self['mail'] = gui.Text(self, (450, 300),
                                'Email: teamEPFSens@gmail.com')


class ParametersLayer(Layer):

    def __init__(self, app):
        super().__init__(app)

        def nope():
            pass

        btn_list = [
            ('language', 'Languages', 'images/language.png', nope),
            ('brightness', 'Brightness', 'images/light.png', nope)
        ]
        self.create_background()
        self.create_buttons_list(btn_list)
        self.create_back_button('main')
