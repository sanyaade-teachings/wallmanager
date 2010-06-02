import sys
sys.path.append("..")

from pymt import *
import subprocess
from datetime import datetime

from mtmenu.application_running import is_app_running, kill_app_running

from gesture.gesture_db import *
from config import GESTURE_ACCEPTANCE_MARGIN, PRODUCTION, UNAVAILABLE_PROJECTORS_TIME
from webmanager.appman.utils import projectors


class GestureWidget( MTGestureWidget ):
    def __init__(self):
        super(GestureWidget, self).__init__()
        self.gestures = Gestures()
        self.counter = 0
        print 'Gesture loaded'

    def on_gesture(self, gesture, touch):
        from mtmenu import activity_checker

        print "PROJECTORS STATE: %d" % activity_checker.projectors_on
        if not activity_checker.projectors_on:
            print 'Turning Projectors On'
            activity_checker.turn_projectors_power(1)
        activity_checker.set_last_activity()
            
        print 'gesture: %d' % self.counter
        self.counter += 1
        #print self.gestures.gesture_to_str(gesture)
        
        # gesture recognition
        if self.gestures.find(gesture, GESTURE_ACCEPTANCE_MARGIN) and is_app_running():
            print "gesture recognized"
            kill_app_running()
            

