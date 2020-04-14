from .ExternalItem import ExternalItem


class FunctionItem(ExternalItem):
    """
    Un item de menú que llama a funciones python
    """
    def __init__(self, text, function, args=None, kwargs=None, menu=None, should_exit=False):
        """
        :param function: la función que se llamará
        :param args: una lista opcional de argumentos para pasar a la función
        :param kwargs: un diccionario opcional de argumentos de palabras clave para pasar a la función
        """
        super(FunctionItem, self).__init__(text=text, menu=menu, should_exit=should_exit)

        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}

        # el valor devuelto por la función, Ninguno si aún no se ha invocado.
        self.return_value = None

    def action(self):
        self.return_value = self.function(*self.args, **self.kwargs)

    def get_return(self):
        """
        :return: el valor de retorno de la llamada a la función
        """
        return self.return_value
