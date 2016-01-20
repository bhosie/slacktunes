'''
This python script listens for distributed notifications from iTunes of new songs playing, 
works alot better then constantly polling. 
'''
import Foundation
from AppKit import *
from PyObjCTools import AppHelper
import requests

name = "";

class GetSongs(NSObject):
    def getMySongs_(self, song):
        song_details = {}
        ui = song.userInfo()
        song_details = dict(zip(ui.keys(), ui.values()))
        songStr = "'" + song_details['Name'] +"' by " + song_details['Artist']
        print songStr
        self.toSlack(songStr)

    def toSlack(self, songStr):
    	global name
        webhookUrl = "" #replace this with your channel webhook url
    	songStr = name + " is listening to " + songStr
    	data = {"channel": "#music-discovery", "username": "now-playing", "text": songStr, "icon_emoji": ":musical_note:"}
    	r = requests.post(webhookUrl, json = data)

    	print r.text

nc = Foundation.NSDistributedNotificationCenter.defaultCenter()
GetSongs = GetSongs.new()
nc.addObserver_selector_name_object_(GetSongs, 'getMySongs:', 'com.apple.iTunes.playerInfo',None)

inp = raw_input('Please enter your slack username: ')
name = inp
NSLog("Listening for new tunes....")
AppHelper.runConsoleEventLoop()