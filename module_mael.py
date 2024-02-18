# =============================================================================
#   Made by MAEL
#   Collection of functions used in main module
# =============================================================================

import colorama
from colorama import Fore, Style
colorama.init()

from datetime import datetime

# Format printed message with timestamp and coloroma color based on message type.
def message(string, type="normal"):
    string = "{} {}".format(timeNow(), string)
    dict={
    "normal":Style.RESET_ALL + string,
    "info":Fore.CYAN + string + Style.RESET_ALL,
    "warning":Fore.YELLOW + string + Style.RESET_ALL,
    "error":Fore.RED + string + Style.RESET_ALL
    }
    print(dict.get(type))
    
# Return time (HH:MM:SS:NN).
def timeNow():
    return "{0:0>2}:{1:0>2}:{2:0>2}.{3:0>6}".format(datetime.now().hour, datetime.now().minute, datetime.now().second, datetime.now().microsecond) 