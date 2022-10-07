import pygame
import random

from models import Spaceship, Asteroid
from utils import load_sprite, get_random_position, print_text, load_highscore, save_highscore, load_sound

#Windows sizes
width = 960
height = 1109

#Colors
red = (255, 0, 0)
green = (0, 255, 0)
bright_green = (0, 200, 0)
purple = (255, 0, 255)
black = (0, 0, 0)

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((width, height))
        self.background = load_sprite("space_default", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.score = 0
        self.high_score = load_highscore()
        self.playing = False
        self.running = True
        self.game_pause = False
        self.dead = False
        self.options_screen = False
        self.intro = True
        self.checkmark_pos_background = (250, 370)
        self.checkmark_pos_rocket = (250, 580)
        self.checkmark_pos_asteroid = (250, 800)
        self.asteroid_type = "asteroid_default"

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((width // 2, height // 2), self.bullets.append)

        self.create_random_asteroids()

    def create_random_asteroids(self):
        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append, asteroid=self.asteroid_type))

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _draw(self):
        #Set background
        self.screen.blit(self.background, (0, 0))

        #Set Score counter on screen
        font = pygame.font.SysFont('Time New Roman', 24)
        score = font.render('Score: ' + str(self.score), False, green)
        scoreRect = score.get_rect()
        scoreRect.center = (width // 2, 50)
        self.screen.blit(score, scoreRect)

        #Draw every object on screen
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def game_options(self):
        self.options_screen = True

        while self.options_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()

            self.screen.fill(black)

            # Options title
            font = pygame.font.SysFont('Time New Roman', 60)
            title = font.render('Options', False, green)
            titleRect = title.get_rect()
            titleRect.center = (480, 100)
            self.screen.blit(title, titleRect)

            # Background choice
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            background = font.render('Choose background', False, green)
            backgroundRect = background.get_rect()
            backgroundRect.center = (480, 200)
            self.screen.blit(background, backgroundRect)

            # Background Choice 1
            background_def = pygame.image.load("assets/sprites/space_default.png")
            background_def_rescaled = pygame.transform.scale(background_def, (100, 100))
            background_def_rescaled_Rect = background_def_rescaled.get_rect()
            background_def_rescaled_Rect.center = (250, 300)
            self.screen.blit(background_def_rescaled, background_def_rescaled_Rect)

            # Background Choice 2
            background_choice_1 = pygame.image.load("assets/sprites/space_option_2.png")
            background_c1_rescaled = pygame.transform.scale(background_choice_1, (100, 100))
            background_c1_rescaled_Rect = background_c1_rescaled.get_rect()
            background_c1_rescaled_Rect.center = (480, 300)
            self.screen.blit(background_c1_rescaled, background_c1_rescaled_Rect)

            # Background Choice 3
            background_choice_2 = pygame.image.load("assets/sprites/space_option_3.png")
            background_c2_rescaled = pygame.transform.scale(background_choice_2, (100, 100))
            background_c2_rescaled_Rect = background_c2_rescaled.get_rect()
            background_c2_rescaled_Rect.center = (710, 300)
            self.screen.blit(background_c2_rescaled, background_c2_rescaled_Rect)

            # Check Mark 1
            checkmark = pygame.image.load("assets/sprites/check-mark.png")
            checkMarkRect = checkmark.get_rect()
            checkMarkRect.center = self.checkmark_pos_background

            if 300 > mouse[0] > 200 and 350 > mouse[1] > 250:
                if click[0] == 1:
                    self.background = background_def
                    self.checkmark_pos_background = (250, 370)
            elif 530 > mouse[0] > 430 and 350 > mouse[1] > 250:
                if click[0] == 1:
                    self.background = background_choice_1
                    self.checkmark_pos_background = (480, 370)
            elif 760 > mouse[0] > 660 and 350 > mouse[1] > 250:
                if click[0] == 1:
                    self.background = background_choice_2
                    self.checkmark_pos_background = (710, 370)

            self.screen.blit(checkmark, checkMarkRect)

            # Spacecraft choice
            spaceship = font.render('Choose spaceship', False, green)
            spaceshipRect = spaceship.get_rect()
            spaceshipRect.center = (480, 450)
            self.screen.blit(spaceship, spaceshipRect)

            # Spacecraft choice 1
            spaceship_def = pygame.image.load("assets/sprites/default_rocket.png")
            spaceship_def_rescaled = pygame.transform.scale(spaceship_def, (75, 75))
            spaceship_def_rescaled_Rect = spaceship_def_rescaled.get_rect()
            spaceship_def_rescaled_Rect.center = (250, 520)
            self.screen.blit(spaceship_def_rescaled, spaceship_def_rescaled_Rect)

            # Spacecraft choice 2
            spaceship_def = pygame.image.load("assets/sprites/rocket_option_1.png")
            spaceship_def_rescaled = pygame.transform.scale(spaceship_def, (75, 75))
            spaceship_def_rescaled_Rect = spaceship_def_rescaled.get_rect()
            spaceship_def_rescaled_Rect.center = (480, 520)
            self.screen.blit(spaceship_def_rescaled, spaceship_def_rescaled_Rect)

            # Spacecraft choice 3
            spaceship_def = pygame.image.load("assets/sprites/rocket_option_2.png")
            spaceship_def_rescaled = pygame.transform.scale(spaceship_def, (75, 75))
            spaceship_def_rescaled_Rect = spaceship_def_rescaled.get_rect()
            spaceship_def_rescaled_Rect.center = (710, 520)
            self.screen.blit(spaceship_def_rescaled, spaceship_def_rescaled_Rect)

            # Check Mark 2
            checkmark2 = checkmark.copy()
            checkMark_2_Rect = checkmark2.get_rect()
            checkMark_2_Rect.center = self.checkmark_pos_rocket

            if 285 > mouse[0] > 215 and 555 > mouse[1] > 495:
                if click[0] == 1:
                    self.spaceship = None
                    self.spaceship = Spaceship((width // 2, height // 2), self.bullets.append, "default_rocket")
                    self.checkmark_pos_rocket = (250, 580)
            elif 513 > mouse[0] > 448 and 557 > mouse[1] > 484:
                if click[0] == 1:
                    self.spaceship = None
                    self.spaceship = Spaceship((width // 2, height // 2), self.bullets.append, "rocket_option_1")
                    self.checkmark_pos_rocket = (480, 580)
            elif 740 > mouse[0] > 680 and 558 > mouse[1] > 482:
                if click[0] == 1:
                    self.spaceship = None
                    self.spaceship = Spaceship((width // 2, height // 2), self.bullets.append, "rocket_option_2")
                    self.checkmark_pos_rocket = (710, 580)

            self.screen.blit(checkmark2, checkMark_2_Rect)

            # Asteroid choice
            asteroid = font.render('Choose asteroids', False, green)
            asteroidRect = asteroid.get_rect()
            asteroidRect.center = (480, 650)
            self.screen.blit(asteroid, asteroidRect)

            # Asteroid choice 1
            asteroid_def = pygame.image.load("assets/sprites/asteroid_default.png")
            asteroid_def_Rect = asteroid_def.get_rect()
            asteroid_def_Rect.center = (250, 730)
            self.screen.blit(asteroid_def, asteroid_def_Rect)

            # Asteroid choice 2
            asteroid_def = pygame.image.load("assets/sprites/asteroid_option_1.png")
            asteroid_def_Rect = asteroid_def.get_rect()
            asteroid_def_Rect.center = (480, 730)
            self.screen.blit(asteroid_def, asteroid_def_Rect)

            # Asteroid choice 3
            asteroid_def = pygame.image.load("assets/sprites/asteroid_option_2.png")
            asteroid_def_Rect = asteroid_def.get_rect()
            asteroid_def_Rect.center = (710, 730)
            self.screen.blit(asteroid_def, asteroid_def_Rect)

            # Check Mark 3
            checkmark3 = checkmark.copy()
            checkMark_3_Rect = checkmark3.get_rect()
            checkMark_3_Rect.center = self.checkmark_pos_asteroid

            if 297 > mouse[0] > 202 and 775 > mouse[1] > 680:
                if click[0] == 1:
                    self.asteroids.clear()
                    self.asteroid_type = "asteroid_default"
                    self.create_random_asteroids()
                    self.checkmark_pos_asteroid = (250, 800)
            elif 526 > mouse[0] > 433 and 775 > mouse[1] > 682:
                if click[0] == 1:
                    self.asteroids.clear()
                    self.asteroid_type = "asteroid_option_1"
                    self.create_random_asteroids()
                    self.checkmark_pos_asteroid = (480, 800)
            elif 757 > mouse[0] > 662 and 776 > mouse[1] > 681:
                if click[0] == 1:
                    self.asteroids.clear()
                    self.asteroid_type = "asteroid_option_2"
                    self.create_random_asteroids()
                    self.checkmark_pos_asteroid = (710, 800)

            self.screen.blit(checkmark3, checkMark_3_Rect)

            # Exit button
           # print(pygame.mouse.get_pos())

            if 545 > mouse[0] > 413 and 965 > mouse[1] > 930:
                start = font.render('Return', False, bright_green)
                if click[0] == 1:
                    self.options_screen = False
                    self.intro = True
                    pygame.time.wait(100)
                    self.game_intro()
            else:
                start = font.render('Return', False, red)

            startRect = start.get_rect()
            startRect.center = (480, 950)
            self.screen.blit(start, startRect)
            pygame.display.update()
            self.clock.tick(60)

    def game_intro(self):
        print("Game intro!")
        self.intro = True

        while self.intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(black)

            # Title
            font = pygame.font.SysFont('Time New Roman', 60)
            title = font.render('Asteroids Game', False, green)
            titleRect = title.get_rect()
            titleRect.center = (480, 150)
            self.screen.blit(title, titleRect)

            # Options Button
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if 560 > mouse[0] > 397 and 370 > mouse[1] > 330:
                options = font.render('Options', False, bright_green)
                if click[0] == 1:
                    self.intro = False
                    pygame.time.wait(100)
                    self.game_options()
            else:
                options = font.render('Options', False, red)

            optionsRect = options.get_rect()
            optionsRect.center = (480, 350)
            self.screen.blit(options, optionsRect)

            # High Score
            high = font.render('High Score: ' + str(self.high_score), False, purple)
            highRect = high.get_rect()
            highRect.center = (480, 550)
            self.screen.blit(high, highRect)

            # Start Button
            if 350 + 258 > mouse[0] > 350 and 715 + 60 > mouse[1] > 715:
                start = font.render('Click to Start', False, bright_green)
                if click[0] == 1:
                    self.intro = False
                    self.game_loop()
            else:
                start = font.render('Click to Start', False,
                                    ((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

            startRect = start.get_rect()
            startRect.center = (480, 750)
            self.screen.blit(start, startRect)
            pygame.display.update()
            self.clock.tick(60)

    def unpaused(self):
        self.game_pause = False

    def paused(self):
        self.game_pause = True

        while self.game_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(black)

            # Title
            font = pygame.font.SysFont('Time New Roman', 60)
            title = font.render('Game is Paused', False, green)
            titleRect = title.get_rect()
            titleRect.center = (480, 150)
            self.screen.blit(title, titleRect)

            # Current score
            high = font.render('Current score: ' + str(self.score), False, purple)
            highRect = high.get_rect()
            highRect.center = (480, 550)
            self.screen.blit(high, highRect)

            # Start Button
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()


            if 350 + 258 > mouse[0] > 350 and 715 + 60 > mouse[1] > 715:
                start = font.render('Resume', False, bright_green)
                if click[0] == 1:
                    self.game_loop()
            else:
                start = font.render('Resume', False, red)

            startRect = start.get_rect()
            startRect.center = (480, 750)
            self.screen.blit(start, startRect)
            pygame.display.update()
            self.clock.tick(60)

    def death_screen(self):
        pygame.mixer.music.stop()
        self.dead = True

        while self.dead:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(black)

            # Title
            font = pygame.font.SysFont('Time New Roman', 60)
            title = font.render('Game Over', False, green)
            titleRect = title.get_rect()
            titleRect.center = (480, 150)
            self.screen.blit(title, titleRect)

            # Current score
            cur = font.render('Reached score: ' + str(self.score), False, purple)
            curRect = cur.get_rect()
            curRect.center = (480, 350)
            self.screen.blit(cur, curRect)

            # High Score
            high = font.render('High Score: ' + str(self.high_score), False, purple)
            highRect = high.get_rect()
            highRect.center = (480, 550)
            self.screen.blit(high, highRect)

            # Start Button
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if 350 + 258 > mouse[0] > 350 and 715 + 60 > mouse[1] > 715:
                start = font.render('Want to play again?', False, bright_green)
                if click[0] == 1:
                    pygame.mixer.music.load("assets/sounds/background_music.mp3")
                    pygame.mixer.music.play(-1)
                    self.__init__()
            else:
                start = font.render('Want to play again?', False, red)

            startRect = start.get_rect()
            startRect.center = (480, 750)
            self.screen.blit(start, startRect)
            pygame.display.update()
            self.clock.tick(60)

    def game_loop(self):
        self.high_score = load_highscore()

        #Play background music while playing
        pygame.mixer.music.load("assets/sounds/background_music.mp3")
        pygame.mixer.music.play(-1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        while True:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.mixer.music.pause()
                    self.game_paused = True
                    self.paused()
                elif (
                        self.spaceship
                        and event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE
                ):
                    self.spaceship.shoot()

            is_key_pressed = pygame.key.get_pressed()

            if self.spaceship:
                if is_key_pressed[pygame.K_RIGHT]:
                    self.spaceship.rotate(clockwise=True)
                elif is_key_pressed[pygame.K_LEFT]:
                    self.spaceship.rotate(clockwise=False)
                if is_key_pressed[pygame.K_UP]:
                    self.spaceship.accelerate()

            for game_object in self._get_game_objects():
                game_object.move(self.screen)

            if self.spaceship:
                for asteroid in self.asteroids:
                    if asteroid.collides_with(self.spaceship):
                        print_text(self.screen, "You lost!", self.font)
                        self.spaceship = None
                        pygame.time.wait(1000)
                        self.death_screen()
                        break

            for bullet in self.bullets[:]:
                for asteroid in self.asteroids[:]:
                    if asteroid.collides_with(bullet):
                        self.score += 1
                        self.asteroids.remove(asteroid)
                        self.bullets.remove(bullet)
                        asteroid.split(self.asteroid_type)
                        break

            for bullet in self.bullets[:]:
                if not self.screen.get_rect().collidepoint(bullet.position):
                    self.bullets.remove(bullet)

            if not self.asteroids and self.spaceship:
                self.message = "You won!"

            if self.score > self.high_score:
                save_highscore(self.score)

            self._draw()

        pygame.quit()