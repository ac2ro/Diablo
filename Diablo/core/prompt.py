from rgbprint import gradient_print

import datetime , random , os , re , shutil , platform , string


from requests import post as reqpost



from ipaddress import ip_address

PLATFORM = platform.system()


if PLATFORM == 'Windows':

    from ctypes import windll

    kernel32 = windll.kernel32


TERMINAL_WIDTH = shutil.get_terminal_size().columns




ACCEPTED = ['yes' , 'y' , 'true']
DENIED = ['no' , 'n' , 'false']

class Colors:

    PURPLE = '\001\033[0;38;5;141m\002'

    BLUE = '\001\033[0;38;5;12m\002'

    MAIN = '\001\033[38;5;85m\002'
    GREEN = '\001\033[38;5;82m\002'
    GRAY = '\033[90m'
    NAME = '\001\033[38;5;228m\002'
    ORANGE = '\001\033[0;38;5;214m\002'
    RED = ORANGE
    FAIL = '\001\033[1;91m\002'
    LRED = '\001\033[0;38;5;196m\002'
    BOLD = '\001\033[1m\002'
    UNDERLINE = '\001\033[4m\002'
    UNSTABLE = '\001\033[5m\002'
    END = '\001\033[0m\002'

    GRAD_BEGIN = 0xf70202
    GRAD_END = 0xf76802
    


    INFO = f'{PURPLE}Info{END}'
    WARN = f'{ORANGE}Warning{END}'
    IMPORTANT = f'{ORANGE}Important{END}'
    FAILED = f'{RED}Fail{END}'
    ERR = f'{LRED}Error{END}'
    DEBUG = f'{ORANGE}Debug{END}'
    CHAT =f'{BLUE}Chat{END}'
    GRN_BUL = f'[{GREEN}*{END}]'


def _get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")
    


class Patterns:

    WEBHOOK = 'https://discord.com/api/webhooks/\d{5,20}/[a-zA-Z0-9\_\-]+'



class RavePrompt:

    SEPERATOR = '═'

    @staticmethod
    def vert(text, **kwargs):
        # Modified Vert From Terminut.

        log_message = f"{Colors.GRAY}{_get_time()}{Colors.END} {Colors.GRAY}[{Colors.END} {Colors.RED}{text}{Colors.END} {Colors.GRAY}]{Colors.END}"


        for index, (key, value) in enumerate(kwargs.items()):
            
            prefix = f"\t ├" if index < len(kwargs) - 1 else f"\t └"



            line = f"{prefix} {key} {Colors.GRAY}:{Colors.END} {Colors.RED}{value}{Colors.END}"


            log_message += f"\n{line}"
            
        print(log_message)

    @staticmethod

    def print_seperator():

        gradient_print(RavePrompt.SEPERATOR * TERMINAL_WIDTH , start_color=Colors.GRAD_BEGIN , end_color=Colors.GRAD_END)

    
    @staticmethod

    def censor_content(content : str , sev = 4 , right_to_left = True):

        length = len(content)
        
        cut = round(length / sev)

        censor = '*' * cut

        return f'{ content [ : -cut ] }{censor}'  if right_to_left else f'{censor}{ content [ cut : ] }'


    @staticmethod

    def censor_email(email : str):

        spl = email.split('@')

        email_part = spl[0]

        after_part = spl[1]


        censored_email_part = RavePrompt.censor_content(email_part , sev=1.5)


        return f'{censored_email_part}@{after_part}'
    
    


    @staticmethod

    def sexy_logo():

        gradient_print(rf'''
╔╦╗  ┬  ┌─┐  ┌┐   ┬    ┌─┐
 ║║  │  ├─┤  ├┴┐  │    │ │
═╩╝  ┴  ┴ ┴  └─┘  ┴─┘  └─┘
                    hell
''', start_color = Colors.GRAD_BEGIN , end_color = Colors.GRAD_END)
        


    @staticmethod

    def clear():
        
        if PLATFORM == 'Windows':

            os.system('cls')
        else:

            os.system('clear')





    if PLATFORM == 'Windows':

        @staticmethod

        def set_title(new : str):

            kernel32.SetConsoleTitleW(new)

    
    @staticmethod

    def log(content : str):

        dt = _get_time()

        print(f'{Colors.GRAY}[{Colors.END}{Colors.RED}{dt}{Colors.END}{Colors.GRAY}]{Colors.END} {content}')



    @staticmethod

    def print_diablo(content : str):

        print(f'{Colors.GRAY}[{Colors.END}{Colors.RED}DIABLO{Colors.END}{Colors.GRAY}]{Colors.END} {content}')

    
    @staticmethod
    def ask_advanced(question : str , regexPattern : re.Pattern):
        # Wrapper for .ask

        answer = RavePrompt.ask(question , strict = True)


        found : re.Match = re.search(regexPattern , answer)


        if found:

            return found.group()
        
        else:

            RavePrompt.print_imp(f'Invalid {Colors.RED}{question}{Colors.END}.')

            return RavePrompt.ask_advanced(question , regexPattern)


    @staticmethod

    def print_prefix(prefix : str , content : str , nl = False):
        if not nl:
            print(f'{Colors.GRAY}[{Colors.END}{Colors.RED}{prefix}{Colors.END}{Colors.GRAY}]{Colors.END} {content}')
        else:
            print(f'\n{Colors.GRAY}[{Colors.END}{Colors.RED}{prefix}{Colors.END}{Colors.GRAY}]{Colors.END} {content}')


    @staticmethod

    def print_imp(content : str):

        print(f'{Colors.GRAY}({Colors.END}{Colors.RED}!!{Colors.END}{Colors.GRAY}){Colors.END} {content}')

    
    @staticmethod

    def print_min(content : str):
        print(f'{Colors.GRAY}({Colors.END}{Colors.RED}-{Colors.END}{Colors.GRAY}){Colors.END} {content}')
    

    @staticmethod

    def print_plus(content : str):

        print(f'{Colors.GRAY}({Colors.END}{Colors.RED}+{Colors.END}{Colors.GRAY}){Colors.END} {content}')

    
    @staticmethod

    def print_mult(content : str):

        print(f'{Colors.GRAY}({Colors.END}{Colors.RED}*{Colors.END}{Colors.GRAY}){Colors.END} {content}')



    @staticmethod

    def ask(question : str , strict = True):
        try:
            answer = input(f'{Colors.GRAY}({Colors.END}{Colors.RED}?{Colors.END}{Colors.GRAY}){Colors.END} {question} {Colors.GRAY}»{Colors.END} ')
            if answer.strip() == '' and strict:

                return RavePrompt.ask(question)
            
            else:

                return answer

        except (KeyboardInterrupt):

            RavePrompt.print_prefix('Exit' , f'Goodbye!' , nl = True)

            exit(0)
    
    @staticmethod

    def better_text(text : str):

        return text.capitalize().replace('-' , ' ')
    
    @staticmethod

    def elapsed_detailed(start : float , end : float):


        diff = end - start

        minutes = diff / 60


        return f'{diff:.3}s ({minutes:.1f}m)'
    


    @staticmethod
    def combine_lines_clean(lines):

        return '\n'.join( [ RavePrompt.clean_string(line) for line in lines ] )
    
    @staticmethod

    def weeb_print(content : str):

        print(f'{Colors.GRAY}({Colors.END}{Colors.RED}キッド{Colors.END}{Colors.GRAY}){Colors.END} {content}')

    

    @staticmethod

    def get_random_string_secure(length):

        chars = string.ascii_letters + string.digits + '!#$%'

        rand_str = ''.join(random.choice(chars) for i in range(length))
	    
        return rand_str
    


    # From the Villain C2 Framework.


    @staticmethod
    def clean_string(input_string):

        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

        input_string = ansi_escape.sub('', input_string)
        
   
        printable_chars = list(range(0x20, 0x7F)) + [0x09, 0x0A, 0x0D]

        input_string = ''.join(filter(lambda x: ord(x) in printable_chars, input_string))
        
        return input_string

    @staticmethod

    def is_valid_ip(ip : str):


        try:

            ip_object = ip_address(ip)


            return True

        except ValueError:

            return False


    @staticmethod


    def ask_yes_no(question : str):


        answer = RavePrompt.ask(f'{question}?')

        if answer in ACCEPTED:

            return True
        
        elif answer in DENIED:

            return False
        
        else:
            RavePrompt.print_min(f'Invalid {Colors.ORANGE}Option{Colors.END}.')
            return RavePrompt.ask_yes_no(question)
        





    @staticmethod

    def check_if_webhook_alive(webhook : str):



        try:

            req = reqpost(webhook , json = {'content' : 'geng'})


            return req.status_code == 200 or req.status_code == 204

        except:

            return False
    
