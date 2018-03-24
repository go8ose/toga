import toga
from toga.style import Pack
from toga.constants import COLUMN, ROW


class ExampleExtraWindowsApp(toga.App):
    # Button callback functions
    def do_new(self, widget, **kwargs):
        window_name = 'Window ' + str(len(self.windows))
        w = ExtraWindow()
        w.startup(window_name)
        self.windows[window_name] = {'state': 'open', 'window': w}
        self.update_table_contents()
        w.app = self
        self.btn_close.enabled = True
        w.show()

    def do_close(self, widget, **kwargs):
        # Get selected table item, find the window, close it.
        window_name = self.table_open_windows.selection.open_windows
        if window_name == None:
            return
        w = self.windows[window_name]
        w['state'] = 'closed'
        self.update_table_contents()
        w['window'].close()

    def update_table_contents(self):
        self.table_open_windows.data.clear()
        self.table_closed_windows.data.clear()
        for (name, w) in self.windows.items():
            assert w['state'] in ('open', 'closed')
            if w['state'] == 'open':
                self.table_open_windows.data.append(name)
            elif w['state'] == 'closed':
                self.table_closed_windows.data.append(name)

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(self.name)
        self.windows = dict()

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
