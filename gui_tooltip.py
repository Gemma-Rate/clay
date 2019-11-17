"""
GUI class for hovering tooltips.
"""

import tkinter as tk
import log

class ToolTipDisplay(tk.Frame):
    """
    Container class for a tooltip display that is activated on hover.

    Public attributes
    -----------------

    Class methods
    -----------------

    """

    def __init__(self, widget, info_text):
        tk.Frame.__init__(self)

        self.text = tk.Label(self, text=info_text, background='yellow')
        self.text.grid(column=0, row=0, sticky='EW')

        self.widget = widget

    @log.log_function
    def bind_to(self):
        """
        Bind entry and exit to the widget, so that the tooltip is activated
        on rollover.
        """
        self.widget.bind('<Enter>', self.display)
        self.widget.bind('<Leave>', self.remove)

    @log.log_function
    def display(self, event, xtime=2000):
        """
        Display the text label on rollover.
        """
        before_show = tk.IntVar()
        # Variable to cause gui to wait for xtime seconds before showing the
        # tool tip.
        self.widget.after(xtime, before_show.set, 1)
        self.widget.wait_variable(before_show)

        self.place(in_=self.widget, y=-20, anchor='n',
                   bordermode="outside")
        # Place at cursor tip location.

    @log.log_function
    def remove(self, event):
        """
        Remove the text label after rollover.
        """
        self.place_forget()
