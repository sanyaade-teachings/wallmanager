
from datetime import datetime, time, timedelta
from threading import Timer

from webmanager.appman.utils import projectors
from models import ScreensaverControlProxy, ProjectorControlProxy, ApplicationProxy
from mtmenu.application_running import is_app_running
from config import PRODUCTION, INACTIVITY_POOL_INTERVAL

from datetime import datetime
from threading import Thread


class ActivityChecker():

    def __init__(self):
        #CONTROL VARIABLES
        self.last_activity = datetime.now()
        self.projectors_on = self.in_schedule()
        
        Thread( target=self.last_activity_checker ).start()


    def set_projectors_status(self, status):
        self.projectors_on = status


    def set_last_activity(self, time = None): 
        if time != None:
            self.last_activity = time
        else:
            self.last_activity = datetime.now()
      
        
    def get_projectors_down_duration(self):
        return self.get_minutes( self.cast_time_to_timedelta( datetime.now() ) ) - self.get_minutes( self.cast_time_to_timedelta(self.projectors_down_time ) )
        
        
    def update_projectors_status(self):
        try:
            dic = projectors.projectors_status()
            for key, value in dic.items():
                if not value == 'OFF':
                    self.set_projectors_status(True)
                    print "Projector status updated to TRUE"
                    return

            self.set_projectors_status(False)
            print "Projector status updated to FALSE"                
        except Exception as e:
            print "Projectors status error: %s" % e
    
    
    def last_activity_checker(self):
        self.update_projectors_status()

        diff_min = self.get_minutes(datetime.now() - self.last_activity)
        screensaver_control = self.get_first_item(ScreensaverControlProxy.objects.all())        
        projector_control = self.get_first_item(ProjectorControlProxy.objects.all())

        if screensaver_control:
            self.manage_screensaver(screensaver_control, diff_min)
        else:
            print "screensaver time not defined"

        if projector_control:
            self.manage_projectors(projector_control, diff_min)           
        else:
            print "projectors inactivity time not defined"

        self.last_activity_checker()


    def manage_screensaver(self, control, minutes):
        inactivity_time = self.get_minutes( self.cast_time_to_timedelta( control.inactivity_time ) )
        application = ApplicationProxy.objects.filter(id = control.application.id)[0]    
        if minutes > inactivity_time and not is_app_running() and application:
            print 'Launching Screensaver'
            application.execute(True)


    def manage_projectors(self, control, minutes):
        inactivity_time = self.get_minutes( self.cast_time_to_timedelta( control.inactivity_time ) ) 
        print "Projector inactivity time = %s\ndiff time = %s\nis_projectors_on = %s" % (inactivity_time, minutes, self.projectors_on)
        
        if minutes > inactivity_time and self.projectors_on:
            print "Turning Projectors Off"   
            self.turn_projectors_power(0)     

        
    def turn_projectors_power(self, status):
        if not self.in_schedule():
            return
        
        try:
            projectors.projectors_power(status)
            print 'projectors turned off'
        except Exception, e:
            print 'Error turning projectors off'
    
    
    def in_schedule(self):
        day = datetime.now().weekday()
        projector_control = self.get_first_item( ProjectorControlProxy.objects.all() )
        if not projector_control:
            return False
         
        if day < 5:
            start = projector_control.startup_week_time
            end = projector_control.shutdown_week_time
        else:
            start = projector_control.startup_weekend_time
            end = projector_control.shutdown_weekend_time

        return self.is_between(start, end)


    def get_first_item(self, items):
        for item in items:
            return item
        return None
    
    
    def cast_time_to_timedelta(self, instant):
        return timedelta( seconds = instant.hour*60*60 + instant.minute*60 + instant.second )
       
    
    def get_minutes(self, time):
        return ( time.seconds + time.microseconds/1000000.0) / 60
    
    def is_between(self, start, end):
        now = datetime.now()
        return (now.hour > start.hour or ( now.hour == start.hour and now.minute > start.minute )) and \
        (now.hour < end.hour or (now.hour == end.hour and now.minute < end.minute))

