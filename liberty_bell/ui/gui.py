import os
import platform

import Tkinter as tk

from liberty_bell.components.gui_button import GUI_Button
from liberty_bell.components.gui_buzzer import GUI_Buzzer
from liberty_bell.components.gui_numeric_display import GUI_Numeric_Display


class Gui(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self, None, None)

    def initialize(self, callback):
        self.callback = callback

        frame = tk.Frame(self, pady=10)
        frame.grid(row=0, column=0, sticky=tk.E)

        embed = tk.Frame(frame, width = 800, height = 480)
        embed.grid(row=0, column=0, sticky=tk.E)

        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        if platform.system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'


        led_frame = tk.Frame(self, padx=10, pady=10)
        led_frame.grid(row=0, column=1, sticky=tk.E)

        wp_label = tk.Label(led_frame, text="Winner Paid:")
        cr_label = tk.Label(led_frame, text="Credits:")
        ab_label = tk.Label(led_frame, text="Amount Bet:")

        wp_label.grid(row=0, column=0)
        cr_label.grid(row=2, column=0)
        ab_label.grid(row=4, column=0)

        self.winner_paid_led = GUI_Numeric_Display("Winner Paid", led_frame)
        self.credits_led = GUI_Numeric_Display("Credits", led_frame)
        self.amount_bet_led = GUI_Numeric_Display("Amount Bet", led_frame)

        self.winner_paid_led.grid(row=1, column=0)
        self.credits_led.grid(row=3, column=0)
        self.amount_bet_led.grid(row=5, column=0)

        self.bind("<Up>", lambda: self.handle_input("UP"))
        self.bind("<Down>", lambda: self.handle_input("DOWN"))

        disp_frame = tk.Frame(self, padx=10, pady=10)
        disp_frame.grid(row=1, column=0)

        self.spin_button = GUI_Button(
            "Spin", disp_frame, text="Spin", command=lambda: self.callback("SPIN"))
        self.up_button = GUI_Button(
            "Up", disp_frame, text="Up", command=lambda: self.callback("UP"))
        self.down_button = GUI_Button(
            "Down", disp_frame, text="Down", command=lambda: self.callback("DOWN"))
        self.menu_button = GUI_Button(
            "Menu", disp_frame, text="Menu", command=lambda: self.callback("MENU"))

        self.reel1_button = GUI_Button(
            "Reel1", disp_frame, text="Reel 1", command=lambda: self.callback("B1"))
        self.reel2_button = GUI_Button(
            "Reel2", disp_frame, text="Reel 2", command=lambda: self.callback("B2"))
        self.reel3_button = GUI_Button(
            "Reel3", disp_frame, text="Reel 3", command=lambda: self.callback("B3"))

        self.spin_button.grid(row=2, column=3)
        self.up_button.grid(row=2, column=2)
        self.down_button.grid(row=2, column=1)
        self.menu_button.grid(row=2, column=0)

        self.reel1_button.grid(row=1, column=0)
        self.reel2_button.grid(row=1, column=1)
        self.reel3_button.grid(row=1, column=2)

        self.buzzer = GUI_Buzzer()

    def ready(self):
        self.after(0, self.run_callback)

    def schedule_next(self, requested_delay_ms):
        self.after(requested_delay_ms, self.run_callback)

    def shutdown(self):
        pass
