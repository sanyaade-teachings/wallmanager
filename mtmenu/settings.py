from os.path import join, dirname, abspath

import sys
sys.path.append('..')


# Returns the absolute path to this file directory joined
# with whatever directories given as arguments
def relative(*x):
    return join(abspath(dirname(__file__)), *x)


#SET TRUE ON WALL
PRODUCTION = False



APPS_REPOSITORY_PATH = relative('apps/')
APPS_BOOT_FILENAME = 'boot.bat'

##PROXY CONFIGURATIONS
PROXY_UDP_IP   = '127.0.0.1'
PROXY_RECEIVING_PORT = 6000
PROXY_SENDING_PORT_ONE = 6001
PROXY_SENDING_PORT_TWO = 3333

## UI
if PRODUCTION:
    MAINWINDOW_SIZE = (2048,768)
else:
    MAINWINDOW_SIZE = (1000,768)
MAINWINDOW_POSITION = (0,0)


TOPBAR_SIZE = (MAINWINDOW_SIZE[0], 148)
TOPBAR_POSITION = (0,620)

CATEGORYLIST_SIZE = (170, 620)
CATEGORYLIST_POSITION = (0,0)

APPSLIST_POSITION = (CATEGORYLIST_SIZE[0],0)
APPSLIST_SIZE = (MAINWINDOW_SIZE[0] - CATEGORYLIST_SIZE[0], 620)
APPSLIST_NUMBER_OF_LINES = 3

VOTEPOPUP_SIZE = (215, 100)
VOTEPOPUP_POSITION = (int((MAINWINDOW_SIZE[0] - VOTEPOPUP_SIZE[0]) / 2),
                      int((MAINWINDOW_SIZE[1] - VOTEPOPUP_SIZE[1]) / 2))

APPPOPUP_SIZE = (215,160)

# LAUCHING APPLICATION SETTINGS
MAX_ATTEMPTS = 3
SLEEP_SECONDS_BETWEEN_ATTEMPTS = 2

## GESTURE
GESTURE_ACCEPTANCE_MARGIN = 0.90
GESTURE_KILLER = "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"

