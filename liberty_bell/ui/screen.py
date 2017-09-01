import pygame

from liberty_bell.ui.pygame_ui import Reel

WIN_SIZE = (800, 480)

POS = [(100, 100), (258, 100), (416, 100)]
REEL_SIZE = (128, 300)

class Liberty_Bell_Screen(object):

    def __init__(self):

        self._screen = pygame.display.set_mode(WIN_SIZE)
        self._screen.fill(pygame.Color(255,255,255))

        pygame.display.init()
        pygame.display.flip()

        self.reels = [None, None, None]

    def set_reel_image(self, reel_number, image):

        self.reels[reel_number] = Reel(image, self._screen, POS[reel_number], REEL_SIZE)

    def flip(self):

        pygame.display.flip()

    def update_reels(self):

        dirty_rects = []

        for reel in self.reels:
            dirty_rects.append(reel.update())

        pygame.display.update(dirty_rects)

    def is_spinning(self):
        """ Return True if any reels are still spinning """

        return any([r.is_spinning for r in self.reels])
