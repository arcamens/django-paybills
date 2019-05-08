from subprocess import check_output

def get_addr(port):
    dom = 'http://%s:8000' % check_output("lynx -dump -hiddenlinks=ignore \
    -nolist http://checkip.dyndns.org:8245/ \
    | awk '{ print $4 }' | sed '/^$/d; s/^[ \
    ]*//g; s/[ ]*$//g'", shell=True).decode('utf-8').rstrip().strip()
    return dom
