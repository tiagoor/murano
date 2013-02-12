# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import logging
LOG = logging.getLogger(__name__)

from windc.core.builder import Builder
from windc.core import change_events as events

class DataCenter(Builder):
	def __init__(self):
		self.name = "Data Center Builder"
		self.type = "datacenter"
		self.version = 1

	def build(self, context, event, data):
		if event.scope == events.SCOPE_DATACENTER_CHANGE:
			LOG.info ("Got Data Center change event. Analysing...")
		else:
			LOG.debug("Not in my scope. Skip event.")
		pass

