import pygame
from settings import *
import Player
import enemy
import random
import threading
import time
from shield import Shield


class Game:
    def __init__(self):
        self.on = on  # Game is set to ON
        self.ready = ready  # Is level ready?
        pygame.init()
        self.width = width
        self.height = height
        self.w_rec = w_rec  # width of the rectangle
        self.offset_y = offset_y  # y-Offset
        self.h_rec = h_rec  # height of the rectangle
        self.offset_x = self.w_rec // self.width  # x Offset
        self.health = health
        self.shielded = shielded
        self.playerColor = playerColor
        self.enemyColor = enemyColor
        self.player = Player.Player(self)  # initializing player
        self.valueCoins = valueCoins  # value of coins
        self.enemies = []
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption("spacefighter-2D")
        self.timer = pygame.time.Clock()
        self.difficulty = difficulty
        self.fps = fps
        self.galaxy = pygame.image.load("galaxy.png")
        self.tmp = pygame.image.load("coins.png")
        self.coins_image = pygame.transform.scale(self.tmp, (40, 40))
        self.shield = Shield(self)
        self.shield_active = active
        self.damage = damage

    # Screen updates
    def update_screen(self):
        pygame.display.flip()
        self.timer.tick(self.fps)

    def closing_q(self):  # tmp
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit()

    # Reset Player
    def reset_player(self):
        if self.player.state == 3:
            self.player.coins = 0
            self.player.state -= 1

        elif self.player.state < 3:
            self.player.coins = 0
            self.player.state = 0

        self.playerColor = self.player.playerColor
        self.player.health = self.health
        self.player.create_image_checker = True
        self.player.bar.width = self.player.imrect.width
        self.player.create_image("player")

    # Enemies will be spawned in a grid pattern
    def spawn_enemy(self):
        for row_index, row in enumerate(range(self.difficulty + 2)):
            for col_index, col in enumerate(range(self.difficulty)):
                self.enemies.append(enemy.Enemy(self, row_index * 80 + self.offset_x, col_index * 80 + self.offset_y))
                self.reset_player()  # resets the player
        self.ready = True

    def enemies_collision(self):
        while self.on and self.ready:
            time.sleep(0.01)
            for enemy0 in self.enemies:
                if self.player.lasers is not None:
                    # for Player(laser):
                    for laser in self.player.lasers:
                        if pygame.Rect.colliderect(enemy0.imrect, laser.rec1):
                            enemy0.get_damage()
                            enemy0.bar.width -= (enemy0.bar.width / 80) * self.damage

                            # Damage-sprites will be changed
                            if enemy0.imrect.centerx > laser.rec1.centerx and enemy0.state == 0:
                                enemy0.create_image_checker = True
                                enemy0.state = 1

                            elif enemy0.imrect.centerx < laser.rec1.centerx and enemy0.state == 0:
                                enemy0.create_image_checker = True
                                enemy0.state = 2

                            elif enemy0.state == 2 and enemy0.imrect.centerx > laser.rec1.centerx:
                                enemy0.create_image_checker = True
                                enemy0.state = 3

                            elif enemy0.state == 1 and enemy0.imrect.centerx < laser.rec1.centerx:
                                enemy0.create_image_checker = True
                                enemy0.state = 3

                            else:

                                self.player.lasers.remove(laser)

                    # for Enemy: will be deleted when enemies > 1
                    if enemy0.health <= 0 and len(self.enemies) > 1:
                        self.enemies.remove(enemy0)
                        self.player.coins += self.valueCoins
                        self.player.get_health()

                # connects on break and deletes the last enemy + spawn_enemy(...)
                if (len(self.enemies) == 1 and self.enemies[0].health <= 0) or self.player.health <= 0:
                    self.enemies.clear()
                    self.player.health = 100
                    self.ready = False
                    self.spawn_enemy()
                    continue

    # Game will be started in a loop
    def run(self):
        while self.on:
            pygame.mouse.set_visible(False)
            self.closing_q()
            self.screen.blit(self.galaxy, (0, 0))
            self.screen.blit(self.coins_image, (10, 10))
            
            # functions of the player will be executed
            self.player.run_and_draw()
            self.shield.run()

            # for all enemies: if dead --> will be deleted
            for enemy0 in self.enemies:
                if enemy0.health == 0 and len(self.enemies) > 1:
                    self.enemies.remove(enemy0)
                enemy0.draw()
                
                # loop will be stopped to reroute an Error
                if (len(self.enemies) <= 1 and enemy0.health <= 0) or self.player.health <= 0:
                    break
                
                # random enemy shoots
                try:
                    self.enemies[(random.randint(-len(self.enemies), -1))].shoot()
                except NotImplementedError:
                    pass

                if self.enemies is not None:
                    # for enemy(Laser):
                    for laser in enemy0.lasers:
                        if pygame.Rect.colliderect(self.shield.rect_sprite, laser.rec2) and self.shield_active:
                            self.shield.bar.width -= (self.shield.rect_sprite.width / 100) * self.damage
                            enemy0.lasers.remove(laser)
                            self.shield.get_damage()
                        if pygame.Rect.colliderect(self.player.imrect, laser.rec2):
                            self.player.get_damage()

                            self.player.bar.width -= (self.player.imrect.width / 100) * self.damage

                            # Damage-sprites will be changed for the player
                            if self.player.imrect.centerx > laser.rec2.centerx and self.player.state == 0 and \
                                    self.player.health <= 60:
                                self.player.create_image_checker = True
                                self.player.state = 1

                            elif self.player.imrect.centerx < laser.rec2.centerx and self.player.state == 0 and \
                                    self.player.health <= 60:
                                self.player.create_image_checker = True
                                self.player.state = 2

                            elif self.player.state == 2 and self.player.imrect.centerx > laser.rec2.centerx and \
                                    self.player.health <= 20:
                                self.player.create_image_checker = True
                                self.player.state = 3

                            elif self.player.state == 1 and self.player.imrect.centerx < laser.rec2.centerx and \
                                    self.player.health <= 20:
                                self.player.create_image_checker = True
                                self.player.state = 3

                            else:
                                pass

                            enemy0.lasers.remove(laser)
            self.update_screen()


# Spiel wird gestartet und ausgeführt + spawnen der Gegner
if __name__ == "__main__":
    game = Game()
    thread2 = threading.Thread(target=game.enemies_collision, daemon=True)
    game.enemies.append(enemy.Enemy(game, 0, 0))
    game.ready = True
    thread2.start()
    game.run()
