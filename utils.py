class Color:
    def __init__(self):
        self.RED = '\033[31m'
        self.GREEN = '\033[32m'
        self.YELLOW = '\033[33m'
        self.BLUE = '\033[34m'
        self.PURPLE = '\033[35m'
        self.CYAN = '\033[36m'
        self.GREY = '\033[90m'

        self.ENDC = '\033[m'
        self.BOLD = '\033[01m'
        self.UNDERLINE = '\033[04m'
        self.REVERSE = '\033[07m'
        self.STRIKETHROUGH = '\033[09m'


def input_yes_no(txt):
    clr = Color()
    while True:
        try:
            txt = f'\n{txt} (Enter \'y\' or \'n\'): {clr.ENDC}'
            opt = str(input(txt))
            
            if opt == 'y': return True
            elif opt == 'n': return False
            else: input(f'{clr.RED}Invalid option! Press enter to continue...{clr.ENDC}')

        except: 
            input(f'{clr.RED}Invalid option! Press enter to continue...{clr.ENDC}')
            continue


def input_number(txt, range = None, type = 'int'):
    clr = Color()
    while True:
        try:
            prompt = f'\n{txt}: {clr.ENDC}'
            number = str(input(prompt))

            if  number == 'c': return None
            else: 
                if type == 'int': number = int(number)
                elif type == 'float': number = float(number)

                if not None and range[0] <= number <= range[1]: return number
                else: input(f'{clr.RED}The value is not inside the range! Press enter to continue...{clr.ENDC}')

        except: 
            input(f'{clr.RED}Invalid option! Press enter to continue...{clr.ENDC}')
            continue
