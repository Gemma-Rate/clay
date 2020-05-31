import tkinter as tk
import log

class StartScreen(tk.Tk):
    """
    Splash screen when loading the main window.
    """

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        print('start')

    @log.log_function
    def start_grid_config(self):
        """
        Set up label and image objects in the grid.
        """
        self.master_height = 30
        self.master_width = 30

        self.grid()
        # Set grid.

        title_data = tk.Label(self.master, text="Clay", font=("Arial Bold", 50))
        title_data.grid(column=0, row=0)

        img_splash = tk.PhotoImage(file='icons//clay_icon.png')
        image_data = tk.Label(self.master, image=img_splash)
        image_data.image = img_splash
        image_data.configure(image=img_splash)
        image_data.grid(column=1, row=0)