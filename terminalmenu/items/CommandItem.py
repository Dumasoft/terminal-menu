import subprocess
from terminalmenu.items.ExternalItem import ExternalItem


class CommandItem(ExternalItem):
    """
    Un item de menú para ejecutar un comando de consola.
    """
    def __init__(self, text, command, arguments=None, menu=None, should_exit=False):
        super(CommandItem, self).__init__(text=text, menu=menu, should_exit=should_exit)

        self.command = command
        self.arguments = [] if arguments else []

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
        return self.exit_status
