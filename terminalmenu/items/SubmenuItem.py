import curses
from .MenuItem import MenuItem


class SubmenuItem(MenuItem):
    """
    Un elemento de menú para abrir un submenú.
    """
    def __init__(self, text, submenu, menu=None, should_exit=False):
        super(SubmenuItem, self).__init__(text=text, menu=menu, should_exit=should_exit)

        # El submenú que se abrirá cuando se seleccione este elemento
        self.submenu = submenu

        if menu:
            self.submenu.parent = menu

    def set_menu(self, menu):
        """
        Establece el menú de este elemento.
        Debe usarse en lugar de acceder directamente al atributo de menú para esta clase.
        :param menu: el menú
        """
        self.menu = menu
        self.submenu.parent = menu

    def set_up(self):
        self.menu.pause()
        curses.def_prog_mode()
        self.menu.clear_screen()

    def action(self):
        self.submenu.start()

    def clean_up(self):
        self.submenu.join()
        self.menu.clear_screen()
        curses.reset_prog_mode()
        curses.curs_set(1)
        curses.curs_set(0)
        self.menu.resume()

    def get_return(self):
        """
        :return: El valor devuelto en el submenú
        """
        return self.submenu.returned_value
