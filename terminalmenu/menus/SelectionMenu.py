from terminalmenu.TerminalMenu import TerminalMenu
from terminalmenu.items.SelectionItem import SelectionItem


class SelectionMenu(TerminalMenu):
    """

    """
    def __init__(self, strings, title=None, subtitle=None, show_exit_option=True):
        """

        """
        super(SelectionMenu, self).__init__(title, subtitle, show_exit_option)

        for index, item in enumerate(strings):
            self.append_item(SelectionItem(item, index, self))

    @classmethod
    def get_selection(cls, strings, title='Selecciona una opción', subtitle=None, exit_option=True, _menu=None):
        """

        """
        menu = cls(strings, title, subtitle, exit_option)

        if _menu is not None:
            _menu.append(menu)

        menu.show()
        menu.join()

        return menu.selected_option

    def append_string(self, string):
        self.append_item(SelectionItem(string))
