import pygame
from settings import shield_health, damage, shield_cooldown, bar_height
import os

class Shield:
    def __init__(self, game):
        self.game = game
        self.laser_time = 0
        self.current_time = 0
        self.cooldown = shield_cooldown
        self.tmp = pygame.image.load(os.path.abspath('shield.png'))
        self.sprite = pygame.transform.scale(self.tmp, (100, 20))
        self.rect_sprite = self.sprite.get_rect()
        self.circle = pygame.image.load(os.path.abspath('circle.png'))
        self.sprite_circle = self.circle.get_rect()
        self.health = shield_health
        self.damage = damage
        self.bar_height = bar_height
        self.bar = pygame.Rect(self.rect_sprite.x, self.rect_sprite.y, self.rect_sprite.width, self.bar_height)
        self.bg_bar = pygame.Rect(self.bar.x, self.bar.y, self.bar.width, self.bar_height)

    def get_damage(self):
        if self.health - self.damage >= 0 and self.game.shield_active:
            self.health -= self.damage

    def recharge(self):
        if self.laser_time - self.current_time >= self.cooldown:
            self.health = 100
            self.bar.width = self.rect_sprite.width
            self.game.shield_active = False
            self.game.shielded = False

    def run(self):
        if self.health < 100:
            self.bar.x, self.bar.y = self.rect_sprite.x, self.rect_sprite.y + self.bar.height * 3
            self.bg_bar.x, self.bg_bar.y = self.bar.x, self.bar.y
            pygame.draw.rect(self.game.screen, "darkgrey", self.bg_bar)
            pygame.draw.rect(self.game.screen, "lightblue", self.bar)
        x, y = pygame.mouse.get_pos()
        rect = self.sprite.get_rect()
        circ = self.circle.get_rect()
        self.sprite_circle = circ
        self.rect_sprite = rect
        self.rect_sprite.centerx = x + (self.rect_sprite.width / 2)
        self.rect_sprite.y = y + (self.rect_sprite.height / 2)

        self.sprite_circle.x = x + (self.sprite_circle.width / 2)
        self.sprite_circle.y = y + (-self.sprite_circle.height * 0.5)

        if self.game.ready and self.health == 0:
            self.game.shield_active = False
            self.game.shielded = True
            self.recharge()
            self.laser_time = pygame.time.get_ticks()

        if pygame.mouse.get_pressed()[0] and self.game.ready and self.health > 0 and not self.game.shielded:
            self.game.shield_active = True

            if self.game.shield_active:
                self.game.screen.blit(self.sprite, (pygame.mouse.get_pos()))
            self.current_time = pygame.time.get_ticks()

        elif pygame.mouse.get_focused():
            self.game.screen.blit(self.circle, (self.sprite_circle.x, self.sprite_circle.y))
            self.game.shield_active = False
