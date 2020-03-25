from .MenuItem import MenuItem


class ExitItem(MenuItem):
    """
    
    """
    def __init__(self, text='Salir', menu=None):
        super(ExitItem, self).__init__(text=text, menu=menu, should_exit=True)

    def show(self, index):
        self.text = f'Regresar al menu {self.menu.parent.title}' if self.menu and self.menu.parent else 'Salir'
        return super(ExitItem, self).show(index)
