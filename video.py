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


import gobject
import pygst
pygst.require("0.10")
import gst

class Video:

	def __init__(self):
		print "v4l2 selected"
		#V4L2
		self.src = gst.element_factory_make("v4l2src", "v4l2src")
		#self.capsfilter = gst.element_factory_make("capsfilter", "capsfilter")
		#self.player.add(self.videosrc, self.capsfilter, self.audiosrc)
		#gst.element_link_many(self.videosrc, self.capsfilter, self.queue_video)
		#caps = gst.caps_from_string("video/x-raw-yuv, width=400, height=300")
		#self.capsfilter.set_property("caps", caps)

	def get_videosrc(self):
		return self.src


