import pygame
import random

SCREEN_SIZE = pygame.Rect(0, 0, 480, 700)


class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image_url, speed=1):
        # 调用父类的 init 方法 ，初始化 Sprite
        super().__init__()

        self.image = pygame.image.load(image_url)
        self.speed = speed
        # 初始位置(0,0,width,height)
        self.rect = self.image.get_rect()

    def update(self):
        """
        重写 父类的方法 更新 位置
        :return:
        """
        self.rect.y += self.speed


class BackGroundSprite(GameSprite):
    def __init__(self, is_alt=False):
        """
        :param is_alt: 是否需要修改初始位置
        """
        super().__init__("./images/background.png")
        if is_alt:
            self.rect.y = -SCREEN_SIZE.height

    def update(self):
        super().update()
        # 当完全离开屏幕以上，那到称动到屏幕的上方
        if self.rect.y >= SCREEN_SIZE.height:
            self.rect.y = -SCREEN_SIZE.height


class EnemySprite(GameSprite):
    def __init__(self):
        # 获得到 1 -- 3 的随机数，包括 1 3
        random_speed = random.randint(1,3)
        # print("random_speed is %d" % random_speed)
        super().__init__("./images/enemy1.png", random_speed)

        # 设定水平随机位置
        self.rect.x = random.randint(0,SCREEN_SIZE.width - self.rect.width)
        # 让飞机在屏幕以外的地方开始飞进来
        self.rect.y = -self.rect.height

        self.is_over = False

        self.destory_list = []
        self.destory_index = 0

        for i in (1,2,3,4):
            self.destory_list.append(pygame.image.load("./images/enemy1_down%d.png" % i))



    # 重写父类中的方法，快捷键  ctrl + o
    def update(self):
        super().update()
        # 如果飞出了屏幕，就销毁
        if self.rect.y >= SCREEN_SIZE.height:
            # 销毁当前精灵
            self.kill()

    def update_image(self):
        """
        爆炸时的动画效果
        :return:
        """
        # 被打中后执行该动作
        if self.is_over:

            if self.destory_index == len(self.destory_list):
                # 爆炸动画完成
                self.kill()
                return

            print("当前敌机要爆炸了。。。")
            self.image = self.destory_list[self.destory_index]
            self.destory_index += 1



    def __del__(self):
        # print("敌机被销毁了...del...")
        pass


class HeroSprite(GameSprite):

    def __init__(self):
        super().__init__("./images/me1.png", 0)
        self.rect.centerx = SCREEN_SIZE.centerx
        self.rect.bottom = SCREEN_SIZE.bottom - 120

        # 创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()

        self.image2 = pygame.image.load("./images/me2.png")

        # 存储 被消灭时，显示的图片列表
        self.destory_list = []
        self.destory_index = 0
        for i in (1,2,3,4):
            self.destory_list.append(pygame.image.load("./images/me_destroy_%d.png" % i))

        # 是否被消灭
        self.is_over = False




    def update(self):
        self.rect.x += self.speed

        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.x > SCREEN_SIZE.width - self.rect.width:
            self.rect.x = SCREEN_SIZE.width - self.rect.width

    def fire(self):
        # 如果被消灭了，就不再发射子弹
        if self.is_over:
            return

        # 添加子弹的精灵,设置子弹的初始位置
        for i in (0,1,2):
            bullet = Bullet()
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.y = self.rect.y - 20 * i

            self.bullet_group.add(bullet)


    def update_image(self):
        """
        更新 飞机显示的图片，会每隔 0.2 秒执行一次
        :return:
        """

        if self.is_over:
            self.image = self.destory_list[self.destory_index]
            self.destory_index += 1

            if self.destory_index == len(self.destory_list):
                # 爆炸的动画完成，游戏结束
                pygame.quit()
                exit()

        else:
            # 要显示英雄飞机喷火的动画，只需要，让飞机，在二张图片之间不断切换即可。
            self.image, self.image2 = self.image2,self.image


class Bullet(GameSprite):

    def __init__(self):
        super().__init__("./images/bullet1.png", -3) 

    def update(self):
        super().update()
        # 如果子弹飞出屏幕，那么销毁子弹
        if self.rect.y < -self.rect.height:
            self.kill()

    def __del__(self):
        print("子弹被销毁了")
        




