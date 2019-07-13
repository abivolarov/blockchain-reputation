ANSI_WHITE = "\u001b[37m"
ANSI_YELLOW = "\u001b[33m"
ANSI_RED = "\u001b[31m"

def info(msg):
    print("INFO:\t" + msg)

def warn(msg):
    print(ANSI_YELLOW + "WARN:\t" + msg + ANSI_WHITE)

def fatal(msg):
    print(ANSI_RED + "FATAL:\t" + msg + ANSI_WHITE)
