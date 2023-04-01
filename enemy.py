from char_0 import Vererber
import pygame
import random
import os


# inherites from Vererber(char_0.py) + init
class Enemy(Vererber):
    def __init__(self, game, index, ebene=0):
        super().__init__(game)
        self.health = 80
        self.tmp = pygame.image.load(os.path.abspath('enemy0.png'))
        self.sprite = pygame.transform.scale(self.tmp, (2 * self.w_rec, 2 * self.h_rec))
        self.imrect = self.sprite.get_rect()
        self.imrect.y = self.height - 2 * self.h_rec
        self.index = index
        self.ebene = ebene
        self.cooldown *= random.randint(1, 20)
        self.imrect.x = self.index + self.width // 9
        self.imrect.x += self.index + self.offset_x
        self.imrect.y = self.ebene
        self.imrect.y += self.ebene + self.offset_y
        self.fire = False
        self.mpl = 20
        self.bar.width = self.imrect.width

    # enemy will be drawn with ist shooten out lasers
    def draw(self):
        if self.health < 80:
            self.bar.x, self.bar.y = self.imrect.x, self.imrect.y + self.imrect.height
            self.bg_bar.x, self.bg_bar.y = self.bar.x, self.bar.y
            pygame.draw.rect(self.game.screen, "darkgrey", self.bg_bar)
            pygame.draw.rect(self.game.screen, self.enemyColor, self.bar)
            self.game.screen.blit(self.font.render(str(self.health), True, "white", None),
                                  (self.imrect.centerx - 10, self.imrect.centery + self.h_rec * 1.5))
            self.create_image("enemy")
        self.game.screen.blit(self.sprite, (self.imrect.x, self.imrect.y))
        
        # drawn the lasers
        for laser in self.lasers:
            laser.draw(2)
            laser.rec2.y += self.speed - (2 * self.state)
            if laser.rec2.y > self.height + self.h_laser:
                self.lasers.remove(laser)
        self.recharge()
