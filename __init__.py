# -*- coding: utf-8 -*-
import time
import datetime


from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi
 
@cbpi.step
class WaitOnTimeStep(StepBase):
    '''
    Just put the decorator @cbpi.step on top of a method
    '''
    # Properties
    user_start_time = Property.Text("Start Time", configurable=True, default_value="00:00", description="Time at which this step completes in 24 hour format")
    target_start_time = datetime.datetime.now()

    def init(self):
        '''
        Initialize Step. This method is called once at the beginning of the step
        :return:
        '''
        # get the current time
        curr_time = datetime.datetime.now()

        # import time from user input in to datetime object
        self.target_start_time = datetime.datetime.strptime(self.user_start_time, "%H:%M")

        # replace the hour and minute with the user input
        self.target_start_time = self.target_start_time.replace(year=curr_time.year)
        self.target_start_time = self.target_start_time.replace(month=curr_time.month)
        self.target_start_time = self.target_start_time.replace(day=curr_time.day)

        # if target is in the past, add a day
        if (curr_time > self.target_start_time):
          self.target_start_time += datetime.timedelta(days=1)

        start_msg = "Configured start time & date is : {0:%H}:{0:%M} {0:%B} {0:%d}, {0:%Y}".format(self.target_start_time)
        self.notify("Setting start time!", start_msg, timeout=None)


    def start(self):
        '''
        Custom Action which can be execute form the brewing dashboard.
        All method with decorator @cbpi.action("YOUR CUSTOM NAME") will be available in the user interface
        :return:
        '''


    def reset(self):
        pass

    def finish(self):
        pass

    def execute(self):
        '''
        This method is execute in an interval
        :return:
        '''
        curr_time = datetime.datetime.now()
        if (curr_time > self.target_start_time):
            self.notify("Time to start!", "Starting the next step", timeout=None)
            self.next()

