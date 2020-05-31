import tkinter as tk
import log

class StartScreen(tk.Tk):
    """
    Splash screen when loading the main window.
    """

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent

    @log.log_function
    def start_grid_config(self):
        """
        Set up label and image objects in the grid.
        """
        self.master_height = 150
        self.master_width = 300

        self.grid()
        # Set grid.

        title_data = tk.Label(self.master, text="Clay", font=("Arial Bold", 90))
        title_data.grid(column=0, row=0)

        img_splash = tk.PhotoImage(file='icons//start_screen_image.png')
        image_data = tk.Label(self.master, image=img_splash)
        image_data.image = img_splash
        image_data.configure(image=img_splash)
        image_data.grid(column=1, row=0)

        program_info = tk.Label(self.master, text="Created by Gemma Rate\nLicensed under MIT", font=("Arial Bold", 15))
        program_info.grid(column=0, row=1)
