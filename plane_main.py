#! /usr/bin/python3
import pygame

from plane_sprites import *

# 我们定义的事件，要大于等于  pygame.USEREVENT ，比这个值小的事件，pygame 自己使用了
ENEMY_ID = pygame.USEREVENT

# 英雄发射子弹的事件 ID
HERO_FIRE_ID = ENEMY_ID + 1

# 定时切换英雄图片的事件 ID
HERO_IMAGE_ID = HERO_FIRE_ID + 1


class PlaneGame(object):
    def __init__(self):

        pygame.init()
        # 设置游戏屏幕大小，并返回 屏幕对象, 游戏界面，宽 600 高 800
        self.screen = pygame.display.set_mode(SCREEN_SIZE.size)
        # 3. 创建游戏时钟对象
        self.clock = pygame.time.Clock()

        # 创建精灵，和精灵组
        self.__create_sprite()

        # 添加  一秒出现一架敌机的机件
        pygame.time.set_timer(ENEMY_ID, 1000)
        # 每隔 0.5 秒发射一次子弹
        pygame.time.set_timer(HERO_FIRE_ID, 500)
        # 每隔 200 毫秒 切换一张图片
        pygame.time.set_timer(HERO_IMAGE_ID, 200)

    def __create_sprite(self):

        bg_1 = BackGroundSprite()
        bg_2 = BackGroundSprite(True)
        self.bg_group = pygame.sprite.Group(bg_1, bg_2)

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        self.hero = HeroSprite()
        self.hero_group = pygame.sprite.Group(self.hero)

        # 正在发生爆炸的敌机组,
        self.destory_group = pygame.sprite.Group()

    def start_game(self):
        while True:
            # 1. 设置刷新率
            self.clock.tick(60)
            # 2. 事件监听
            self.__event_handler()

            # 3. 碰撞检测
            self.__check_collide()

            # 4. 更新精灵组
            self.__update_sprites()

            # 5.更新屏幕
            pygame.display.update()

    def __event_handler(self):

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                PlaneGame.game_over()
            if event.type == ENEMY_ID:
                # print("要出现敌机了。。。")
                enemy = EnemySprite()
                self.enemy_group.add(enemy)
            if event.type == HERO_FIRE_ID:
                self.hero.fire()
            if event.type == HERO_IMAGE_ID:
                self.hero.update_image()
                # 在此处让所有应该爆炸的敌机，更新爆炸的图片
                for enemy in self.destory_group.sprites():
                    enemy.update_image()

        # 按下按键时，不停的移动, pygame.key.get_pressed() 获得现在所有被按下的键
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            # print("左键被按下了")
            self.hero.speed = -2
        elif pressed_keys[pygame.K_RIGHT]:
            # print("右键被按下了")
            self.hero.speed = 2
        else:
            self.hero.speed = 0

    def __check_collide(self):

        # 检测子弹精灵组和 敌机 精灵组的碰撞, 返回值是发生碰撞的敌机和子弹组成的 字典
        ret = pygame.sprite.groupcollide(self.enemy_group, self.hero.bullet_group, False, True)
        if len(ret) > 0:
            for enemy in ret.keys():
                # print(enemy)
                enemy.is_over = True
                enemy.update_image()
                # 将被打中的敌机从 敌机组中 删除 ，同时加入，正在爆炸的敌机组
                self.enemy_group.remove(enemy)
                self.destory_group.add(enemy)

        # 检测英雄和敌机的碰撞
        enemy_list = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemy_list) > 0:
            # 英雄被撞，
            self.hero.is_over = True
            # print(enemy_list)
            # PlaneGame.game_over()

    def __update_sprites(self):
        # 更新背景
        # bg_group.update() 执行时，会调用 bg_group 中所有的精灵的 update 方法
        self.bg_group.update()
        # draw 方法 ，会将 bg_group 中所有的精灵 blit 到 screen 上
        self.bg_group.draw(self.screen)

        # 更新敌机精灵组
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        # 刷新英雄 
        self.hero_group.update()
        self.hero_group.draw(self.screen)

        # 更新子弹
        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)

        self.destory_group.update()
        self.destory_group.draw(self.screen)

    @staticmethod
    def game_over():
        pygame.quit()
        # 内置函数 ，结束程序
        exit()


if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()
