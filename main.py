#!/usr/bin/env python
import sys
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
import re
from twisted.internet.defer import setDebugging
setDebugging(True)


class SedBot(irc.IRCClient):
    nickname = "sedbot"

    def __init__(self):
        self.last = {}

    def signedOn(self):
        self.join("#pumpingstationone")

    def joined(self, channel):
        pass

    def privmsg(self, user, channel, msg):
        nick = user.split("!")[0]
        if nick == self.nickname:
            return
        elif channel == self.nickname:
            return
        m = re.search("s/(.*)/(.*)/[giI]*", msg)
        if(m):
            search_string = m.group(1)
            replace_string = m.group(2)
            original_msg = self.last[user]
            log.msg("replacing {0} with {1} in {2}".format(search_string, replace_string, original_msg))
            new_msg = re.sub(search_string, replace_string, original_msg, 0, re.IGNORECASE)
            full_msg = "What {0} meant to say was \"{1}\".".format(nick, new_msg)
            self.msg(channel, full_msg)

        else:
            self.last[user] = msg

class SedBotFactory(protocol.ClientFactory):
    protocol = SedBot

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print("connection failed: {0}".format(reason))
        reactor.stop()


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    
    f = SedBotFactory()

    reactor.connectTCP("irc.freenode.net", 6667, f)
    reactor.run()
