import curses

from terminalmenu.items.MenuItem import MenuItem
from terminalmenu.utils.clear_terminal import clear_terminal


class ExternalItem(MenuItem):
    """
    Una clase base para elementos que necesitan hacer cosas en la consola fuera del modo cursor.
    Establece el terminal nuevamente en modo estándar hasta que see realiza la acción.
    """

    def __init__(self, text, menu=None, should_exit=False):
        super(ExternalItem, self).__init__(text=text, menu=menu, should_exit=should_exit)

    def set_up(self):
        self.menu.pause()
        curses.def_prog_mode()
        clear_terminal()
        self.menu.clear_screen()

    def clean_up(self):
        self.menu.clear_screen()
        curses.reset_prog_mode()
        curses.curs_set(1)
        curses.curs_set(0)
        self.menu.resume()
