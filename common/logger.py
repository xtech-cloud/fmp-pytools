from colorama import init

init(autoreset=True)


def trace(_msg):
    print("\033[0;34;40m{}\033[0m".format(_msg))


def debug(_msg):
    print("\033[0;36;40m{}\033[0m".format(_msg))


def info(_msg):
    print("\033[0;32;40m{}\033[0m".format(_msg))


def warn(_msg):
    print("\033[0;33;40m{}\033[0m".format(_msg))


def error(_msg):
    print("\033[0;31;40m{}\033[0m".format(_msg))


def fatal(_msg):
    print("\033[0;35;40m{}\033[0m".format(_msg))
