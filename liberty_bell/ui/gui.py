import Tkinter as tk

import PIL.Image as Image
import PIL.ImageTk as ImageTk

from components.gui_1306 import GUI_1306
from components.gui_1351 import GUI_1351
from components.gui_button import GUI_Button
from components.gui_buzzer import GUI_Buzzer
from components.gui_numeric_display import GUI_Numeric_Display


class Gui(tk.Tk):

  def __init__(self, controller):

    tk.Tk.__init__(self, None, None)

    self.controller = controller

    frame = tk.Frame(self, pady=10)
    frame.grid(row=1, column=0, sticky=tk.E)

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

    #self.bind("<Enter>", controller.handle_spin)
    self.bind("<Up>", controller.handle_up)
    self.bind("<Down>", controller.handle_down)

    self.blank_image = Image.new(
        "RGB", (128, 128), color="#000000")
    self.blank_image = ImageTk.PhotoImage(self.blank_image)

    disp_frame = tk.Frame(self, padx=10, pady=10)
    disp_frame.grid(row=0, column=0)

    self.display_1 = GUI_1351(disp_frame)
    self.display_2 = GUI_1351(disp_frame)
    self.display_3 = GUI_1351(disp_frame)

    self.reel_displays = [self.display_1, self.display_2, self.display_3]

    for i, disp in enumerate(self.reel_displays):
      disp.grid(row=0, column=i)

    self.menu_display = GUI_1306(frame)

    self.spin_button = GUI_Button(
        "Spin", frame, text="Spin", command=self.controller.handle_spin)
    self.up_button = GUI_Button(
        "Up", frame, text="Up", command=self.controller.handle_up)
    self.down_button = GUI_Button(
        "Down", frame, text="Down", command=self.controller.handle_down)
    self.menu_button = GUI_Button(
        "Menu", frame, text="Menu", command=self.controller.handle_menu)

    self.reel1_button = GUI_Button(
        "Reel1", disp_frame, text="Reel 1", command=self.controller.handle_b1)
    self.reel2_button = GUI_Button(
        "Reel2", disp_frame, text="Reel 2", command=self.controller.handle_b2)
    self.reel3_button = GUI_Button(
        "Reel3", disp_frame, text="Reel 3", command=self.controller.handle_b3)

    self.spin_button.grid(row=0, column=4)
    self.up_button.grid(row=0, column=3)
    self.down_button.grid(row=0, column=2)
    self.menu_button.grid(row=0, column=1)
    self.menu_display.grid(row=0, column=0)

    self.reel1_button.grid(row=1, column=0)
    self.reel2_button.grid(row=1, column=1)
    self.reel3_button.grid(row=1, column=2)

    self.buzzer = GUI_Buzzer()

    self.after(0, self.start)

  def start(self):

    requested_delay_ms = self.controller.run()
    self.after(requested_delay_ms, self.start)

  def shutdown(self):
    pass
