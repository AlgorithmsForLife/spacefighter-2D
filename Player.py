import pygame
from char_0 import Vererber
from settings import coins


# inherites from Vererber(char_0.py) + init
class Player(Vererber):
    def __init__(self, game):
        super().__init__(game)
        self.coins = coins
        self.health = 100
        self.rec = None
        self.health_indicator = None
        self.tmp = pygame.image.load("player0.png")
        self.sprite = pygame.transform.scale(self.tmp, (2 * self.w_rec, 2 * self.h_rec))
        self.imrect = self.sprite.get_rect()
        self.imrect.y = self.height - 4 * self.h_rec
        self.shielded = self.game.shielded
        self.bar.width = self.imrect.width

    # enemy will be drawn with its shooten out lasers + player-controller
    def run_and_draw(self):
        self.bar.x, self.bar.y = self.imrect.x, self.imrect.y + self.imrect.height
        self.bg_bar.x, self.bg_bar.y = self.bar.x, self.bar.y
        pygame.draw.rect(self.game.screen, "darkgrey", self.bg_bar)
        pygame.draw.rect(self.game.screen, self.game.playerColor, self.bar)
        # changes the color according to its health
        self.color_changer()
        self.game.screen.blit(self.font.render(str(self.coins), True, "orange", None), (80, 20))

        if pygame.key.get_pressed()[pygame.K_a] and self.imrect.x > 0:
            if self.state == 0:
                self.imrect.x -= self.speed
            elif self.state == 1 or self.state == 2:
                self.imrect.x -= (self.speed - self.speedreduction)
            elif self.state == 3:
                self.imrect.x -= (self.speed - round(1.25 * self.speedreduction))

        if pygame.key.get_pressed()[pygame.K_d] and self.imrect.x < (self.width - self.imrect.width):
            if self.state == 0:
                self.imrect.x += self.speed
            elif self.state == 1 or self.state == 2:
                self.imrect.x += (self.speed - self.speedreduction)
            elif self.state == 3:
                self.imrect.x += (self.speed - round(1.25 * self.speedreduction))

        self.create_image("player")
        self.game.screen.blit(self.sprite, (self.imrect.x, self.imrect.y))

        if pygame.key.get_pressed()[pygame.K_SPACE] and self.game.ready:
            self.shoot()

        # draws th lasers
        for laser in self.lasers:
            laser.draw(1)
            laser.rec1.y -= self.speed * 2
            if laser.rec1.y < -self.h_laser:
                self.lasers.remove(laser)
        self.recharge()
