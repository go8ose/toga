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
        self.update()
        w.app = self
        w.show()

    # Get selected table item, find the window, close it.
    def do_close(self, widget, **kwargs):
        selection = self.table_open_windows.selection
        if selection == None:
            return
        window_name = selection.open_windows
        w = self.windows[window_name]
        w['state'] = 'closed'
        self.update()
        w['window'].close()


    def do_focus(self, widget, **kwargs):
        selection = self.table_open_windows.selection
        if selection == None:
            return
        window_name = selection.open_windows
        w = self.windows[window_name]
        if w['state'] != 'open':
            return

        w['window'].focus()

    def do_reopen(self, widget, **kwargs):
        '''Re-open a closed window'''
        selection = self.table_closed_windows.selection
        if selection == None:
            return
        window_name = selection.closed_windows
        w = self.windows[window_name]

        assert w['state'] == 'closed'

        w['window'].show()
        w['state'] = 'open'
        self.update()

    def update(self):
        '''Update what is displayed in the tables, and enable/disable some
        buttons as appropriate'''
        self.table_open_windows.data.clear()
        self.table_closed_windows.data.clear()
        for (name, w) in self.windows.items():
            assert w['state'] in ('open', 'closed')
            if w['state'] == 'open':
                self.table_open_windows.data.append(name)
            elif w['state'] == 'closed':
                self.table_closed_windows.data.append(name)

        # enable/disable the top box buttons, for open windows
        if len([w for w in self.windows.values() if w['state'] == 'open']) == 0:
            self.btn_close.enabled = False
            self.btn_focus.enabled = False
        else:
            self.btn_close.enabled = True
            self.btn_focus.enabled = True

        # enable/disable the bottom box buttons, for closed windows
        if len([w for w in self.windows.values() if w['state'] == 'closed']) == 0:
            self.btn_reopen.enabled = False
        else:
            self.btn_reopen.enabled = True

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(self.name)
        self.windows = dict()

        # Buttons next to the open windows table
        btn_style = Pack(flex=1)
        self.btn_new = toga.Button('New Window', on_press=self.do_new, style=btn_style)
        self.btn_close = toga.Button('Close Window', on_press=self.do_close, style=btn_style)
        self.btn_focus = toga.Button('Focus Window', on_press=self.do_focus, style=btn_style)
        open_btn_box = toga.Box(
            children=[
                self.btn_new,
                self.btn_close,
                self.btn_focus,
            ],
            style=Pack(direction=COLUMN)
        )

        # Buttons next to the close windows table
        self.btn_reopen = toga.Button('Re-Open Window', on_press=self.do_reopen, style=btn_style)
        closed_btn_box = toga.Box(
            children=[
                self.btn_reopen,
            ],
            style=Pack(direction=COLUMN)
        )

        self.table_open_windows = toga.Table(['Open Windows'])
        self.table_closed_windows = toga.Table(['Closed Windows'])

        top_box = toga.Box()
        top_box.style.direction = ROW
        top_box.add(self.table_open_windows)
        top_box.add(open_btn_box)

        bottom_box = toga.Box()
        bottom_box.style.direction = ROW
        bottom_box.add(self.table_closed_windows)
        bottom_box.add(closed_btn_box)

        # Outermost box
        outer_box = toga.Box(
            children=[top_box, bottom_box],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10,
                width=500,
                height=200
            )
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        self.update()

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
