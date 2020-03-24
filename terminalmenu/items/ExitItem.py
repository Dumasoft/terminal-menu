from terminalmenu.items.MenuItem import MenuItem


class ExitItem(MenuItem):
    """
    Se usa para salid del menú actual.
    """

    def __init__(self, text='Salir', menu=None):
        super(ExitItem, self).__init__(text=text, menu=menu, should_exit=True)

    def show(self, index):
        if self.menu and self.menu.parent:
            self.text = f'Regresar al menú {self.menu.parent.title}'
        else:
            self.text = 'Salir'

        return super(ExitItem, self).show(index)
