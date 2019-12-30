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

    def __init__(self, widget, info_text, root_window):
        tk.Frame.__init__(self)

        self.text = tk.Label(self, text=info_text, background='yellow')
        self.text.grid(column=0, row=0, sticky='EW')

        self.widget = widget
        self.root = root_window

    @log.log_function
    def bind_to_widget(self):
        """
        Bind entry and exit to the widget, so that the tooltip is activated
        on rollover.
        """
        self.widget.bind('<Enter>', self.display_widget)

    @log.log_function
    def display_widget(self, event, xtime=2000):
        """
        Display the text label on rollover of a widget.
        """
        before_show = tk.IntVar()
        # Variable to cause gui to wait for xtime seconds before showing the
        # tool tip.
        self.widget.after(xtime, before_show.set, 1)
        self.widget.wait_variable(before_show)

        widget_x1, widget_y1 = self.widget.winfo_rootx(), \
                               self.widget.winfo_rooty()
        widget_x2, widget_y2 = widget_x1+self.widget.winfo_width(), \
                               widget_y1 + self.widget.winfo_height()
        # Get widget corner positions.

        cursor_x, cursor_y = self.root.winfo_pointerx(), \
                             self.root.winfo_pointery()

        if all([cursor_x>=widget_x1, cursor_y>=widget_y1,
                cursor_x<=widget_x2, cursor_y<=widget_y2]):
            # Ensure cursor is still in the widget.
            self.place(in_=self.widget, y=-20, anchor='n',
                       bordermode="outside")
            # Place at cursor tip location.
            self.widget.bind('<Leave>', self.remove)
            # Now bind leave widget for when to remove tooltip.


    @log.log_function
    def remove(self, event):
        """
        Remove the text label after rollover.
        """
        self.place_forget()


    @log.log_function
    def display_text(self):
        """
        Display data over text in tab.
        """
        pass