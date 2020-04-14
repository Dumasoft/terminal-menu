import subprocess
from .ExternalItem import ExternalItem


class CommandItem(ExternalItem):
    """
    Item del menú que ejecuta comandos de consola.
    """
    def __init__(self, text, command, arguments=None, menu=None, should_exit=False):
        """
        :param command: el comando de consola que se ejecutará
        :param arguments: una lista opcional de argumentos de cadena que se pasará al comando
        """
        super(CommandItem, self).__init__(text=text, menu=menu, should_exit=should_exit)

        self.command = command
        self.arguments = arguments if arguments else []

        # el estado de salida del comando, None si aún no se ha ejecutado
        self.exit_status = None

    def action(self):
        arguments = ' '.join(self.arguments)
        commandline = f'{self.command} {arguments}'

        try:
            completed_process = subprocess.run(commandline, shell=True)
            self.exit_status = completed_process.returncode
        except AttributeError:
            self.exit_status = subprocess.call(commandline, shell=True)

    def get_return(self):
        """
        :return: el estado de salida del comando
        """
        return self.exit_status
