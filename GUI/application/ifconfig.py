from subprocess import run, PIPE
import re


def get_ip_addresses_str():
    return ' - '.join(get_ip_addresses())


def get_ip_addresses():
    try:
        pat = re.compile('^(\w+):.*$\n\s*inet\s+(\d+\.\d+\.\d+.\d+)',
                         re.MULTILINE)
        cmd = run(['ifconfig'], stdout=PIPE, encoding='utf8').stdout
        return [f"{m.group(1)}: {m.group(2)}" for m in pat.finditer(cmd)]
    except BaseException as e:
        return ['Failed to get IP addresses']
