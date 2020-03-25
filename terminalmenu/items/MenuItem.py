class MenuItem(object):
    """

    """
    def __init__(self, text, menu=None, should_exit=False):
        self.text = text
        self.menu = menu
        self.should_exit = should_exit

    def __str__(self):
        return f'{self.menu.title} {self.text}'

    def show(self, index):
        """

        """
        return f'{index + 1} {self.text}'

    def set_up(self):
        pass

    def action(self):
        pass

    def clean_up(self):
        pass

    def get_return(self):
        pass
