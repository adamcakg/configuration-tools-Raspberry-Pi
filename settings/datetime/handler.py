import cairo
import math
import time
from thread import Thread
from localisation.timezone import get_arreas, get_locations
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import GLib

class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        self.darea = None
        self.init_ui()
        self.draw()
        
        Thread(self)
        
    def add_controller(self, controller):
        self.controller = controller
        
    def init_ui(self):
        self.darea = self.builder.get_object('drawing_arrea')
        self.darea.connect("draw", self.on_draw)
        
    def draw(self):
        self.darea.queue_draw()
        GLib.timeout_add(1000, self.draw)
        
    def get_time(self):
        time = os.popen("date | grep -oP '[0-9]+:[0-9]+:[0-9]+'").read().rstrip()
        is_pm = os.popen("date | grep -oP '[P,A][M]'").read().rstrip()
        hours, minutes, secs = time.split(':')
        if is_pm == 'PM':
            hours = str(int(hours) + 12)
        return int(hours), int(minutes), int(secs)
        
    def on_draw(self, wid, cr):
        w = 150
        h = 150
        hours, minutes, secs = self.get_time()
        
        secs_arc = (2*math.pi / 60) * secs
        minute_arc = (2*math.pi / 60) * minutes
        if hours > 12:
            hours = hours - 12       
        hour_arc = (2*math.pi / 12) * hours + minute_arc / 12
        
        # pointer hour
        cr.set_source_rgba(0.25, 0.35, 0.42, 0.8) 
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_width ((min(w,h)/2 -20)/6 )
        cr.move_to(w/2,h/2)
        cr.line_to(w/2 + (min(w,h)/2 -20) * 0.6 * math.cos(hour_arc - math.pi/2),
            h/2 + (min(w,h)/2 -20) * 0.6 * math.sin(hour_arc - math.pi/2))
        cr.stroke()
        
        # pointer minute
        cr.set_source_rgba(0.25, 0.35, 0.42, 0.8) 
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_width ((min(w,h)/2 -20)/6 * 0.8)
        cr.move_to(w/2,h/2)
        cr.line_to(w/2 + (min(w,h)/2 -20) * 0.9 * math.cos(minute_arc - math.pi/2), 
            h/2 + (min(w,h)/2 -20) * 0.8 * math.sin(minute_arc - math.pi/2))
        cr.stroke()

        # pointer seconds
        cr.set_source_rgba(1, 0.34, 0.46, 0.8) 
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_width ((min(w,h)/2 -20)/6 * 0.3)
        cr.move_to(w/2,h/2)
        cr.line_to(w/2 + (min(w,h)/2 -20) * 1.1 * math.cos(secs_arc - math.pi/2), 
            h/2 + (min(w,h)/2 -20) * 0.8 * math.sin(secs_arc - math.pi/2))
        cr.stroke()
        
# -------------------------------------------------------------------------------------------------------  
    def fulfill_arreas(self, arreas):
        arrea_combo_box = self.builder.get_object('arrea_combo_box')
        for arrea in arreas:
            arrea_combo_box.append(arrea, arrea)
        current_timezone = os.popen('timedatectl show | grep -oP [A-Za-z]+\/[a-zA-Z_]+').read().rstrip()
        current_arrea = current_timezone.split('/')[0]
        arrea_combo_box.set_active_id(current_arrea)
        
    
    def fulfill_locations(self, widget=None):    
        arrea = self.builder.get_object('arrea_combo_box').get_active_id()
        locations = get_locations(arrea)
        location_combo_box = self.builder.get_object('location_combo_box')
        location_combo_box.remove_all()
        for location in locations:
            location_combo_box.append(location, location)
            
        current_timezone = os.popen('timedatectl show | grep -oP [A-Za-z]+\/[a-zA-Z_]+').read().rstrip()
        current_location = current_timezone.split('/')[1:]
        current_location = '/'.join(current_location)
        
        if locations == ['']:
            return
        elif len(locations) == 1:
            location_combo_box.set_active_id(locations[0])
        elif current_location in locations:
            location_combo_box.set_active_id(current_location)
        else:
            location_combo_box.set_active_id(locations[9])
    
    def set_timezone(self, widget):
        self.delete_timezone_modal()
        arrea = self.builder.get_object('arrea_combo_box').get_active_id()
        location = self.builder.get_object('location_combo_box').get_active_id()
        
        os.popen('sudo timedatectl set-timezone {}/{}'.format(arrea, location))
    
    def create_timezone_modal(self, widget):
        dialog = self.builder.get_object('timezone_modal')
        dialog.set_attached_to(self.builder.get_object('date_time_page'))
        dialog.show_all()

    def delete_timezone_modal(self, widget=None):
        dialog = self.builder.get_object('timezone_modal')
        dialog.hide()
        
# -------------------------------------------------------------------------------------------------------
    def fulfill_time(self):
        hours = self.builder.get_object('hours_combo_box')
        minutes = self.builder.get_object('minutes_combo_box')
        seconds = self.builder.get_object('seconds_combo_box')
        
        for number in range(1,61):
            if number < 25:
                hours.append(str(number), str(number))
            minutes.append(str(number), str(number))
            seconds.append(str(number), str(number))
    
    
    def create_date_time_modal(self, widget):
        time = self.get_time()
        
        hours = self.builder.get_object('hours_combo_box').set_active_id(str(time[0]))
        minutes = self.builder.get_object('minutes_combo_box').set_active_id(str(time[1]))
        seconds = self.builder.get_object('seconds_combo_box').set_active_id(str(time[2]))
        
        dialog = self.builder.get_object('time_modal')
        dialog.set_attached_to(self.builder.get_object('date_time_page'))
        dialog.show_all()
        
    def delete_date_time_modal(self, widget=None):
        dialog = self.builder.get_object('time_modal')
        dialog.hide()

    def set_date_time(self, widget):
        date = self.builder.get_object('calendar').get_date()
        os.popen('sudo date --set {}-{}-{}'.format(date[0], date[1], date[2]))
        
        hours = self.builder.get_object('hours_combo_box').get_active_id()
        minutes = self.builder.get_object('minutes_combo_box').get_active_id()
        seconds = self.builder.get_object('seconds_combo_box').get_active_id()
        os.popen('sudo date --set {}:{}:{}'.format(hours, minutes, seconds))
        self.delete_date_time_modal()
        
    def thread_function(self):
        self.fulfill_time()
        
        self.fulfill_arreas(get_arreas())
        self.fulfill_locations()

          
                         