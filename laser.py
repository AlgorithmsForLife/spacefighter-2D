import pygame
from settings import h_laser, w_laser, w_rec, h_rec, playerColor, enemyColor


# Laser will be initialized
class Laser:
    def __init__(self, game, lx, ly):
        self.game = game
        self.height = h_laser
        self.width = w_laser
        self.w_rec = w_rec
        self.h_rec = h_rec
        self.rec1 = pygame.Rect(lx, ly - 2 * self.h_rec, self.width, self.height)
        self.rec2 = pygame.Rect(lx, ly + 2 * self.h_rec, self.width, self.height)
        self.playerColor = playerColor
        self.enemyColor = enemyColor

    # if executed: will be drawn
    def draw(self, which):
        if which == 1:
            pygame.draw.rect(self.game.screen, self.game.playerColor, self.rec1)
        else:
            pygame.draw.rect(self.game.screen, self.game.enemyColor, self.rec2)
