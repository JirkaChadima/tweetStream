#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
##
## tweetStream
## ===========
## Simple GTK application that can display one user's statuses in real time.
## Currently there's no possibility to change user on the fly. Restart is
## needed.
##
## Dependencies
## ------------
## PyGTK 2.0. Program can be used without it though. If you call TwitterClient
## directly, stdout is used as a text pane.
##
## Author
## ------
## Jirka Chadima, chadima.jiri@gmail.com, 03/2010
##
## License
## -------
## MIT, feel free to use and improve the code
################################################################################

### imports

import sys
import logging
from gui import MainWindow
from twitterclient import TwitterClient

### credentials

__author__="Jiri Chadima"
__version__ = "0.2"

### basic configuration

LOG_FILENAME = "tweetstream.log"
DEBUG = False

### main loop

if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s:%(levelname)s:%(message)s')
    else:
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')

    
    logging.info("Starting tweetStream %s" % __version__)

    if len(sys.argv) < 2:
        logging.fatal("No username given! Stopping...")
        print "Usage: %s [username]" % sys.argv[0]
        sys.exit(1)
        
    uname = sys.argv[1]
    logging.info("Given username %s" % uname)

    client = TwitterClient(uname)
    win = MainWindow(client)
    win.main()

