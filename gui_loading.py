import tkinter as tk
import log
import functools

class LoadScreen(tk.Tk):
    """
    Loading screen for a function.
    """

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent

        """
        Set up label and image objects in the grid.
        """
        self.master_height = 100
        self.master_width = 150

        self.grid()
        # Set grid.

        title_data = tk.Label(self.master, text="Loading...", font=("Arial Bold", 15))
        title_data.grid(column=0, row=0)


def bar_function(fun):
    """
    Add a loading bar popup to functions.

    Parameters
    ----------
    fun : python function object
        Function input.

    """
    @functools.wraps(fun)
    def wrapper_log_function(*args, **kwargs):
        # Set up a wrapper of the function that takes args and key word
        # args.


    return wrapper_log_function