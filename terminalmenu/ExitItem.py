from .MenuItem import MenuItem


class ExitItem(MenuItem):
    """
    Se usa para salir del menú actual
    """

    def __init__(self, text='Exit', menu=None):
        super(ExitItem, self).__init__(text=text, menu=menu, should_exit=True)

    def show(self, index):
        self.text = 'Return to %s menu' % self.menu.parent.title if self.menu and self.menu.parent else 'Exit'
        return super(ExitItem, self).show(index)
