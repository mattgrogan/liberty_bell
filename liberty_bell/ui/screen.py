import pygame

from liberty_bell.ui.pygame_ui import Reel

WIN_SIZE = (800, 480)

class Liberty_Bell_Screen(object):

    def __init__(self):

        self._screen = pygame.display.set_mode(WIN_SIZE)
        self._screen.fill(pygame.Color(255,255,255))

        pygame.display.init()
        pygame.display.flip()

        self.reels = []

    def add_reel(self, image, pos, size):

        r = Reel(image, self._screen, pos, size)
        self.reels.append(r)

        r.blit()

        return r
