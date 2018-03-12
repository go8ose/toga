import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class ExampleExtraWindowsApp(toga.App):
    # Button callback functions
    def do_new(self, widget, **kwargs):
        window_name = 'Window ' + str(len(self.extra_windows.keys()))
        w = ExtraWindow()
        w.startup(window_name)
        self.extra_windows[window_name] = w
        self.update_table_contents()
        w.app = self
        self.btn_close.enabled = True
        w.show()

    def do_close(self, widget, **kwargs):
        # Get selected table item, find the window, close it.
        try:
            window_name = self.table_open_windows.selection.open_windows
            if window_name == None:
                return
            w = self.extra_windows[window_name]
            del self.extra_windows[window_name]
            self.closed_windows[window_name] = w
            self.update_table_contents()
            w.close()
        except AttributeError:
            # Table throws AttributeError if no selection.
            # TODO: I don't think this is really meant to be part of the
            # API, I've raised https://github.com/pybee/toga/issues/401
            pass

    def update_table_contents(self):
        self.table_open_windows.data.clear()
        for i in self.extra_windows.keys():
            self.table_open_windows.data.append(i)

        self.table_closed_windows.data.clear()
        for i in self.closed_windows.keys():
            self.table_closed_windows.data.append(i)

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(self.name)
        self.extra_windows = {}
        self.closed_windows = {}

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

        self.table_open_windows = toga.Table(['Open Windows'])
        # TODO: setup a handler so you can select an item, and then cause
        # focus to switch to that item. Maybe right click for a menu, or
        # double tap on it, or select it and press a third button (which
        # only displays when there is a selection?)

        self.table_closed_windows = toga.Table(['Closed Windows'])

        window_box = toga.Box()
        window_box.style.direction = COLUMN
        window_box.add(self.table_open_windows)
        window_box.add(self.table_closed_windows)

        # Outermost box
        outer_box = toga.Box(
            children=[window_box, btn_box],
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
    def startup(self, name):
        window_index = int(name.split()[1])

        # TODO: work out why setting the position doesn't seem to work.
        self.position = (10*window_index,10*window_index)
        self.size = (110,120)

        box = toga.Box()
        self.title=name
        l = toga.Label(name)
        box.add(l)
        self.content = box


def main():
    return ExampleExtraWindowsApp('Extra Windows', 'org.pybee.widgets.extrawindows')


if __name__ == '__main__':
    app = main()
    app.main_loop()
