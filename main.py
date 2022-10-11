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

import asyncio
import getpass
import json
import os
import sys

from nio import LoginResponse
from scripts.moderator import Moderator

CONFIG_FILE = "credentials.json"


def write_credentials(resp: LoginResponse, homeserver) -> None:
	# open the config file in write-mode
	with open(CONFIG_FILE, "w") as f:
		# write the login details to disk
		json.dump(
			{
				"homeserver": homeserver,  # e.g. "https://matrix.org"
				"user_id": resp.user_id,  # e.g. "@user:matrix.org"
				"device_id": resp.device_id,  # device ID, 10 uppercase letters
				"access_token": resp.access_token,  # cryptogr. access token
			},
			f,
		)


async def main() -> None:
	# If there are no previously-saved credentials, we'll use the password
	if not os.path.exists(CONFIG_FILE):
		print("First time use. Did not find credential file.")
		homeserver = "https://matrix.example.org"
		homeserver = input(f"Enter your homeserver URL: [{homeserver}] ")
		if not (homeserver.startswith("https://") or homeserver.startswith("http://")):
			homeserver = "https://" + homeserver
		user_id = "@user:example.org"
		user_id = input(f"Enter your full user ID: [{user_id}] ")
		device_name = "matrix-nio"
		device_name = input(f"Choose a name for this device: [{device_name}] ")
		client = Moderator(homeserver, user_id)
		pw = getpass.getpass()
		resp = await client.login(pw, device_name=device_name)
		# check that we logged in succesfully
		if isinstance(resp, LoginResponse):
			write_credentials(resp, homeserver)
		else:
			print(f'homeserver = "{homeserver}"; user = "{user_id}"')
			print(f"Failed to log in: {resp}")
			sys.exit(1)
		print("Logged in using a password. Credentials were stored.")
	# Otherwise the config file exists, so we'll use the stored credentials
	else:
		# open the file in read-only mode
		with open(CONFIG_FILE, "r") as f:
			config = json.load(f)
			client = Moderator(config["homeserver"])
			client.access_token = config["access_token"]
			client.user_id = config["user_id"]
			client.device_id = config["device_id"]
		print("Logged in using stored credentials.")
	# Start the bot with 30 millisecond timeout
	await client.sync_forever(timeout=30000)

asyncio.run(main())
