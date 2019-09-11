import unittest
import gui_windows as gu
import tkinter as tk
import log


class TestWindow(unittest.TestCase):
    def test_window(self):
        """Test window creation."""
        log.log_setup()
        # Start logging.
        app = gu.MainWindow(None,'hello')
        # Creates a text window containing the word 'hello'.
        app.title('Analysis')
        app.grid_config()
        # Set up a text object widget in the grid.
        app.colourise_text(app.raw, 'snow', 'blue', 'highlight')
        # Colour the text blue with a white background and highlights.
        app.mainloop()


    def test_scrollbar(self):
        """Test the scrollbar works."""
        log.log_setup()
        # Start logging.
        app = gu.MainWindow(None,'hello'*1000)
        # Creates a text window containing the word 'hello'.
        app.title('Analysis')
        app.grid_config()
        # Set up a text object widget in the grid.
        app.text.insert(tk.END, app.raw)
        app.scrollbar()
        app.mainloop()


    def test_menu(self):
        """Test the menu works."""

        log.log_setup()
        # Start logging.
        app = gu.MainWindow(None,'hello'*1000)
        # Creates a text window containing the word 'hello'.
        app.title('Analysis')
        app.grid_config()
        # Set up a text object widget in the grid.
        app.text.insert(tk.END, app.raw)
        app.menu()
        app.mainloop()



if __name__ == '__main__':
    unittest.main()


