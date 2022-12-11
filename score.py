import pygame
from settings import *
from helpers import *


class ScoreCounter:
    """
    This class keeps track of the players score. It also creates the "digits" objects (sprites) that appear in the
    upper left of the screen to display the score.
    """

    def __init__(self, game):
        self.game = game  # We need access to the game to access appropriate groups
        self.digit_sprites = pygame.sprite.Group()  # We create a new sprite group which includes this counters digits
        self.score = 0  # We initialize the game score to 0
        self.add_to_score(0)  # This calls the "add_to_score" method, which initiates the "0 score" sprite.

    def add_to_score(self, bonus):
        """
       This method is called whenever the players score is increased (e.g. after killing enemies). The "bonus" is how
       much the score is increased by. The function updates the counter's score attribute, and if necessary adds more
       digit sprites to the display.
       """
        self.score += bonus  # First we update the score attribute

        # The following loop adds new digit sprites until we have enough sprites to display the score
        while len(self.digit_sprites) < len(str(self.score)):
            Digit(digit=len(self.digit_sprites), groups=[self.digit_sprites, self.game.camera_static_UI_sprites],
                  screen_dim=self.game.screen_dim)

        # After adding all the needed sprites, we call the update_digits method to update the digit sprites
        self.update_digits()

    def update_digits(self):
        """
        This method is called after updating the score. It just goes through each of the digit sprites, and for each
        of them it calls the reset_digit method so that that digit will show the new number it is supposed to so that
        the entire group of digits displays the correct score
        """
        for sprite in self.digit_sprites:  # For each digit sprite...
            sprite.reset_digit(str(self.score))  # We tell the digit to update to show its digit of the updated score


class Digit(pygame.sprite.Sprite):
    """
    This class describes a "Digit". That, is a single number 0-9. It contains an attribute "digit", which is the integer
    of how many digits to the left of the decimal point of the score this sprite is supposed to display. It contains a
    "reset_digit" method which causes it to display the correct digit when the score changes.
    """

    def __init__(self, digit, groups, screen_dim):
        super().__init__(groups)  # We initialize as a pygame Sprite
        self.digit = digit  # We set the digit (which digit of the number does this sprite represent)

        self.graphics = import_folder(DIGITS_FILE_PATH)  # Uploads the animation. See helpers.py
        self.image = self.graphics[0]  # initializes the image to the 0 digit.

        # The following creates the rect so that pygame knows where to draw the digit.
        # Note that later digits are drawn to the left, so the digits do not overlap.
        self.rect = self.image.get_rect(
            topright=(screen_dim[0] - SPACING - digit * (SCORE_DIGITS_DIM[0] + SPACING / 2), SPACING))

    def reset_digit(self, number):
        """
        This method is called whenever the score changes, so that each digit switches to the right graphic.
        """
        self.image = self.graphics[int(number[-(self.digit + 1)])]  # We switch to the correct graphic
        self.image = pygame.transform.scale(self.image, SCORE_DIGITS_DIM)  # We scale up the image to the desired size
