class MenuItem(object):
    """
    Clase para crear items en el menú
    """

    def __init__(self, text, menu=None, should_exit=False):
        """
        Constructor
        :param text: el texto que se muestra para este elemento del menú
        :param menu: el menú al que pertenece este elemento
        :param should_exit: si el menú debe salir una vez que se realiza la acción de este elemento
        """
        self.text = text
        self.menu = menu
        self.should_exit = should_exit

    def __str__(self):
        return '%s %s' % (self.menu.title, self.text) if self.menu is not None else self.text

    def show(self, index):
        """
        Cómo se debe mostrar este elemento en el menú. Se puede anular, pero debe mantener la misma firma.

        El valor predeterminado es:

        1. Item 1
        2. Otro item

        :param index: el índice del elemento en la lista de elementos
        :return: la representación del elemento que se mostrará en un menú
        """
        return '%d - %s' % (index + 1, self.text)

    def set_up(self):
        """
        Sobreescribir para agregar cualquier acción de configuración necesaria para el item
        """
        pass

    def action(self):
        """
        Sobreescribir para llevar a cabo la acción principal de este item
        """
        pass

    def clean_up(self):
        """
        Sobreescribir para agregar cualquier acción necesaria para limpiar el item
        """
        pass

    def get_return(self):
        """
        Sobreescribir para cambiar lo que devuelve el item. De lo contrario, solo devuelve el mismo valor que el
        último item seleccionado
        """
        return self.menu.returned_value
