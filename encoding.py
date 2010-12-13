# -*- coding: utf-8 -*-
# Copyright (C) 2010 Holoscopio Tecnologia
# Author: Luciana Fujii Pontello <luciana@holoscopio.com>, Nilson Morais <nilson.morais-filho@serpro.gov.br>
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

class Encoding:

	def __init__(self):
		print "Theora selected"
		self.mux = gst.Bin()
		audioconvert = gst.element_factory_make("audioconvert", "audioconvert")
		vorbisenc = gst.element_factory_make("vorbisenc", "vorbisenc")
		theoraenc = gst.element_factory_make("theoraenc", "theoraenc")
		oggmux = gst.element_factory_make("oggmux", "oggmux")
		self.mux.add(audioconvert, vorbisenc, theoraenc, oggmux)
		gst.element_link_many(audioconvert, vorbisenc, oggmux)
		theoraenc.link(oggmux)
		theoraenc.set_property("quality", 32)
		source_pad = gst.GhostPad(
			"source_ghost_pad", self.mux.find_unlinked_pad(gst.PAD_SRC)
		)
		self.mux.add_pad(source_pad)
		sink_pad1 = gst.GhostPad(
			"sink_pad1", self.mux.find_unlinked_pad(gst.PAD_SINK)
		)
		sink_pad2 = gst.GhostPad(
			"sink_pad2", self.mux.find_unlinked_pad(gst.PAD_SINK)
		)
		self.mux.add_pad(sink_pad1)
		self.mux.add_pad(sink_pad2)	
	
	def get_mux(self):
		return self.mux
