#!/usr/bin/python

# create a web server using web.py framework and the apis for tic-tac-toe board

import web
import json
import tic_tac_toe

web.config.debug = False

urls = (
	'/', 'index',
	'/index.*', 'index',
	'/(js|css|images)/(.*)', 'static',
	'/api/(.*)', 'api'
)

app = web.application(urls, globals())

# create sessions in order to handle the multiple users
session = web.session.Session(app,web.session.DiskStore('sessions'))

class index:
	def GET(self):
		f = open('pages/index.html', 'r')
		return f.read()


class api:
	"""handle api calls for tic-tac-toe game"""
	def GET(self, action):
		# start the game
		if action == "start":
			session.game = tic_tac_toe.Game()
			result = session.game.start()
			web.header('Content-Type', 'application/json')
			return json.dumps(result)

		if action == "state":
			# if the game exists, it returns the latests state of the board
			if hasattr(session, 'game'):
				result = session.game.state(False)
			else:
				session.game = tic_tac_toe.Game()
				result = session.game.start()
			web.header('Content-Type', 'application/json')
			return json.dumps(result)

	def POST(self, action):
		if action == "update":
			user_data = web.input(cell=[])
			result = session.get('game').update(int(user_data["cell"][0]))
			web.header('Content-Type', 'application/json')
			return json.dumps(result)


if __name__ == "__main__":
	app.run()