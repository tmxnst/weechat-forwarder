# Copyright (c) 2017 Teemu Ikonen <tpikonen@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This script does bidirectional forwading of messages from one weechat
# buffer to another, while also doing some simple processing (i.e. adding
# nicks to messages originating from IRC). See forward_message() for details.
#
# Usage:
# Find out the full names of the buffers you want to forward between by
# issuing the command '/buffer get full_name' in the buffer. Add the names
# to config variables 'plugins.var.python.forwarder.buf1' and
# 'plugins.var.python.forwarder.buf2' with the '/set' command.


import weechat as w

info = (
    'forwarder',
    'Teemu Ikonen <tpikonen@gmail.com>',
    '0.1',
    'MIT',
    'Forward messages between two buffers',
    '',
    ''
)

# Full names of the buffers between which messages are forwarded.
# Use '/buffer get full_name' to get the full name of buffers
SETTINGS = {
    'buf1': '',
    'buf2': '',
}


buf1name = ""
buf2name = ""
buf1 = ""
buf2 = ""


def forward_message(data, frombuf, date, tags, dspld, hlgt, prefix, message):
    '''Forwards messages with some protocol-dependent processing.'''
    if frombuf == buf1:
        tobuf = buf2
    elif frombuf == buf2:
        tobuf = buf1
    else:
        return w.WEECHAT_RC_OK

    buffer_name = w.buffer_get_string(frombuf, 'full_name')
    tags = set(tags.split(','))
    #w.prnt("", "buffer_name: %s" % buffer_name)
    #w.prnt("", "Tags: %s" % str(tags))
    nick = "(unknown)"
    for t in tags:
        if t[:5] == "nick_":
            nick = t[5:]
            break
    if buffer_name.startswith("irc."):
        if "irc_action" in tags:
            msg = "* %s" % message
        elif "irc_topic" in tags:
            msg = message
        else:
            msg = "<%s> %s" % (nick, message)
    elif buffer_name.startswith("python.jabber.") and \
      not tags.isdisjoint({"notify_private", "notify_message"}):
        msg = message
    else:
        return w.WEECHAT_RC_OK

    w.command(tobuf, msg)
    return w.WEECHAT_RC_OK


if w.register(*info):
    # Initialize config.
    for option, value in SETTINGS.items():
        if not w.config_is_set_plugin(option):
            w.config_set_plugin(option, value)
    buf1name = w.config_get_plugin("buf1")
    buf2name = w.config_get_plugin("buf2")
    buf1 = w.buffer_search("==", buf1name)
    buf2 = w.buffer_search("==", buf2name)
    isok = True
    if buf1:
        w.prnt("", "full name of buf1 is: %s"
            % w.buffer_get_string(buf1, "full_name"))
    else:
        w.prnt("", "buf1 ('%s') not found" % buf1name)
        isok = False
    if buf2:
        w.prnt("", "full name of buf2 is: %s"
            % w.buffer_get_string(buf2, "full_name"))
    else:
        w.prnt("", "buf2 ('%s') not found" % buf2name)
        isok = False
    if isok:
        w.hook_print('', '', '', 1, 'forward_message', '')
        w.prnt("", "Forwarding between buf1 and buf2 in action.")
    else:
        w.prnt("", "Could not start forwarder.")
