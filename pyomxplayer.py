import pexpect
import re

from threading import Thread
from time import sleep

class OMXPlayer(object):

    _LAUNCH_CMD = '/usr/bin/omxplayer -o hdmi %s %s'
    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD = 'q'

    paused = False
    subtitles_visible = True

    _VOF=1

    def __init__(self, mediafile):
        cmd = self._LAUNCH_CMD % (mediafile, '')
        #print(cmd)
        self._process = pexpect.spawn(cmd)

        self._end_thread = Thread(target=self._get_end)
        self._end_thread.start()
 
    def _get_end(self):
        while True:
            index = self._process.expect([pexpect.TIMEOUT,
                                            pexpect.EOF])
            if index == 1: self.stop()
            else:
                print('video end '+str(index))
                #self.stop()
                break
            sleep(0.5)
        self._VOF=0
			
    def toggle_pause(self):
        if self._process.send(self._PAUSE_CMD):
            self.paused = not self.paused

    def toggle_subtitles(self):
        if self._process.send(self._TOGGLE_SUB_CMD):
            self.subtitles_visible = not self.subtitles_visible
            
    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)

    def set_speed(self):
        raise NotImplementedError

    def set_audiochannel(self, channel_idx):
        raise NotImplementedError

    def set_subtitles(self, sub_idx):
        raise NotImplementedError

    def set_chapter(self, chapter_idx):
        raise NotImplementedError

    def set_volume(self, volume):
        raise NotImplementedError

    def seek(self, minutes):
        raise NotImplementedError
