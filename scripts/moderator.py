# -*- coding: utf-8 -*-
# Copyright (C) 2022 Mykhailo Pyrozhenko @rfe:matrix.org
#
# This file is part of the Matrix Moderation Tool.
#
# The program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the program. If not, see <https://www.gnu.org/licenses/>.

import antispam

from nio import AsyncClient, MatrixRoom, RoomMessageText


class Moderator(AsyncClient):
	# Print and filter all the messages we receive
	async def message_callback(self, room: MatrixRoom, event: RoomMessageText) -> None:
		formatted_body = event.body.replace("\n", " ")
		print(f"{room.user_name(event.sender)} | {formatted_body}"[:80])
		# Uncomment the following code to allow your bot move the room read marker:
		# await self.room_read_markers(room.room_id, event.event_id, event.event_id)
		try:
			if (antispam.is_spam(formatted_body)):
				await self.room_redact(room.room_id, event.event_id, "autofilter")
		except TypeError:
			pass

	# We're running the __init__ method defined in AsyncClient with our new callback
	def __init__(self, homeserver, user="", device_id="",
              store_path="", config=None, ssl=None, proxy=None):
		super().__init__(homeserver, user=user, device_id=device_id,
                   store_path=store_path, config=config, ssl=ssl, proxy=proxy)
		self.add_event_callback(self.message_callback, RoomMessageText)
