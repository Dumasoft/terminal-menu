import threading
import curses
from terminalmenu.items import *
from terminalmenu.utils import *


class TerminalMenu(object):
    """
    Una clase que muestra un menú y permite al usuario seleccionar una opción
    :cvar TerminalMenu cls.currently_active_menu: Variable de clase que contiene el menú
    actualmente activo o Ninguno si no hay menú está actualmente activo (p. ej., al cambiar de menú)
    """
    currently_active_menu = None
    stdscr = None

    def __init__(self, title=None, subtitle=None, show_exit_option=True):
        """
        :ivar str title: El título del menú
        :ivar str subtitle: El subtítulo del menú
        :ivar bool show_exit_option: si este menú debe mostrar un elemento de salida por
        defecto. Puede ser anulado cuando se inicia el menú
        :ivar items: la lista de elementos de menú que mostrará el menú
        :ivar CursesMenu parent: El padre de este menú
        :ivar CursesMenu previous_active_menu: el menú previamente activo para ser restaurado en la
        clase menú actualmente activo
        :ivar int current_option: la opción de menú actualmente resaltada
        :ivar MenuItem current_item: El elemento correspondiente a la opción de menú que está resaltada actualmente
        :ivar int selected_option: la opción que el usuario ha seleccionado más recientemente
        :ivar MenuItem selected_item: El elemento en: attr: `items` que el usuario seleccionó más recientemente
        :ivar returned_value: el valor devuelto por el elemento seleccionado más recientemente
        :ivar screen: la ventana de maldiciones asociada con este menú
        :ivar normal: el par de colores de texto normal para este menú
        :ivar highlight: el par de colores de resaltado asociado con esta ventana
        """

        self.screen = None
        self.highlight = None
        self.normal = None

        self.title = title
        self.subtitle = subtitle
        self.show_exit_option = show_exit_option

        self.items = list()

        self.parent = None

        self.exit_item = ExitItem(menu=self)

        self.current_option = 0
        self.selected_option = -1

        self.returned_value = None

        self.should_exit = False

        self.previous_active_menu = None

        self._main_thread = None

        self._running = threading.Event()

    def __repr__(self):
        return f'{self.title}: {self.subtitle}. {len(self.items)} items'

    @property
    def current_item(self):
        return self.items[self.current_option] if self.items else None

    @property
    def selected_item(self):
        if self.items and self.selected_option != -1:
            return self.items[self.current_option]
        else:
            return None

    def append_item(self, item):
        """
        Agregue un elemento al final del menú antes del elemento de salida
        :param MenuItem item: el elemento que se va a agregar
        """
        did_remove = self.remove_exit()
        item.menu = self

        self.items.append(item)

        if did_remove:
            self.add_exit()

        if self.screen:
            max_row, max_cols = self.screen.getmaxyx()
            if max_row < 6 + len(self.items):
                self.screen.resize(6 + len(self.items), max_cols)
            self.draw()

    def add_exit(self):
        """
        Agregue el elemento de salida si es necesario. Se usa para asegurarse de que no haya varios elementos de salida
        :return: True si se necesita agregar un elemento, False de lo contrario
        """
        if self.items:
            if self.items[-1] is not self.exit_item:
                self.items.append(self.exit_item)
                return True
        return False

    def remove_exit(self):
        """
        Retire el elemento de salida si es necesario. Se usa para asegurarnos de que solo
        eliminemos el elemento de salida, no otra cosa
        :return: True si el elemento necesitaba ser eliminado, False de lo contrario
        """
        if self.items:
            if self.items[-1] is self.exit_item:
                del self.items[-1]
                return True
        return False

    def _wrap_start(self):
        curses.wrapper(self._main_loop) if self.parent is None else self._main_loop(None)

        TerminalMenu.currently_active_menu = None

        self.clear_screen()
        clear_terminal()

        TerminalMenu.currently_active_menu = self.previous_active_menu

    def start(self, show_exit_option=None):
        """
        Inicia el menú en un nuevo hilo y permita que el usuario interactúe con él.
        El hilo es un demonio, entonces: meth: `join () <cursesmenu.CursesMenu.join>` debería
        llamarse si hay una posibilidad que el hilo principal saldrá antes de que se termine el menú
        :param show_exit_option: Si se debe mostrar el elemento de salida, el valor predeterminado es
        el valor establecido en el constructor
        """

        self.previous_active_menu = TerminalMenu.currently_active_menu
        TerminalMenu.currently_active_menu = None

        self.should_exit = False

        if show_exit_option is None:
            show_exit_option = self.show_exit_option

        self.add_exit() if show_exit_option else self.remove_exit()

        try:
            self._main_thread = threading.Thread(target=self._wrap_start, daemon=True)
        except TypeError:
            self._main_thread = threading.Thread(target=self._wrap_start)
            self._main_thread.daemon = True

        self._main_thread.start()

    def show(self, show_exit_option=None):
        """
        Las llamadas comienzan y luego se unen de inmediato.
        :param show_exit_option: si se debe mostrar el elemento de salida, el valor
        predeterminado es en el constructor
        """
        self.start(show_exit_option)
        self.join()

    def _main_loop(self, scr):
        if scr is not None:
            TerminalMenu.stdscr = scr
            
        self.screen = curses.newpad(len(self.items) + 6, TerminalMenu.stdscr.getmaxyx()[1])
        self._set_up_colors()
        curses.curs_set(0)
        TerminalMenu.stdscr.refresh()
        self.draw()
        TerminalMenu.currently_active_menu = self
        self._running.set()
        
        while self._running.wait() is not False and not self.should_exit:
            self.process_user_input()

    def draw(self):
        """
        Vuelve a dibujar el menú y actualiza la pantalla. Debería llamarse cada vez que algo
        cambia que necesita ser redibujado.
        """

        self.screen.border(0)

        if self.title is not None:
            self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)

        if self.subtitle is not None:
            self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)

        for index, item in enumerate(self.items):
            text_style = self.highlight if self.current_option == index else self.normal
            self.screen.addstr(5 + index, 4, item.show(index), text_style)

        screen_rows, screen_cols = TerminalMenu.stdscr.getmaxyx()
        top_row = 0

        if 6 + len(self.items) > screen_rows:
            if screen_rows + self.current_option < 6 + len(self.items):
                top_row = self.current_option
            else:
                top_row = 6 + len(self.items) - screen_rows

        self.screen.refresh(top_row, 0, 0, 0, screen_rows - 1, screen_cols - 1)

    def is_running(self):
        """
        :return: True si el menú se inicia y no se ha detenido
        """
        return self._running.is_set()

    def wait_for_start(self, timeout=None):
        """
        Bloquear hasta que se inicie el menú
        :param timeout: cuánto tiempo esperar antes de que se agote
        :return: False si se da el tiempo de espera y la operación agota el tiempo de espera, de lo contrario, True
        """
        return self._running.wait(timeout)

    def is_alive(self):
        """
        :return: True si el hilo sigue vivo, False de lo contrario
        """
        return self._main_thread.is_alive()

    def pause(self):
        """
        Pause temporalmente el menú hasta que se llame a reanudar
        """
        self._running.clear()

    def resume(self):
        """
        Establece el menú actualmente activo en este y lo reanuda
        """
        TerminalMenu.currently_active_menu = self
        self._running.set()

    def join(self, timeout=None):
        """
        Debería llamarse en algún momento después de: meth: `start () <cursesmenu.CursesMenu.start>`
        para bloquear hasta que salga el menú.
        :param timeout: cuánto tiempo esperar antes de que se agote el tiempo de espera
        """
        self._main_thread.join(timeout=timeout)

    def get_input(self):
        """
        Se puede anular para cambiar el método de entrada.
        :return: el valor ordinal de un solo carácter
        """
        return TerminalMenu.stdscr.getch()

    def process_user_input(self):
        """
        Obtiene el siguiente caracter y decide qué hacer con él.
        """
        user_input = self.get_input()

        go_to_max = ord("9") if len(self.items) >= 9 else ord(str(len(self.items)))

        if ord('1') <= user_input <= go_to_max:
            self.go_to(user_input - ord('0') - 1)
        elif user_input == curses.KEY_DOWN:
            self.go_down()
        elif user_input == curses.KEY_UP:
            self.go_up()
        elif user_input == ord("\n"):
            self.select()

        return user_input

    def go_to(self, option):
        """
        Ir a la opción ingresada por el usuario como un número
        :param option: la opción para ir a
        """
        self.current_option = option
        self.draw()

    def go_down(self):
        """
        Baja un item en el menú al pulsar una tecla
        """
        if self.current_option < len(self.items) - 1:
            self.current_option += 1
        else:
            self.current_option = 0
        self.draw()

    def go_up(self):
        """
        Sube un item en el menú al pulsar una tecla
        """
        if self.current_option > 0:
            self.current_option += -1
        else:
            self.current_option = len(self.items) - 1
        self.draw()

    def select(self):
        """
        Seleccione el elemento actual y ejecútelo
        """
        self.selected_option = self.current_option
        self.selected_item.set_up()
        self.selected_item.action()
        self.selected_item.clean_up()
        self.returned_value = self.selected_item.get_return()
        self.should_exit = self.selected_item.should_exit

        if not self.should_exit:
            self.draw()

    def exit(self):
        """
        Señale el menú para salir, luego bloquee hasta que termine de limpiar
        """
        self.should_exit = True
        self.join()

    def _set_up_colors(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlight = curses.color_pair(1)
        self.normal = curses.A_NORMAL

    def clear_screen(self):
        """
        Borrar la pantalla que pertenece a este menú
        """
        self.screen.clear()
