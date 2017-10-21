import pygame

from liberty_bell.ui.pygame_ui import Reel

WIN_SIZE = (500, 400)

REEL_SIZE = (128, 300)
REEL_POS = (1, 1)
NUMBER_REELS = 3
REEL_MARGIN = 1

class Liberty_Bell_Screen(object):

    def __init__(self):

        self._screen = pygame.display.set_mode(WIN_SIZE)
        self._screen.fill(pygame.Color("slategrey"))

        pygame.display.init()
        pygame.display.flip()

        self.reels = [None, None, None]

        # Set up the reel area
        reel_box_width = REEL_SIZE[0] * NUMBER_REELS + REEL_MARGIN * (NUMBER_REELS-1)
        print "width=%i" % reel_box_width
        reel_box_height = REEL_SIZE[1]

        reel_rect = pygame.Rect(REEL_POS, (reel_box_width, reel_box_height))

        reel_border = self._screen.subsurface(reel_rect.inflate((REEL_MARGIN, REEL_MARGIN)))
        reel_border.fill(pygame.Color("burlywood3"))

        self._reel_box = self._screen.subsurface(reel_rect)
        self._reel_box.fill(pygame.Color("white"))

        pygame.display.flip()


    def set_reel_image(self, reel_number, image):
        x, y = REEL_POS
        w, h = REEL_SIZE
        x += (w + REEL_MARGIN) * reel_number

        self.reels[reel_number] = Reel(image, self._screen, (x, y), REEL_SIZE)

    def flip(self):

        pygame.display.flip()

    def update_reels(self):

        dirty_rects = []

        for reel in self.reels:
            dirty_rects.append(reel.update())

        pygame.display.update(dirty_rects)

    @property
    def is_spinning(self):
        """ Return True if any reels are still spinning """

        return any([r.is_spinning for r in self.reels])
