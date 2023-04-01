import pygame
import os

from settings import *
from laser import Laser


# super() from "enemy" and "Player" init
class Vererber:
    def __init__(self, game):
        self.game = game
        self.health = 100
        self.damage = damage
        self.mpl = max_projectile_lasers
        self.lasers = []
        self.fire = shot
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.speed = speed
        self.width = width
        self.height = height
        self.w_rec = w_rec
        self.h_rec = h_rec
        self.offset_y = offset_y
        self.offset_x = offset_x
        self.h_laser = h_laser
        self.enemyColor = enemyColor
        self.playerColor = playerColor
        self.laser_time = 0
        self.current_time = 0
        self.speedreduction = speedreduction
        self.cooldown = cooldown
        self.tmp = pygame.image.load(os.path.abspath('placeholderX.png'))
        self.sprite = pygame.transform.scale(self.tmp, (2 * self.w_rec, 2 * self.h_rec))
        self.imrect = self.sprite.get_rect()
        self.imrect.y = self.height - 4 * self.h_rec
        self.create_image_checker = False
        self.state = 0
        self.bar_height = bar_height
        self.bg_bar = pygame.Rect(self.imrect.x, self.imrect.y, self.imrect.width, self.bar_height)
        self.bar = pygame.Rect(self.imrect.x, self.imrect.y, self.imrect.width, self.bar_height)
        self.bar.width = self.imrect.width
        self.bar.x = self.imrect.x

    # changes the color depending on the entities damage
    def color_changer(self):
        if self.health == 100:
            self.game.playerColor = self.playerColor
        elif self.health <= 60:
            self.game.playerColor = "yellow"
        elif self.health <= 20:
            self.game.playerColor = "orange"

    # changes the damage-sprite depending on the impact-location
    def create_image(self, type):
        if self.create_image_checker:
            try:
                tmp = pygame.image.load(os.path.abspath(str(type) + str(self.state) + ".png"))
            except FileNotFoundError:
                tmp = pygame.image.load(os.path.abspath(placeholderX.png"))
            sprite = pygame.transform.scale(tmp, (2 * self.w_rec, 2 * self.h_rec))
            imrect = sprite.get_rect()
            imrect.y = self.imrect.y
            imrect.x = self.imrect.x
            self.sprite = sprite
            self.imrect = imrect
        self.create_image_checker = False

    # Cooldown
    def recharge(self):
        if self.fire and self.health > 0:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.laser_time >= self.cooldown:
                self.fire = False

    # entity shoots
    def shoot(self):
        if len(self.lasers) < self.mpl and not self.fire and self.health > 0 and self.game.ready:
            self.lasers.append(Laser(self.game, self.imrect.centerx, self.imrect.centery))
            self.fire = True
            self.laser_time = pygame.time.get_ticks()

    # entity gets damage
    def get_damage(self):
        self.health -= self.damage

    # entity gets health
    def get_health(self):
        if self.health + self.damage <= 100:
            self.health += self.damage
            self.bar.width += self.damage
