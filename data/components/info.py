import pygame as pg
from .. import setup
from .. import constants as c
from . import flashing_coin


class Character(pg.sprite.Sprite):  #<- (self.image_dict[letter])-creatf_label
    """Parent class for all characters used for the overhead level info"""
    def __init__(self, image):
        super(Character, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()


class OverheadInfo(object): #<- (perlist,c.LEVEL)-load_screen.LoadScreen.startup
    """Class for level information like score, coin total,
        and time remaining"""
    def __init__(self, game_info, state):
        self.sprite_sheet = setup.GFX['text_images']    #time out and game over image
        self.coin_total = game_info[c.COIN_TOTAL]   #game_info -> load_screen.LoadScreen.persist
        self.time = 401 #?
        self.current_time = 0
        self.total_lives = game_info[c.LIVES]
        self.top_score = game_info[c.TOP_SCORE]
        self.state = state  #load_screen.LoadScreen.info_state(LoadScreen(str))
        self.special_state = None
        self.game_info = game_info

        self.create_image_dict()    #创造字符和对应显示surface字典
        self.create_score_group()   #创造初始得分'000000'显示样式Character(sprite)集合 ^ self.score_images
        self.create_info_labels()   #创造'MARIO''WORLD''TIME''1-1'显示样式Character(sprite)集合，^ mario_label,world_label.time_label,stage_label >> label_list
        self.create_load_screen_labels()    #创造'WORLD''1-1'显示样式Character(sprite)集合，^ world_label,number_label >> center_label
        self.create_countdown_clock()   #创时间显示样式Character(sprite)集合， ^ count_down_images
        self.create_coin_counter()  #创造'*00'显示样式Character(sprite)集合，^ coin_count_images
        self.create_flashing_coin() #创造闪烁金币图片实例 ^ flashing_coin
        self.create_mario_image()   #设置显示mario,*,lives,界面 ^ life_times_rect,life_total_label,mario_rect
        self.create_game_over_label()   #设置GAME OVER ^ game_label,over_label
        self.create_time_out_label()    #设置TIME OUT ^ time_out_label
        self.create_main_menu_labels()  #设置MAIN MENU ^ player_one_game,player_two_game,top,top_score >> main_menu_labels


    def create_image_dict(self):    #<- self.__init__
        """Creates the initial images for the score"""
        self.image_dict = {}
        image_list = []

        image_list.append(self.get_image(3, 230, 7, 7)) #(x,y,width,height) #以下10行为0~9的游戏显示字体
        image_list.append(self.get_image(12, 230, 7, 7))
        image_list.append(self.get_image(19, 230, 7, 7))
        image_list.append(self.get_image(27, 230, 7, 7))
        image_list.append(self.get_image(35, 230, 7, 7))
        image_list.append(self.get_image(43, 230, 7, 7))
        image_list.append(self.get_image(51, 230, 7, 7))
        image_list.append(self.get_image(59, 230, 7, 7))
        image_list.append(self.get_image(67, 230, 7, 7))
        image_list.append(self.get_image(75, 230, 7, 7))

        image_list.append(self.get_image(83, 230, 7, 7))    #A
        image_list.append(self.get_image(91, 230, 7, 7))
        image_list.append(self.get_image(99, 230, 7, 7))
        image_list.append(self.get_image(107, 230, 7, 7))
        image_list.append(self.get_image(115, 230, 7, 7))
        image_list.append(self.get_image(123, 230, 7, 7))   #F
        image_list.append(self.get_image(3, 238, 7, 7))     #G
        image_list.append(self.get_image(11, 238, 7, 7))
        image_list.append(self.get_image(20, 238, 7, 7))
        image_list.append(self.get_image(27, 238, 7, 7))
        image_list.append(self.get_image(35, 238, 7, 7))
        image_list.append(self.get_image(44, 238, 7, 7))
        image_list.append(self.get_image(51, 238, 7, 7))
        image_list.append(self.get_image(59, 238, 7, 7))
        image_list.append(self.get_image(67, 238, 7, 7))
        image_list.append(self.get_image(75, 238, 7, 7))
        image_list.append(self.get_image(83, 238, 7, 7))
        image_list.append(self.get_image(91, 238, 7, 7))
        image_list.append(self.get_image(99, 238, 7, 7))
        image_list.append(self.get_image(108, 238, 7, 7))
        image_list.append(self.get_image(115, 238, 7, 7))
        image_list.append(self.get_image(123, 238, 7, 7))   #V
        image_list.append(self.get_image(3, 246, 7, 7))     #W
        image_list.append(self.get_image(11, 246, 7, 7))
        image_list.append(self.get_image(20, 246, 7, 7))
        image_list.append(self.get_image(27, 246, 7, 7))
        image_list.append(self.get_image(48, 248, 7, 7))    #@

        image_list.append(self.get_image(68, 249, 6, 2))    #-
        image_list.append(self.get_image(75, 247, 6, 6))    #*



        character_string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -*'

        for character, image in zip(character_string, image_list):
            self.image_dict[character] = image  #字符和对应显示在屏幕上相应的样式


    def get_image(self, x, y, width, height):   #<- self.creat_image_dict <- self.__init__
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))    #sprite_sheet: text_images
        image.set_colorkey((92, 148, 252))  #浅蓝
        image = pg.transform.scale(image,   #扩大2.9倍
                                   (int(rect.width*2.9),
                                    int(rect.height*2.9)))
        return image


    def create_score_group(self):   #<- self.__init__
        """Creates the initial empty score (000000)"""
        self.score_images = []
        self.create_label(self.score_images, '000000', 75, 55)


    def create_info_labels(self):   #<- self.__init__
        """Creates the labels that describe each info"""
        self.mario_label = []
        self.world_label = []
        self.time_label = []
        self.stage_label = []


        self.create_label(self.mario_label, 'MARIO', 75, 30)
        self.create_label(self.world_label, 'WORLD', 450, 30)
        self.create_label(self.time_label, 'TIME', 625, 30)
        self.create_label(self.stage_label, '1-1', 472, 55)

        self.label_list = [self.mario_label,
                           self.world_label,
                           self.time_label,
                           self.stage_label,]


    def create_load_screen_labels(self):    #<- self.__init__
        """Creates labels for the center info of a load screen"""
        world_label = []
        number_label = []
        score_label = []

        self.create_label(world_label, 'WORLD', 280, 200)
        self.create_label(number_label, '1-'+str(self.game_info['round']), 430, 200)
        self.create_label(score_label, 'SCORE '+str(500 * self.game_info['round']**2), 280, 350)

        self.center_labels = [world_label, number_label, score_label]


    def create_countdown_clock(self):
        """Creates the count down clock for the level"""
        self.count_down_images = []
        self.create_label(self.count_down_images, str(self.time), 645, 55)


    def create_label(self, label_list, string, x, y):   #<- (self.score_images, '000000', 75, 55)-self.creat_score_group
        """Creates a label (WORLD, TIME, MARIO)"""
        for letter in string:
            label_list.append(Character(self.image_dict[letter]))   #label_list里面是字符的Character实例(继承了精灵)，里面包含显示字符surface和rect

        self.set_label_rects(label_list, x, y)  #设置Character(sprite)的rect参数


    def set_label_rects(self, label_list, x, y):    #<- (Character'000000',75,55)-(label_list, x, y)-create_label
        """Set the location of each individual character"""
        for i, letter in enumerate(label_list):
            letter.rect.x = x + ((letter.rect.width + 3) * i)   #以下位置待证
            letter.rect.y = y
            if letter.image == self.image_dict['-']:
                letter.rect.y += 7
                letter.rect.x += 2


    def create_coin_counter(self):
        """Creates the info that tracks the number of coins Mario collects"""
        self.coin_count_images = []
        self.create_label(self.coin_count_images, '*00', 300, 55)


    def create_flashing_coin(self): #<- OverheadInfo.__init__
        """Creates the flashing coin next to the coin total"""
        self.flashing_coin = flashing_coin.Coin(280, 53)    #->　flasing_coin.py    #创造了flasin_coin.Coin实例


    def create_mario_image(self):   #<- OverheadInfo.__init__
        """Get the mario image"""
        self.life_times_image = self.get_image(75, 247, 6, 6)   #*
        self.life_times_rect = self.life_times_image.get_rect(center=(378, 295))    #*号放在游戏界面的(378,295)
        self.life_total_label = []
        self.create_label(self.life_total_label, str(self.total_lives), # ^ life_total_label,Character列表，'lives',rect显示参数都设置好了
                          450, 285)

        self.sprite_sheet = setup.GFX['mario_bros'] #sprite_sheet改变为'mario_bros'
        self.mario_image = self.get_image(178, 32, 12, 16)  #mario: normal_small_right
        self.mario_rect = self.mario_image.get_rect(center=(320, 290))  #设置好显示mario,*,lives,界面中的mario位置


    def create_game_over_label(self):   #<- OverheadInfo.__init__
        """Create the label for the GAME OVER screen"""
        game_label = []
        over_label = []

        self.create_label(game_label, 'GAME', 280, 300)
        self.create_label(over_label, 'OVER', 400, 300)

        self.game_over_label = [game_label, over_label]


    def create_time_out_label(self):
        """Create the label for the time out screen"""
        time_out_label = []

        self.create_label(time_out_label, 'TIME OUT', 290, 310)
        self.time_out_label = [time_out_label]


    def create_main_menu_labels(self):
        """Create labels for the MAIN MENU screen"""
        player_one_game = []
        player_two_game = []
        top = []
        top_score = []

        self.create_label(player_one_game, '1 PLAYER GAME', 272, 360)
        self.create_label(player_two_game, '2 PLAYER GAME', 272, 405)
        self.create_label(top, 'TOP - ', 290, 465)
        self.create_label(top_score, '000000', 400, 465)

        self.main_menu_labels = [player_one_game, player_two_game,
                                 top, top_score]

    #多个state都会调用的函数
    def update(self, level_info, mario=None):   #<- (game_info)-main_menu.MENU <- tool.Control.update
        """Updates all overhead info"""
        self.mario = mario  #None
        self.handle_level_state(level_info)

    #多个state都会调用的函数
    def handle_level_state(self, level_info):   #<- 1.(level_info)-info.update <- (game_info)-main_menu.MENU.update <- tool.Control.update 2.self.update <- LoadScreen.update
        """Updates info based on what state the game is in"""
        if self.state == c.MAIN_MENU:   #初始state是MAIN_MENU
            self.score = level_info[c.SCORE]
            self.update_score_images(self.score_images, self.score)
            self.update_score_images(self.main_menu_labels[3], self.top_score)
            self.update_coin_total(level_info)
            self.flashing_coin.update(level_info[c.CURRENT_TIME])

        elif self.state == c.LOAD_SCREEN:   #
            self.score = level_info[c.SCORE]
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == c.LEVEL: #初始情况？
            self.score = level_info[c.SCORE]
            self.update_score_images(self.score_images, self.score) #(score_image)-字符Character实例列表
            if level_info[c.LEVEL_STATE] != c.FROZEN \
                    and self.mario.state != c.WALKING_TO_CASTLE \
                    and self.mario.state != c.END_OF_LEVEL_FALL \
                    and not self.mario.dead:    #???
                self.update_count_down_clock(level_info)
            self.update_coin_total(level_info)
            self.flashing_coin.update(level_info[c.CURRENT_TIME])

        elif self.state == c.TIME_OUT:
            self.score = level_info[c.SCORE]
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == c.GAME_OVER:
            self.score = level_info[c.SCORE]
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == c.FAST_COUNT_DOWN:
            level_info[c.SCORE] += 50
            self.score = level_info[c.SCORE]
            self.update_count_down_clock(level_info)
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)
            self.flashing_coin.update(level_info[c.CURRENT_TIME])
            if self.time == 0:
                self.state = c.END_OF_LEVEL

        elif self.state == c.END_OF_LEVEL:
            self.flashing_coin.update(level_info[c.CURRENT_TIME])


    def update_score_images(self, images, score):   #<- (score_image,self.score)-handle_level_state <- (level_info)-info.update <- (game_info)-main_menu.MENU <- tool.Control.update
        """Updates what numbers are to be blitted for the score"""
        index = len(images) - 1

        for digit in reversed(str(score)):  #从后往前修改，所以仅修改了images中score占的长度
            rect = images[index].rect
            images[index] = Character(self.image_dict[digit])
            images[index].rect = rect
            index -= 1


    def update_count_down_clock(self, level_info):  #<- update_count_down_clock <- (level_info)-info.update <- (game_info)-main_menu.MENU <- tool.Control.update
        """Updates current time"""
        if self.state == c.FAST_COUNT_DOWN: #???
            self.time -= 1

        elif (level_info[c.CURRENT_TIME] - self.current_time) > 400:    #？？？
            self.current_time = level_info[c.CURRENT_TIME]
            self.time -= 1
        self.count_down_images = []
        self.create_label(self.count_down_images, str(self.time), 645, 55)
        if len(self.count_down_images) < 2: #以下未深究，设置显示在游戏主屏幕的时间位置等
            for i in range(2):
                self.count_down_images.insert(0, Character(self.image_dict['0']))
            self.set_label_rects(self.count_down_images, 645, 55)
        elif len(self.count_down_images) < 3:
            self.count_down_images.insert(0, Character(self.image_dict['0']))
            self.set_label_rects(self.count_down_images, 645, 55)


    def update_coin_total(self, level_info):
        """Updates the coin total and adjusts label accordingly"""
        self.coin_total = level_info[c.COIN_TOTAL]

        coin_string = str(self.coin_total)
        if len(coin_string) < 2:
            coin_string = '*0' + coin_string
        elif len(coin_string) > 2:
            coin_string = '*00'
        else:
            coin_string = '*' + coin_string

        x = self.coin_count_images[0].rect.x
        y = self.coin_count_images[0].rect.y

        self.coin_count_images = []

        self.create_label(self.coin_count_images, coin_string, x, y)


    def draw(self, surface):    #1.<- (surface)-Menu.update <- tool.Control.update  2.<- LoadScreen.update
        """Draws overhead info based on state"""
        if self.state == c.MAIN_MENU:
            self.draw_main_menu_info(surface)
        elif self.state == c.LOAD_SCREEN:
            self.draw_loading_screen_info(surface)
        elif self.state == c.LEVEL:
            self.draw_level_screen_info(surface)
        elif self.state == c.GAME_OVER:
            self.draw_game_over_screen_info(surface)
        elif self.state == c.FAST_COUNT_DOWN:
            self.draw_level_screen_info(surface)
        elif self.state == c.END_OF_LEVEL:
            self.draw_level_screen_info(surface)
        elif self.state == c.TIME_OUT:
            self.draw_time_out_screen_info(surface)
        else:
            pass



    def draw_main_menu_info(self, surface): #<- self.draw <- (surface)-Menu.update <- tool.Control.update
        """Draws info for main menu"""
        for info in self.score_images:  #character实例列表，画上分数
            surface.blit(info.image, info.rect)

        for label in self.main_menu_labels: #"one player game, two player game,top score"
            for letter in label:    #character实例列表
                surface.blit(letter.image, letter.rect)

        for character in self.coin_count_images:    #Character实例列表，画上金币图像
            surface.blit(character.image, character.rect)

        for label in self.label_list:   #"Mario,world,time,1-1"
            for letter in label:    #character实例
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect) #上方闪烁的金币


    def draw_loading_screen_info(self, surface):    #<- self.draw <- LoadScreen.update
        """Draws info for loading screen"""
        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for word in self.center_labels: #加载画面"world 1-1"
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for word in self.life_total_label:  #生命数
            surface.blit(word.image, word.rect)

        surface.blit(self.mario_image, self.mario_rect) #mario图像
        surface.blit(self.life_times_image, self.life_times_rect)   #乘号

        for character in self.coin_count_images:    #Character实例列表，画上金币图像
            surface.blit(character.image, character.rect)

        for label in self.label_list:   #"Mario,world,time,1-1"
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect) #上方闪烁的金币


    def draw_level_screen_info(self, surface):
        """Draws info during regular game play"""
        for info in self.score_images:  #分数character列表
            surface.blit(info.image, info.rect)

        for digit in self.count_down_images:    #时间character对象列表
                surface.blit(digit.image, digit.rect)

        for character in self.coin_count_images:    #金币character对象列表
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)


    def draw_game_over_screen_info(self, surface):
        """Draws info when game over"""
        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for word in self.game_over_label:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)


    def draw_time_out_screen_info(self, surface):
        """Draws info when on the time out screen"""
        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for word in self.time_out_label:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)









