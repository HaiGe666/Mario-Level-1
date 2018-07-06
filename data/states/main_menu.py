__author__ = 'justinarmstrong'

import pygame as pg
from .. import setup, tools
from .. import constants as c
from .. components import info, mario


class Menu(tools._State):
    def __init__(self):
        """Initializes the state"""
        tools._State.__init__(self)
        persist = {c.COIN_TOTAL: 0, #初始persist哈哈
                   c.SCORE: 0,
                   c.LIVES: 3,
                   c.TOP_SCORE: 0,
                   c.CURRENT_TIME: 0.0,
                   c.LEVEL_STATE: None,
                   c.CAMERA_START_X: 0,
                   c.MARIO_DEAD: False,
                   'round': 1}
        self.startup(0.0, persist)

    def startup(self, current_time, persist):
        """Called every time the game's state becomes this one.  Initializes
        certain values"""
        self.next = c.LOAD_SCREEN   #'load screen'
        self.persist = persist
        self.game_info = persist
        self.overhead_info = info.OverheadInfo(self.game_info, c.MAIN_MENU)

        self.sprite_sheet = setup.GFX['title_screen']   #获取title_screen.png图片的surface，其中洋红色背景被设为了透明
        self.setup_background()
        self.setup_mario()
        self.setup_cursor()


    def setup_cursor(self):
        """Creates the mushroom cursor to select 1 or 2 player game"""
        self.cursor = pg.sprite.Sprite()
        dest = (220, 358)
        self.cursor.image, self.cursor.rect = self.get_image(
            24, 160, 8, 8, dest, setup.GFX['item_objects'])
        self.cursor.state = c.PLAYER1


    def setup_mario(self):
        """Places Mario at the beginning of the level"""
        self.mario = mario.Mario()
        self.mario.rect.x = 110 #左上角X坐标
        self.mario.rect.bottom = c.GROUND_HEIGHT    #mario下边缘的y坐标


    def setup_background(self):
        """Setup the background image to blit"""
        self.background = setup.GFX['level_1']
        self.background_rect = self.background.get_rect()   #get the rectangular area of the Surface
        self.background = pg.transform.scale(self.background,
                                   (int(self.background_rect.width*c.BACKGROUND_MULTIPLER),
                                    int(self.background_rect.height*c.BACKGROUND_MULTIPLER)))   #Resizes the Surface to a new resolution.
        self.viewport = setup.SCREEN.get_rect(bottom=setup.SCREEN_RECT.bottom)

        self.image_dict = {}
        self.image_dict['GAME_NAME_BOX'] = self.get_image(
            1, 60, 176, 88, (170, 100), setup.GFX['title_screen'])



    def get_image(self, x, y, width, height, dest, sprite_sheet):
        """Returns images and rects to blit onto the screen"""  #从图片上的制指定范围抠图到image再返回
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(sprite_sheet, (0, 0), (x, y, width, height)) #draw one image onto another
        if sprite_sheet == setup.GFX['title_screen']:
            image.set_colorkey((255, 0, 220))
            image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        else:
            image.set_colorkey(c.BLACK)
            image = pg.transform.scale(image,
                                   (int(rect.width*3),
                                    int(rect.height*3)))

        rect = image.get_rect()
        rect.x = dest[0]    #220    #设置被贴图的位置
        rect.y = dest[1]    #358
        return (image, rect)


    def update(self, surface, keys, current_time):  #<- (pg.display.get_surface())-tool.Control.update
        """Updates the state every refresh"""
        self.current_time = current_time
        self.game_info[c.CURRENT_TIME] = self.current_time
        self.update_cursor(keys)    #keys从tools.py的Control.event_loop中可以得到，用于确认选择，进入游戏和上下移动蘑菇光标
        self.overhead_info.update(self.game_info)   #更新分数、金币、闪烁的金币表示信息

        surface.blit(self.background, self.viewport, self.viewport) #blit(source,dest,area,special,special_flag)
        surface.blit(self.image_dict['GAME_NAME_BOX'][0],
                     self.image_dict['GAME_NAME_BOX'][1])
        surface.blit(self.mario.image, self.mario.rect)
        surface.blit(self.cursor.image, self.cursor.rect)
        self.overhead_info.draw(surface)    #!!!!!!!


    def update_cursor(self, keys):  #<- (key_pressed)-Menu.update <- tools.Control.update
        """Update the position of the cursor"""
        input_list = [pg.K_RETURN, pg.K_a, pg.K_s]  #enter,a,s

        if self.cursor.state == c.PLAYER1:  #初始self.cursor = c.PLAYER1
            self.cursor.rect.y = 358    #调整蘑菇光标贴在主屏幕上的位置
            if keys[pg.K_DOWN]:
                self.cursor.state = c.PLAYER2
            for input in input_list:
                if keys[input]:
                    self.reset_game_info()  #更新game_info
                    self.done = True    #确认选择，进入游戏
        elif self.cursor.state == c.PLAYER2:
            self.cursor.rect.y = 403
            if keys[pg.K_UP]:
                self.cursor.state = c.PLAYER1


    def reset_game_info(self):
        """Resets the game info in case of a Game Over and restart"""
        self.game_info[c.COIN_TOTAL] = 0
        self.game_info[c.SCORE] = 0
        self.game_info[c.LIVES] = 3
        self.game_info[c.CURRENT_TIME] = 0.0
        self.game_info[c.LEVEL_STATE] = None

        self.persist = self.game_info
















