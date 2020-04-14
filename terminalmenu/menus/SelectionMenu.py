from ..TerminalMenu import TerminalMenu
from ..items import *


class SelectionMenu(TerminalMenu):
    """
    Un menú que simplifica la creación de elementos, solo dale una lista de cadenas y crea el menú para ti
    """
    def __init__(self, strings, title=None, subtitle=None, show_exit_option=True):
        """
        La lista de cadenas de este menú debe construirse
        """
        super(SelectionMenu, self).__init__(title, subtitle, show_exit_option)

        for index, item in enumerate(strings):
            self.append_item(SelectionItem(item, index, self))

    @classmethod
    def get_selection(cls, strings, title='Selecciona una opción', subtitle=None, exit_option=True, _menu=None):
        """
        Forma de método único de obtener una selección de una lista de cadenas
        :param strings: la lista de cadenas utilizada para construir el menú
        """
        menu = cls(strings, title, subtitle, exit_option)

        if _menu is not None:
            _menu.append(menu)

        menu.show()
        menu.join()

        return menu.selected_option

    def append_string(self, string):
        self.append_item(SelectionItem(string))
