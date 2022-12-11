import pygame, sys, csv
from helpers import *

from world import *

from player import *
from slime import *
from dark_slime import *
from potion import *

from health_bars import *
from score import *
from crosshair import *


class Game:
    """
    This is the class that runs the game, including the actual updating of all the relevant sprites as well as the UI
    for interacting with the leaderboard. It is the most backbone of the entire game.
    """

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()

        # Next, we set up the basic pygame settings we will use
        self.my_font = pygame.font.SysFont(TEXT_FONT, TEXT_SIZE)  # The font used for the leaderboard
        self.screen = pygame.display.set_mode(SCREEN_DIM, pygame.FULLSCREEN)  # The display of the game
        #self.screen = pygame.display.set_mode((700, 700))  # A smaller screen used in development
        self.screen_dim = pygame.display.get_surface().get_size()  # Gives the screen dims, if its not full screen
        self.clock = pygame.time.Clock()  # The clock used to increase the frame number
        pygame.mouse.set_visible(False)  # Hides the mouse so it doesn't cover up the crosshair
        pygame.display.set_caption("The Dungeon")  # Sets the name of the game window

        # Creating the sprite groups
        self.foreground_sprites = CameraGroup()  # Includes: Player, Enemies, Walls
        self.background_sprites = CameraGroup()  # Includes: Floor Tiles
        self.activation_sprites = CameraGroup()  # Includes: The activation tile in the center of each room

        self.obstacle_sprites = pygame.sprite.Group()  # Includes: Walls, Gates

        self.enemy_sprites = pygame.sprite.Group()  # Includes Slimes, Dark Slimes

        self.camera_static_UI_sprites = pygame.sprite.Group()  # UI elements that don't move with the player
        self.camera_dynamic_UI_sprites = CameraGroup()  # UI elements that move with the player

        # Creating the sprites present from the start of the game
        self.player = Player(game=self, groups=[self.foreground_sprites], pos=(0, 0),
                             collision_groups=[self.obstacle_sprites])

        self.cross_hair = Crosshair(groups=[self.camera_static_UI_sprites], player=self.player,
                                    enemy_sprites=self.enemy_sprites, screen_dim=self.screen.get_size(), game=self)

        self.score_counter = ScoreCounter(game=self)

        # Initializing the leaderboard list, for when we display the leaderboard
        self.leaderboard = []

        # Creating the start of the level
        self.alive = True  # Bool recording the state of the player being alive
        self.world = World(game=self)  # Creates the world object, which stores the tiles and the world map
        self.difficulty = 0  # Initializes the difficulty of the world to 0
        self.world.create_room()
        self.enemies_remaining = -1  # A value of -1 here means that a new room is already created (see documentation)

        # Finally, we actually run the game!
        self.run()

    def run(self):
        """
        This function is what actually runs the game. It runs continually in the loop until the player dies. Then, it
        runs some code to deal with the leaderboard. If the user then clicks "R" on the leaderboard page, the game
        is reinitialized.
        """
        while self.alive:  # While the player is alive
            for event in pygame.event.get():  # Iterate through all events
                if event.type == pygame.QUIT:  # If the game was quit, we should close everything down
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # If the escape key was pressed, we should close everything down
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse was clicked, we shoot the crosshair
                    self.cross_hair.shoot()

            if self.enemies_remaining == 0:  # If the player defeats all enemies, we respond accordingly
                self.enemies_remaining = -1  # A value of -1 here means that a new room is already created (see docs)

                create_potion = random.randint(1, 3)  # Gives a 1 in 3 chance of creating a potion
                if create_potion != -1:
                    # Creates a potion object. A new room is created when the potion is drunk.
                    Potion(groups=[self.foreground_sprites], world=self.world, player=self.player,
                           cross_hair=self.cross_hair)
                else:
                    self.world.create_room()  # If the player didn't get a potion, we just create a new room.

            self.draw_game_screen()  # We run the draw_game_screen method to draw all the game sprites
            pygame.display.flip()  # We flip the display (i.e. actually show it)
            self.clock.tick(FPS)  # We tick the clock by a certain amount, to wait in between frames

        """
        The following code tuns after the player dies.
        """

        self.update_leaderboard()  # First, we update the leaderboard
        self.draw_leaderboard_screen()  # Then, we draw the leaderboard

        has_reset = False  # Then, we wait for the user to reset the game
        while not has_reset:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the game was quit, we should close everything down
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # If the escape key is pressed , we should close everything down
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:  # If the "R" key is pressed, we reinitialize
                        has_reset = True
                        self.__init__()

    def begin_attack(self):
        """
        This function is called whenever a new wave of enemies needs to be created. It initializes all the new enemies.
        """
        self.world.begin_attack()  # This method closes the gate behind the player, and removes the activation tile
        self.enemies_remaining = 0  # Initializes the number of enemies to zero

        # The following lines add the correct number of enemies of each type, as prescribed by the current difficulty
        for i in range(WAVES[self.difficulty]["slime_count"]):
            self.enemies_remaining += 1
            Slime(game=self, groups=[self.foreground_sprites, self.enemy_sprites], pos=self.player.rect.center,
                  collision_groups=[self.obstacle_sprites, self.enemy_sprites], time_before_attack=3)
        for i in range(WAVES[self.difficulty]["dark_slime_count"]):
            self.enemies_remaining += 1
            DarkSlime(game=self, groups=[self.foreground_sprites, self.enemy_sprites], pos=self.player.rect.center,
                      collision_groups=[self.obstacle_sprites, self.enemy_sprites], time_before_attack=3)

        if self.difficulty < len(WAVES) - 1:  # We increase the difficulty, if it can be increased anymore
            self.difficulty += 1

    def draw_game_screen(self):
        """
        This method draws all the sprites on the game screen in the appropriate order
        """

        # First, we update each of our sprite groups that need to be updated
        self.background_sprites.update()
        self.foreground_sprites.update()
        self.camera_dynamic_UI_sprites.update()
        self.camera_static_UI_sprites.update()

        # Then, we draw each of the sprite groups in the correct order
        self.screen.fill(BACKGROUND_COLOR)
        self.background_sprites.custom_draw(self.player)
        self.foreground_sprites.custom_draw(self.player)
        self.camera_dynamic_UI_sprites.custom_draw(self.player)

        # Finally, we draw a rectangle at the top as a backdrop for some UI elements, and then draw the UI elements.
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(0, 0, self.screen_dim[0], 60))
        self.camera_static_UI_sprites.draw(self.screen)

    def update_leaderboard(self):
        """
        This method first opens the leaderboard CSV file, and saves the rows to the leaderboard attribute. Then, it asks
        for the user's name and adds the user's name and score to the leaderboard CSV file
        """

        # This part of the code reads in the CSV file.
        rows = []  # We initialize to the empty list
        with open(LEADERBOARD_FILE_NAME, 'r') as csvfile:
            csvreader = csv.reader(csvfile)  # We create the CSV reader

            for row in csvreader:  # We add each nonempty row into our rows list
                if not len(row) == 0:
                    rows.append(row)

        name = self.get_name()  # We get the user's name
        rows.append([name, self.score_counter.score])  # We add the user's info to our list of rows
        self.leaderboard = rows[1:]  # The first row is just the names of the columns, so we ignore it
        self.leaderboard.sort(key=(lambda row: int(row[1])), reverse=True)  # Sort the leaderboard by decreasing score

        with open(LEADERBOARD_FILE_NAME, 'w') as csvfile:  # Finally, we write the now data into the CSV file
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(rows)

    def draw_leaderboard_screen(self):
        """
        This method draws the leaderboard screen. This consists of the top ten scores (including the users that got
        them) as well as some text prompting the user to press "R" to restart
        """

        self.screen.fill(BACKGROUND_COLOR)  # We fill the screen with the background color
        text_surface = self.my_font.render('LEADERBOARD', True, (255, 255, 255))  # We add a surface with header tex
        self.screen.blit(text_surface, (SPACING, SPACING))  # We blit (actually show) that surface on the screen

        displayed_entries = self.leaderboard[:10]  # We create a list with the scores we want to display
        height = TEXT_SIZE  # This sets the height of the text we are currently writing
        for idx in range(len(displayed_entries)):  # For each of the entries we want to display...
            height += TEXT_SIZE  # First, we move down another row so text doesn't overlap
            row = displayed_entries[idx]  # Then, we take out what specific row we want

            # This code defines a surface with the row of text we want to add
            text_surface = self.my_font.render(f'{idx + 1}. {row[0]}:-----------{row[1]}', True, (255, 255, 255))

            # Finally, we blit (actually show) that surface on the screen
            self.screen.blit(text_surface, (SPACING, height))

        height += 2 * TEXT_SIZE  # Skip two lines
        text_surface = self.my_font.render('PRESS \'R\' TO RESTART', True, (150, 255, 150))  # Prompt user to reset game
        self.screen.blit(text_surface, (SPACING, height))  # Actually shows the prompt on the screen

        pygame.display.flip()  # Then we show the display again

    def get_name(self):
        """
        The following code prompts the user to input their name, to display on the leaderboard. It was very inspired
        from some code on Stack Exchange for getting user text input, see README.md
        """
        name = ""  # initialize the user's name to the empty screen
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the game was quit, we should close everything down
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # If the escape key pressed, we should close everything down
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.unicode.isalnum():  # If the key was a letter/number, we add it to the name
                        if len(name) <= 10:  # We want to limit the length of the inputted name
                            name += event.unicode  # updates the name by adding the new letter
                    elif event.key == pygame.K_BACKSPACE:  # If the backspace key pressed, delete last character
                        name = name[:-1]  # updates the name by cutting off the last letter
                    elif event.key == pygame.K_RETURN:  # If the return key is pressed, we return the final name
                        return name

            # The following lines of code draw what the user sees
            self.screen.fill(BACKGROUND_COLOR)  # We fill with the background color

            # Then, we show the prompt for the user to input their name
            text_surface = self.my_font.render('ENTER NAME:', True, (255, 255, 255))  # Creates the surface
            self.screen.blit(text_surface, (SPACING, SPACING))  # Actually shows the surface on the screen

            # Then, we show what the user is typing.
            text_surface = self.my_font.render(name, True, (255, 255, 255))  # Creates the surface
            rect = text_surface.get_rect()  # Creates a rect so we can center the text
            rect.center = self.screen.get_rect().center  # Centers the rect on the screen
            self.screen.blit(text_surface, rect)  # Draws the surface where the rect is located
            pygame.display.flip()  # Flips the display so the user can see it


class CameraGroup(pygame.sprite.Group):
    """
    This group creates the effect where sprites are drawn from the top of the screen to the bottom, which makes it so
    that sprites overlap in the appropriate way. It also centers the screen on the player. It is inspired from a
    tutorial by ClearCode (see README.md)
    """
    def __init__(self):
        super().__init__()  # We initialize from the pygame sprite Group class
        self.display_surface = pygame.display.get_surface()  # We set the display

        # The following lines of code initialize the necessary variables so that we can center the camera on the player
        self.offset = pygame.math.Vector2(0, 0)
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

    def custom_draw(self, player):
        """
        This is the meat of the class. It is what actually does the drawing
        """
        # The following camera offset values make it so that the player is located at the center of the screen
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # The following loop draws each of the sprites from top to bottom, at their adjusted location.
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)

# This is the line of code that runs the actual program
if __name__ == '__main__':
    game = Game()
