import pygame
from tiles import Tile
from settings import *
from player import Player
class Level:
    def __init__(self,level_data,surface):
        self.display_surface=surface
        self.setup_level(level_data)

        self.world_shift=0


    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.winds_up= pygame.sprite.Group()
        self.winds_left = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size,'grey')
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                if cell == 'W':
                    wind_up = Tile((x, y), tile_size,'white')
                    self.winds_up.add(wind_up)
                if cell == 'A':
                    wind_left = Tile((x, y), tile_size,'white')
                    self.winds_left.add(wind_left)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False
        for sprite in self.winds_up.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.direction.y = -3
                elif player.direction.y < 0:
                    player.direction.y = -3
        for sprite in self.winds_left.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.direction.x = -8
                    player.direction.y = -0.9
                elif player.direction.y < 0:
                    player.direction.x = -8
                    player.direction.y = -0.9

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False



    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
    #def scroll_y(self):
        #player = self.player.sprite
        #player_x = player.rect.centerx
        direction_x = player.direction.x

        #if player_x < screen_height / 4 and direction_y < 0:
            ##player.speed = 0
        #elif player_x > screen_height - (screen_height / 4) and direction_y > 0:
            #self.world_shift = -8
            #player.speed = 0
        #else:
            #self.world_shift = 0
            #player.speed = 8




    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.winds_up.update(self.world_shift)
        self.winds_up.draw(self.display_surface)
        self.winds_left.update(self.world_shift)
        self.winds_left.draw(self.display_surface)

        self.scroll_x()
        self.player.update()
        self.get_player_on_ground()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
