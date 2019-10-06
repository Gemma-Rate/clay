"""Main execution file."""
import log
import tkinter.ttk as tk
import gui_windows as gu

log.log_setup()
# Start logging.
app  = gu.MainWindow(None)
# Creates a text window containing the word 'hello'.
app.title('Analysis')
app.grid_config()
# Set up a text object widget in the grid.
app.menu()
app.mainloop()