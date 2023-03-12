#!/usr/bin/env python3

from asciimatics.widgets import Frame, TextBox, Layout, Label, Divider, Text, \
    CheckBox, RadioButtons, Button, PopUpDialog, TimePicker, DatePicker, DropdownList, PopupMenu
from asciimatics.effects import Background
from asciimatics.event import MouseEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication, \
    InvalidFields
from asciimatics.parsers import AsciimaticsParser
import sys
import re
import datetime
import logging
import os
import subprocess

import ffmpeg



global screen_var

# Initial data for the form
form_data = {
    "text_field_input_video_location": "",
    "text_field_output_video_folder_location": "",
    "text_field_output_video_name": "",
    "RO": "You can't touch this",
    "Things": 2,
    "CA": False,
    "CB": True,
    "CC": False,
    "DATE": datetime.datetime.now().date(),
    "TIME": datetime.datetime.now().time(),
    "start_time_field": datetime.datetime(1, 1, 1, 0, 0),
    "end_time_field": datetime.datetime(1, 1, 1, 0, 0),
    "PWD": "",
    "DD": 1
}

#logging.basicConfig(filename="forms.log", level=logging.DEBUG)


class MainFrame(Frame):
    def __init__(self, screen):
        super(MainFrame, self).__init__(screen,
                                        int(screen.height * 2.7 // 3),
                                        int(screen.width * 2.7 // 3),
                                        data=form_data,
                                        has_shadow=True,
                                        name="My Form")
        layout = Layout([1, 20, 1])
        self.add_layout(layout)
        layout.add_widget(Label("Spl1t v0.1"), 1)
        layout.add_widget(Label("Click the field and drag and drop."), 1)
        layout.add_widget(
            Text(label="Input Video File Location:",
                 name="text_field_input_video_location",
                 on_change=self.on_change), 1)

        layout.add_widget(Label("Make sure to close the Folder path below by adding a \ for Windows or a / for Unix-based."), 1)
        layout.add_widget(
            Text(label="Output Video Folder Location:",
                 name="text_field_output_video_folder_location",
                 on_change=self.on_change,
                 validator=".*(\\\|/)$"), 1)
        layout.add_widget(Label("Include the video extension .mp4 or .mkv"), 1)
        layout.add_widget(
            Text(label="Output Video Name (include .mp4 or .mkv):",
                 name="text_field_output_video_name",
                 on_change=self.on_change,
                 validator="^.*\.(mp4|MP4|mkv|MKV)$"), 1)

        layout.add_widget(Divider(height=2), 1)
        layout.add_widget(Label("(Hours:Minutes:Seconds)"), 1)
        layout.add_widget(
            TimePicker("Start Time:", name="start_time_field", on_change=self.on_change, seconds=True), 1)

        layout.add_widget(
            TimePicker("End Time:", name="end_time_field", on_change=self.on_change, seconds=True), 1)

        layout.add_widget(Button("Click Here To Trim", self.split), 1)


        layout.add_widget(Divider(height=3), 1)
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Quit", self._quit), 2)
        self.fix()


    def on_change(self):
        changed = False
        self.save()
        for key, value in self.data.items():
            if key not in form_data or form_data[key] != value:
                changed = True
                break



    def split(self):
        # ffmpeg -ss 00:01:00 -to 00:02:00  -i input.mp4 -c copy output.mp4
        #check to see if fields are correct
        try:
            self.save(validate=True)
            message = "Values entered are:\n\n"
            for key, value in self.data.items():
                message += "- {}: {}\n".format(key, value)
        except InvalidFields as exc:
            message = "The following fields are invalid:\n\n"
            for field in exc.fields:
                message += "- {}\n".format(field)
            self._scene.add_effect(PopUpDialog(self._screen, message, ["OK"]))
            return False

        try:
            data_dictionary = self.data
            given_video_location = data_dictionary["text_field_input_video_location"]
            given_output_video_folder = data_dictionary["text_field_output_video_folder_location"]
            given_output_video_name = data_dictionary["text_field_output_video_name"]
            given_start_time = data_dictionary["start_time_field"].strftime("%H:%M:%S")
            given_end_time = data_dictionary["end_time_field"].strftime("%H:%M:%S")
            ffmpeg_command = "ffmpeg -ss " + given_start_time + " -to " + given_end_time + " -i " + given_video_location + " -c copy " + given_output_video_folder + given_output_video_name
            #Try Catch Block to Handle Crossplatform Compatability
            try: #Works on windows
                subprocess.call(ffmpeg_command, creationflags=subprocess.CREATE_NEW_CONSOLE)
            except: #Works on MacOS
                open_new_window_mac_command= '''osascript -e 'tell application "Terminal" to activate' \
  -e 'tell application "System Events" to keystroke "t" using {command down}' \
  -e 'tell application "Terminal" to do script ''' +  "\""+ ffmpeg_command + "\"" + "in front window\'" 
                subprocess.call(open_new_window_mac_command, shell=True)
                self.fix()
        except:
            print(self.data.items())
            print(self.data['text_field_input_video_location'])

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        has_shadow=True,
                        on_close=self._quit_on_yes))

    @staticmethod
    def _check_email(value):
        m = re.match(r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z0-9_\-.]+$",
                     value)
        return len(value) == 0 or m is not None

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")



def demo(screen, scene):
    screen.play([Scene([
        Background(screen),
        MainFrame(screen)
    ], -1)], stop_on_resize=True, start_scene=scene, allow_int=True)




last_scene = None
while True:
    try:
        screen_var = Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
