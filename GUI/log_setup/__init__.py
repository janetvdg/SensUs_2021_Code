import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


def to_ansi_format(msg, use_color=True):
    if use_color:
        msg = msg.replace("$RESET", RESET_SEQ)
        msg = msg.replace("$BOLD", BOLD_SEQ)
    else:
        msg = msg.replace("$RESET", "").replace("$BOLD", "")
    return msg


class ColoredFormatter(logging.Formatter):

    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname
            levelname_color = levelname_color + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


def add_stdout_handler(log):
    fmt = '$BOLD%(name)s$RESET - %(levelname)s - $BOLD%(filename)s'
    fmt = fmt + '$RESET:%(lineno)d - %(message)s'
    fmt = to_ansi_format(fmt, True)
    sh = logging.StreamHandler()
    color_formatter = ColoredFormatter(fmt)
    sh.setLevel(logging.WARNING)
    sh.setFormatter(color_formatter)
    log.addHandler(sh)


def add_file_handler(log):
    fmt = '%(asctime)s - $BOLD%(name)s$RESET - %(levelname)s - $BOLD'
    fmt = fmt + '%(filename)s$RESET:%(lineno)d - %(message)s'
    fmt = to_ansi_format(fmt, True)
    fh = logging.FileHandler('log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    log.addHandler(fh)


def init(name='main', path='./log', safe_mode=False):
    welcome_msg = '{:#^40s}'.format(' NEW LOG SESSION ')
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    if safe_mode:
        log.debug(welcome_msg)
        return log
    add_stdout_handler(log)
    add_file_handler(log)
    log.debug(welcome_msg)
    return log
