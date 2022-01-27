from colorama import Fore, Style

class Logger:
    def __init__(self, name: str = "Logger", color: Fore = Fore.GREEN):
        self.name = name
        self.color = color
        self.prefix = f"{self.color}{Style.BRIGHT}[{self.name}]{Style.NORMAL}"
        return

    def log(self, message: str, color: Fore = Fore.WHITE):
        print(f"{self.prefix} {color}{message}{Style.RESET_ALL}")

    def warn(self, message: str):
        print(f"{self.prefix} {Fore.YELLOW}{message}{Style.RESET_ALL}")
        
    def error(self, message: str):
        print(f"{self.prefix} {Style.BRIGHT}{Fore.RED}{message}{Style.RESET_ALL}")

    def ok(self, message: str):
        print(f"{self.prefix} {Fore.GREEN}{message}{Style.RESET_ALL}")   
