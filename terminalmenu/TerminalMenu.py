import curses
import os
import platform
import threading

from terminalmenu.items.ExitItem import ExitItem
from terminalmenu.utils.clear_terminal import clear_terminal


class TerminalMenu(object):
    """
    Una clase que muestra un menú y permite al usuario seleccionar una opción.
    """
    currently_active_menu = None
    stdscr = None

    def __init__(self, title=None, subtitle=None, show_exit_option=True):
        """

        :param title:
        :param subtitle:
        :param show_exit_option:
        """
        self.screen = None
        self.highlight = None
        self.normal = None

        self.title = title
        self.subtitle = subtitle
        self.show_exit_option = show_exit_option

        self.items = list()

        self.parent = None

        self.exit_item = ExitItem(menu=self)

        self.current_option = 0
        self.selected_option = -1

        self.returned_value = None

        self.should_exit = False

        self.previous_active_menu = None

        self._main_thread = None

        self._running = threading.Event()

    def __repr__(self):
        return f'{self.title} {self.subtitle}. {len(self.items)} items'

    @property
    def current_item(self):
        return self.items[self.current_option] if self.items else None

    @property
    def selected_item(self):
        return self.items[self.current_option] if self.items and self.selected_option != -1 else None

    def append_item(self, item):
        """

        """
        did_remove = self.remove_exit()
        item.menu = self
        self.items.append(item)

        if did_remove:
            self.add_exit()

        if self.screen:
            max_row, max_cols = self.screen.getmaxyx()
            if max_row < 6 + len(self.items):
                self.screen.resize(6 + len(self.items), max_cols)
            self.draw()

    def add_exit(self):
        """

        """
        if self.items:
            if self.items[-1] is not self.exit_item:
                self.items.append(self.exit_item)
                return True
        return False

    def remove_exit(self):
        """

        """
        if self.items:
            if self.items[-1] is self.exit_item:
                del self.items[-1]
                return True
        return False

    def _wrap_start(self):
        if self.parent is None:
            curses.wrapper(self._main_loop)
        else:
            self._main_loop(None)

        TerminalMenu.currently_active_menu = None
        self.clear_screen()
        clear_terminal()
        TerminalMenu.currently_active_menu = self.previous_active_menu

    def start(self, show_exit_option=None):
        """

        """
        self.previous_active_menu = TerminalMenu.currently_active_menu
        TerminalMenu.currently_active_menu = None

        self.should_exit = False

        if show_exit_option is None:
            show_exit_option = self.show_exit_option

        if show_exit_option:
            self.add_exit()
        else:
            self.remove_exit()

        try:
            self._main_thread = threading.Thread(target=self._wrap_start(), daemon=True)
        except TypeError:
            self._main_thread = threading.Thread(target=self._wrap_start)
            self._main_thread.daemon = True

        self._main_thread.start()

    def show(self, show_exit_option=None):
        """

        """
        self.start(show_exit_option)
        self.join()

    def _main_loop(self, scr):
        if scr is not None:
            TerminalMenu.stdscr = scr
        self.screen = curses.newpad(len(self.items) + 6, TerminalMenu.stdscr.getmaxyx()[1])
        self._set_up_colors()
        curses.curs_set(0)
        TerminalMenu.stdscr.refresh()
        self.draw()
        TerminalMenu.currently_active_menu = self
        self._running.set()

        while self._running.wait() is not False and not self.should_exit:
            self.process_user_input()

    def draw(self):
        """

        """
        self.screen.border(0)

        if self.title is not None:
            self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)

        if self.subtitle is not None:
            self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)

        for index, item in enumerate(self.items):
            text_style = self.highlight if self.current_option == index else self.normal
            self.screen.addstr(5 + index, 4, item.show(index), text_style)

        screen_rows, screen_cols = TerminalMenu.stdscr.getmaxyx()
        top_row = 0

        if 6 + len(self.items) > screen_rows:
            if screen_rows + self.current_option < 6 + len(self.items):
                top_row = self.current_option
            else:
                top_row = 6 + len(self.items) - screen_rows

        self.screen.refresh(top_row, 0, 0, 0, screen_rows - 1, screen_cols - 1)

    def is_running(self):
        """

        """
        return self._running.is_set()

    def wait_for_start(self, timeout=None):
        """

        """
        return self._running.wait(timeout)

    def is_alive(self):
        """

        """
        return self._main_thread.is_alive()

    def pause(self):
        """

        """
        self._running.clear()

    def resume(self):
        """

        """
        TerminalMenu.currently_active_menu = self
        self._running.set()

    def join(self, timeout=None):
        """

        """
        self._main_thread.join(timeout=timeout)

    def get_input(self):
        """

        """
        return TerminalMenu.stdscr.getch()

    def process_user_input(self):
        """

        """
        user_input = self.get_input()

        go_to_max = ord('9') if len(self.items) >= 9 else ord(str(len(self.items)))

        if ord('1') <= user_input <= go_to_max:
            self.go_to(user_input - ord('0') - 1)
        elif user_input == curses.KEY_DOWN:
            self.go_down()
        elif user_input == curses.KEY_UP:
            self.go_up()
        elif user_input == ord('\n'):
            self.select()

        return user_input

    def go_to(self, option):
        """

        """
        self.current_option = option
        self.draw()

    def go_down(self):
        """

        """
        if self.current_option < len(self.items) - 1:
            self.current_option += 1
        else:
            self.current_option = 0

        self.draw()

    def go_up(self):
        """

        """
        if self.current_option > 0:
            self.current_option += -1
        else:
            self.current_option = len(self.items) - 1

        self.draw()

    def select(self):
        """
        Selecciona el elemento actual y lo ejecuta.
        """
        self.selected_option = self.current_option
        self.selected_item.set_up()
        self.selected_item.action()
        self.selected_item.clean_up()
        self.returned_value = self.selected_item.get_return()
        self.should_exit = self.selected_item.should_exit

        if not self.should_exit:
            self.draw()

    def exit(self):
        """
        Señale el menú para salir, luego bloquee hasta que termine de limpiar
        """
        self.should_exit = True
        self.join()

    def _set_up_colors(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlight = curses.color_pair(1)
        self.normal = curses.A_NORMAL

    def clear_screen(self):
        """
        Borrar la pantalla que pertenece a este menú
        """
        self.screen.clear()
