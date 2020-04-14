from terminalmenu import *
from terminalmenu.items import *
from terminalmenu.menus import *


def main():
    menu = TerminalMenu('Menú de ejemplo', 'Subtítulo del menú')

    item1 = MenuItem('Item 1', menu)
    function_item = FunctionItem('Ejemplo función', input, ['Introduce un dato: '])
    command_item = CommandItem('Ejemplo comando', 'python examples/example.py')
    submenu = SelectionMenu(['item1', 'item2', 'item3'])
    submenu_item = SubmenuItem('Submenú item', submenu=submenu)
    submenu_item.set_menu(menu)
    submenu_2 = TerminalMenu('Submenú título', 'Submenú subtítulo')
    function_item_2 = FunctionItem("Función item", input, ['Introduce un dato: '])
    item2 = MenuItem('Otro Item')
    submenu_2.append_item(function_item_2)
    submenu_2.append_item(item2)
    submenu_item_2 = SubmenuItem('Otro submenu', submenu=submenu_2)
    submenu_item_2.set_menu(menu)
    menu.append_item(item1)
    menu.append_item(function_item)
    menu.append_item(command_item)
    menu.append_item(submenu_item)
    menu.append_item(submenu_item_2)

    menu.start()
    menu.join()


if __name__ == '__main__':
    main()
