from terminalmenu.items.CommandItem import CommandItem
from terminalmenu.items.SubmenuItem import SubmenuItem
from terminalmenu.items.ExitItem import ExitItem
from terminalmenu.items.SelectionItem import SelectionItem
from terminalmenu.items.FunctionItem import FunctionItem
from terminalmenu.enums.TypeItem import TypeItem
from terminalmenu.TerminalMenu import TerminalMenu


def parse_old(menu_data):
    """

    """
    menu_title = menu_data['title']
    menu = TerminalMenu(menu_title)

    for item in menu_data['options']:
        item_type = item['type']
        item_title = item['title']

        if item_type == TypeItem.COMMAND:
            item_command = item['command']
            menu.append_item(CommandItem(item_title, item_command, menu))
        elif item_type == TypeItem.FUNCTION:
            item_function = item['function']
            menu.append_item(FunctionItem(item_title, item_function, menu))
        elif item_type == TypeItem.EXITMENU:
            menu.append_item(ExitItem(item_title, menu))
        elif item_type == TypeItem.NUMBER:
            menu.append_item(SelectionItem(item_title, menu))
        elif item_type == TypeItem.MENU:
            menu.append_item(SubmenuItem(item_title, menu, parse_old(item)))

    return menu
