import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class ExampleExtraWindowsApp(toga.App):
    # Button callback functions
    def do_new(self, widget, **kwargs):
        w = ExtraWindow()
        window_name = 'Window ' + str(len(self.extra_windows.keys()))
        self.extra_windows[window_name] = w
        self.window_list.data.insert(0, window_name)
        w.app = self
        self.btn_close.enabled = True
        w.show()

    def do_close(self, widget, **kwargs):
        # Get selected table item, find the window, close it.
        try:
            window_name = self.window_list.selection.windows
            w = self.extra_windows[window_name]
            w.close()
            # TODO: remove the window from self.window_list. Maybe add it to
            # a closed windows list?
        except AttributeError:
            # Table throws AttributeError if no selection.
            # TODO: Confirm this is really part of the API for a Table, and
            # if not raise an issue (or raise an issue about documentation)?
            pass

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(self.name)
        self.extra_windows = {}

        # Buttons
        btn_style = Pack(flex=1)
        btn_new = toga.Button('New Window', on_press=self.do_new, style=btn_style)
        self.btn_close = toga.Button('Close Window', on_press=self.do_close, style=btn_style)
        self.btn_close.enabled=False
        btn_box = toga.Box(
            children=[
                btn_new,
                self.btn_close
            ],
            style=Pack(direction=COLUMN)
        )

        self.window_list = toga.Table(['Windows'])
        # TODO: setup a handler so you can select an item, and then cause
        # focus to switch to that item. Maybe right click for a menu, or
        # double tap on it, or select it and press a third button (which
        # only displays when there is a selection?)

        # Outermost box
        outer_box = toga.Box(
            children=[self.window_list, btn_box],
            style=Pack(
                flex=1,
                direction=ROW,
                padding=10,
                width=500,
                height=300
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()

class ExtraWindow(toga.Window):
    # TODO: Add a button to switch back to main window
    # TODO: Add something that's unique to this window (maybe a random
    # number?) so when you come back to it, you know 
    # TODO: default the windo
    pass

def main():
    return ExampleExtraWindowsApp('Extra Windows', 'org.pybee.widgets.extrawindows')


if __name__ == '__main__':
    app = main()
    app.main_loop()
