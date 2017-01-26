# Simple forwarding between WeeChat buffers

This WeeChat script sets up forwarding between two buffers, that is, it
copies messages appearing in one buffer to the other buffer and vice versa.
Some simple processing to the messages is also made (currently only
nicks are prepended to messages from IRC channels).

With the jabber.py script and an xmpp-capable mobile device, this script
can be used to set up a simple IM-based mobile IRC client, with the messages
originating from your WeeChat client running under tmux as usual. Note that
this currently only works for one channel and requires an extra xmpp
account for your WeeChat xmpp client.

## Usage

Copy the forwarder.py script to the `~/.weechat/python` directory.

Find out the full names of the buffers you want to forward between by
issuing the command `/buffer get full_name` in the buffer. Add the names
to config variables `plugins.var.python.forwarder.buf1` and
`plugins.var.python.forwarder.buf2` with the `/set` command.

Run the forwarder by loading the script: `/script load forwarder`.

