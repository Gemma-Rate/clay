"""Main execution file."""
import log
import gui_windows as gu

log.log_setup()
# Start logging.
app  = gu.MainWindow(None)
# Creates an empty text window.

app.title('clay')
app.iconbitmap(r'icons//clay_icon.ico')

app.grid_config()
# Set up a text object widget in the grid.
app.menu()
app.mainloop()