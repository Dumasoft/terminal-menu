from terminalmenu.items.ExternalItem import ExternalItem


class FunctionItem(ExternalItem):
    def __init__(self, text, function, args=None, kwargs=None, menu=None, should_exit=False):
        """
        :param text:
        :param function: La función que se llamará
        :param args: Una lista opcional de argumentos para pasar a la función
        :param kwargs: Un diccionario opcional de argumentos de palabras clave para pasar a la función.
        """
        super(FunctionItem, self).__init__(text=text, menu=menu, should_exit=should_exit)

        self.function = function

        self.args = [] if args is None else args
        self.kwargs = {} if kwargs is None else kwargs

        self.return_value = None

    def action(self):
        self.return_value = self.function(*self.args, **self.kwargs)

    def get_return(self):
        return self.return_value
