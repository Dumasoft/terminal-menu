class MenuItem(object):
    """
    Item menú genérico.
    """
    def __init__(self, text, menu=None, should_exit=False):
        """
        :param text: el texto que se muestra para este elemento del menú
        :param menu: el menú al que pertenece este elemento
        :param should_exit: si el menú debe salir una vez que se realiza la acción de este elemento
        """
        self.text = text
        self.menu = menu
        self.should_exit = should_exit

    def __str__(self):
        title = self.menu.title if self.menu is not None else ''
        return f'{title} {self.text}'

    def show(self, index):
        """
        Cómo se debe mostrar este elemento en el menú. Se puede anular, pero debe mantener la misma firma.
        El valor predeterminado es:
            1 - Artículo 1
            2 - Otro artículo
        :param index: el índice del elemento en la lista de elementos del menú
        :return: la representación del elemento que se mostrará en un menú
        """
        return f'{index + 1} - {self.text}'

    def set_up(self):
        pass

    def action(self):
        pass

    def clean_up(self):
        pass

    def get_return(self):
        """
        Anular para cambiar lo que devuelve el artículo.
        De lo contrario, solo devuelve el mismo valor que el último elemento seleccionado.
        """
        return self.menu.returned_value
