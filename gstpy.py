# -*- coding: utf-8 -*-
# Copyright (C) 2010 SERPRO
# Author: Nilson Morais <nilson.morais-filho@serpro.gov.br>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import sys, os, time, thread
import glib, gobject
import pygst
pygst.require("0.10")
import gst
from output import *
from video import *
from encoding import *
from audio import *
#from effects import *
#from video_switch import *
#from swap import *

class gstpy:
	def __init__(self):
		print "Iniciando transmissão"
		self.player = None
		self.encoding = Encoding()
		self.output = Output()
		self.audio = Audio()
		self.video = Video()
		#self.video_switch = VideoSwitch(window)
		self.preview_enabled = "False"
		self.effect_enabled = "False"

		self.player = gst.Pipeline("player")

		self.queue_video = gst.element_factory_make("queue", "queue_video")
		self.queue_audio = gst.element_factory_make("queue", "queue_audio")
		self.player.add(self.queue_video, self.queue_audio)

		self.convert = gst.element_factory_make("audioconvert", "convert")
		self.player.add(self.convert)

		self.videosrc = self.video.get_videosrc()
		self.audiosrc = self.audio.get_audiosrc()

		self.player.add(self.videosrc, self.audiosrc)
		gst.element_link_many(self.videosrc, self.queue_video)
		gst.element_link_many(self.audiosrc, self.queue_audio)

		self.overlay = gst.element_factory_make("textoverlay", "overlay")
		self.tee = gst.element_factory_make("tee", "tee")
		queue1 = gst.element_factory_make("queue", "queue1")
		queue2 = gst.element_factory_make("queue", "queue2")
		self.mux = self.encoding.get_mux() #theora
		self.sink = self.output.get_output() #icecast
		#self.preview_element = self.preview.get_preview()
		self.colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspacesink")

		#effects
		src_colorspace = gst.element_factory_make("ffmpegcolorspace", "src_colorspace")
		self.player.add(src_colorspace)

		self.player.add(
			self.overlay, self.tee, queue1, self.mux, self.sink,
			self.colorspace
		)
		gst.element_link_many(self.queue_video, src_colorspace, self.overlay)

		err = gst.element_link_many(
			self.overlay, self.tee, queue1, self.colorspace, self.mux,
			self.sink
		)
		if err == False:
			print "Error conecting elements"

		gst.element_link_many(self.queue_audio, self.convert, self.mux)

		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		#bus.connect("sync-message::element", self.on_sync_message)

	def play(self):
		self.state = "playing"
		self.playmode = True
		self.player.set_state(gst.STATE_PLAYING)
		print self.bus

		while self.playmode:
			time.sleep(1)
		time.sleep(1)
		loop.quit()

	def stop(self):
		self.player.set_state(gst.STATE_NULL)

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug

mainclass = gstpy()
thread.start_new_thread(mainclass.play, ())
gobject.threads_init()
loop = glib.MainLoop()
loop.run()
