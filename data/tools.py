import os
import pygame as pg

keybinding = {
    'action':pg.K_s,
    'jump':pg.K_a,
    'left':pg.K_LEFT,
    'right':pg.K_RIGHT,
    'down':pg.K_DOWN
}

class Control(object):
    """Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here."""
    def __init__(self, caption):
        self.screen = pg.display.get_surface()  #get a reference to the currently set display surface, if no displaying surface return None
        self.done = False
        self.clock = pg.time.Clock()    #create an object to help track time
        self.caption = caption
        self.fps = 55
        self.show_fps = False
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()    #true if the display is receiving keyboard input from the system
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):    #<- (state_dict,c.MAIN_MENU)-main.py
        self.state_dict = state_dict
        self.state_name = start_state   #从main menu -> load_screen
        self.state = self.state_dict[self.state_name]

    def update(self):   #<- self.main
        self.current_time = pg.time.get_ticks() #Return the number of milliseconds since pygame.init() was called. Before pygame is initialized this will always be 0.
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()   #状态转换MAIN_MENU按下a,s,enter和LOADSCRREEN过2635ms后
        self.state.update(self.screen, self.keys, self.current_time)    # 1.load screen (screen,key_pressed,current_time)-(主屏幕，按键字典，时间)  #观察各模块的update函数

    def flip_state(self):   #<- Control.update
        previous, self.state_name = self.state_name, self.state.next    #main menu->load screen
        persist = self.state.cleanup()  #self.state.done = False
        self.state = self.state_dict[self.state_name]   #MAIN_MENU转换顺便创建了一个LoadScreen实例,LOADSCREEN转换到LEVEL1
        self.state.startup(self.current_time, persist)  #调用各模块的start_up函数
        self.state.previous = previous


    def event_loop(self):   #<- self.main
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.state.get_event(event) #进入各state的get_event函数进行更新，初始是MAIN_MENU 接着是 LOAD_SCREEN，然而MENU的get_event没什么卵用,LoadScreen的也是


    def toggle_show_fps(self, key): #<- self.event_loop() <- self.main
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:   #False
                pg.display.set_caption(self.caption)    #Super Mario 1-1


    def main(self): #<- main.py
        """Main loop for entire program"""
        while not self.done:    #在self.update中会更新self.done为True，使循环结束
            self.event_loop()   #获取按键？？待研究各state的get_event函数，1.帮MENU拿到按键
            self.update()
            pg.display.update() #更新屏幕部分内容？
            self.clock.tick(self.fps)   #update the clock and limit the run time speed of the game
            if self.show_fps:   #在窗口上显示fps
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(self.caption, fps)  #"Super Mario 1-1"后显示fps
                pg.display.set_caption(with_fps)


class _State(object):
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        pass

    def startup(self, current_time, persistant):
        self.persist = persistant   #？？？
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, surface, keys, current_time):
        pass



def load_all_gfx(directory, colorkey=(255,0,255), accept=('.png', '.jpg', '.bmp')):   #是不是缺了.号
    """colorkey=(255,0,255)是洋红色，目的应该是将title_screen.png的背景色设置成透明"""
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha(): #get the current Surface transparency value
                img = img.convert_alpha()   #change the pixel format of an image including per pixel alphas
            else:
                img = img.convert() #change the pixel format of an image
                img.set_colorkey(colorkey)  #Set the transparent colorkey
            graphics[name]=img
    return graphics


def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')): #<- setup.py
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song) #只是路径名字典而已
    return songs


def load_all_fonts(directory, accept=('.ttf')):
    return load_all_music(directory, accept)


def load_all_sfx(directory, accept=('.wav','.mpe','.ogg','.mdi')):  #<- (os.path.join("resources","sound"))-setup.SFX
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)    #分开文件名和后缀
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx)) #Create a new Sound object from a file or buffer object #使用指定文件名载入一个音频文件，并创建一个Sound对象
    return effects











