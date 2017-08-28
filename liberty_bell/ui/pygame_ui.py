from __future__ import division
import os
import random

import pygame
from pygame.locals import *

main_dir = os.path.dirname(os.path.abspath(__file__))

RPM = 90
FPS = 60

class ReelStepper(object):

    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.steps_remaining = 0

    def set_target(self, pos, tgt, revs=0):

        if tgt == pos:
            # Target is the same as current position
            offset = 0
        elif tgt > pos:
            # Target is after the current position
            offset = tgt - pos
        elif tgt < pos:
            # Target is after next revolution
            offset = (self.total_steps - pos) + tgt

        self.steps_remaining = revs * (self.total_steps) + offset

        print "sr=%i pos=%i tgt=%i revs=%i" % (self.steps_remaining, pos, tgt, revs)

    def step(self, steps):

        steps = steps

        if self.steps_remaining <= 0:
            raise ValueError("Steps remaining cannot be negative")
        elif self.steps_remaining <= steps:
            steps = self.steps_remaining

        self.steps_remaining -= steps

        return steps # Actual steps taken



class Reel(object):
    def __init__(self, reel_image, screen, screen_loc, view_size):

        self.reel_image = reel_image
        self.screen = screen
        self.screen_loc = screen_loc
        self.view_size = view_size


        self.orig_image = None

        self.orig_h = None
        self.orig_w = None

        self.image = None

        self.reel_stepper = None
        self.is_spinning = False


        self.rect = Rect((0, 0), self.view_size)
        self.screen_rect = Rect(screen_loc, self.view_size)
        self.screen_surface = self.screen.subsurface(self.screen_rect)

        self.load_img()
        self.extend_img()

    def load_img(self):

        #image_file = os.path.join(main_dir, filename)
        image = self.reel_image.image

        mode = image.mode
        size = image.size
        data = image.tobytes()
        self.orig_image = pygame.image.fromstring(data, size, mode)

        #self.orig_image = pygame.image.load(image_file).convert()

    def extend_img(self):
        """ Increase the size of the image to make infinite scrolling easier """

        # Determine the size of the image
        self.orig_w, self.orig_h = self.orig_image.get_size()

        # Create surface twice as large
        self.image = pygame.Surface((self.orig_w, self.orig_h * 2))

        # Repeat the image
        self.image.blit(self.orig_image, (0, 0))
        self.image.blit(self.orig_image, (0, self.orig_h))

        self.row_rate = self.orig_h / (60 / RPM) / FPS
        #self.row_rate = 1
        self.reel_stepper = ReelStepper(total_steps=self.orig_h)
        print self.row_rate


    def get_view(self):

        return self.image.subsurface(self.rect)

    def scroll(self, dy=1):

        if self.rect.top + dy > self.orig_h:
            y = (self.rect.top + dy) - self.orig_h
            self.rect.topleft = (0, y) # Reset to top
        else:
            self.rect.move_ip(0, dy)

        self.blit()
        return self.screen_rect

    def blit(self):
        self.screen_surface.blit(self.get_view(), (0, 0))

    def spin(self, revolutions, stop):
        """ Spin for a certain amount of time. Duration in milliseconds """

        stop_row = self.reel_image.stop_locs[stop]

        if not self.is_spinning:
            self.reel_stepper.set_target(pos=self.rect.top, tgt=stop_row, revs=revolutions)
            self.is_spinning = True

    def update(self):
        if self.is_spinning:
            try:
                rows = self.reel_stepper.step(self.row_rate)
            except ValueError:
                print "stopping at %i" % self.rect.top
                self.is_spinning = False
                return None

            return self.scroll(dy=rows)
