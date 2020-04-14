import curses
from .MenuItem import MenuItem
from ..utils import clear_terminal


class ExternalItem(MenuItem):
    """
    Una clase base para elementos que necesitan hacer cosas en la consola fuera del modo maldiciones.
    Establece el terminal nuevamente en modo estándar hasta que se realiza la acción.
    Probablemente debería ser subclase.
    """
    def __init__(self, text, menu=None, should_exit=False):
        super(ExternalItem, self).__init__(text=text, menu=menu, should_exit=should_exit)

    def set_up(self):
        """

        """
        self.menu.pause()
        curses.def_prog_mode()
        clear_terminal()
        self.menu.clear_screen()

    def clean_up(self):
        """

        """
        self.menu.clear_screen()
        curses.reset_prog_mode()
        curses.curs_set(1)
        curses.curs_set(0)
        self.menu.resume()
