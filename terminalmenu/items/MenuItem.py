class MenuItem(object):
    """
    Clase genérica de menú item
    """

    def __init__(self, text, menu=None, should_exit=False):
        """
        :param text: El texto que se muestra para este elemento del menú
        :param menu: El menú al que pertenece este elemento
        :param should_exit: Si el menú debe salir una vez que se realiza la acción de este elemento
        """
        self.text = text
        self.menu = menu
        self.should_exit = should_exit

    def __str__(self):
        return f'{self.menu.title} {self.text}'

    def show(self, index):
        """
        Cómo se debe mostrar este elemento en el menú. Se puede anular, pero debe mantener la misma firma.
        El valor predeterminado es:
        1 - Item 1
        2 - Otro Item
        :param index: El índice del elemento en la lista de elementos del menú
        :return:
        """
        return f'{index + 1} {self.text}'

    def set_up(self):
        """
        Sobreescribir para agregar cualquier acción de configuración necesaria para el item
        """
        pass

    def action(self):
        """
        Sobreescribir para llevar a cabo la acción principal de este item.
        """
        pass

    def clean_up(self):
        """
        Sobreescribir para agregar cualquier acción de limpieza necesaria para el item
        """
        pass

    def get_return(self):
        """
        Sobreescribir para cambiar lo que devuelve el artículo.
        De lo contrario, solo devuelve el mismo valor que el último elemento seleccionado.
        """
        return self.menu.returned_value
