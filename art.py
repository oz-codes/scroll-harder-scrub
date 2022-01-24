# -*- coding: utf-8 -*-
#
import weechat
import random
import pprint
import os
import shlex,subprocess
import re

SCRIPT_NAME = "art"
SCRIPT_AUTHOR = "0"
SCRIPT_VERSION = "0"
SCRIPT_LICENSE = "WTFPL"
SCRIPT_DESC = ("send ansi files loll")


#if PY3:
unichr = chr
def send(buf, text):
    weechat.command(buf, "/input send {}".format(text))
#else:
#    def send(buf, text):
#        weechat.command(buf, "/input send {}".format(text.encode("utf-8")))

w=weechat
ARTPATH="/home/oz/git/scroll-harder-scrub/art" #change to wherever your art dir is lol
files = [
            f for f in os.listdir(ARTPATH)
            if os.path.isfile(
                "/".join([ARTPATH, f])
            )
        ]

def cb_art_cmd(data, buf, argv ):
    global ARTPATH
    global files
    file = ''
    args = argv.split(' ')
    fname = ''
    """Callback for ``/art``, do the things"""
    preview=False
    chars = []
    #if not PY3:
    #    args = args.decode("utf-8")
    #file=''
    if not args[0]: # randum!
        fname = random.choice(files)
        file = "/".join([ARTPATH,fname])
    else:
        if args[0] == 'list': #list files...
            w.prnt(buf, " ".join(files))
            return w.WEECHAT_RC_OK
        else:
            fname = " ".join(args[1:])
            file = "/".join([ARTPATH,fname])
            test=os.path.isfile(file)
            if not test:
                w.prnt(buf,"lol wtf {0} ain't no FILE!!!!".format(file))
                return w.WEECHAT_RC_ERROR
            if args[0] == 'preview': #preview lol file
                preview=True
    with open(file, 'rb') as f:
        chars=f.read().decode('utf8', errors='ignore')
    out='{2}Now playing {4}/ircart/{0}{3}\n{1}'.format(fname.split('.')[0],(chars if not preview else
           re.sub(
              r"(\x03\d+,\d+)",
              a2w,
              chars
           )),
           w.color("red"),
           w.color("chat"),
           w.color('*red')
        )
    if preview:
        w.prnt(buf,out)
    else:
        send(buf,out)
    return weechat.WEECHAT_RC_OK

def a2w(m):
    return weechat.color(m.group(1))

def art_files(data, completion_item, buffer, completion):
    global files
    w.prnt(buffer, pprint.pformat(files))
    for f in files:
        weechat.hook_completion_list_add(completion, f, 0, weechat.WEECHAT_LIST_POS_SORT)
    return w.WEECHAT_RC_OK

if __name__ == "__main__":
    weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                     SCRIPT_LICENSE, SCRIPT_DESC, '', '')
    weechat.hook_completion('art_files', 'file completions', 'art_files', '')
    weechat.hook_command("art", SCRIPT_DESC, "[play <filename> | list | preview <filename> ]", 'play <filename> - send <filename> to buffer\npreview <filename> - output <filename> to buffer, no sendy\nlist - list files\nno args: output random!', 'list || play %(art_files) || preview %(art_files)',
                         "cb_art_cmd", '')
