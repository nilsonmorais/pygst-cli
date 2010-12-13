# -*- coding: utf-8 -*-
# Copyright (C) 2009 Holoscopio Tecnologia
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

class Output:

	def __init__(self):
		#icecast
		print "Icecast selected"
		self.sink = gst.element_factory_make("shout2send", "icecastsink")
		self.sink.set_property("ip", "10.200.104.59")
		self.sink.set_property("username", "source")
		self.sink.set_property("password", "hackme")
		self.sink.set_property("port", 8000)
		self.sink.set_property("mount", "assiste.ogv")

	def get_output(self):
		return self.sink


