"""Main execution file."""
import log
import gui_windows as gu
import gui_startscreen as sc
import spacy as sp

log.log_setup()
# Start logging.

print('test')

sph = sc.StartScreen(None)
sph.title('Loading...')
sph.iconbitmap(r'icons//clay_icon.ico')
sph.start_grid_config()
sph.update()

import gui_windows as gu
sph.update()
#sph.after(3000, start_mainscreen)

core = sp.load("en_core_web_md")
# Load in the medium sized dataset (may take a moment).

sph.destroy()

app = gu.MainWindow(None, core)
# Creates an empty text window.

app.title('clay')
app.iconbitmap(r'icons//clay_icon.ico')

app.grid_config()
# Set up a text object widget in the grid.
app.menu()
app.mainloop()