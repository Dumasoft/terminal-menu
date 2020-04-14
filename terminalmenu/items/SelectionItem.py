from .MenuItem import MenuItem


class SelectionItem(MenuItem):
    """

    """
    def __init__(self, text, index, menu=None):
        super(SelectionItem, self).__init__(text=text, menu=menu, should_exit=True)

        self.index = index

    def get_return(self):
        return self.index
