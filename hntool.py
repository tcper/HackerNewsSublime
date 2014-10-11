import json
import threading
import urllib.request as request
import webbrowser
import queue 

import sublime, sublime_plugin

keys = []
detail_data_list = []
urlQueue = queue.Queue()

class HntoolCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global keys
		t = ThreadUrl(urlQueue, self.callback)
		t.setDaemon(True)
		t.start()
		opener = request.build_opener(TopicListHandler())
		try:
			thread = threading.Thread(target=opener.open, args=('https://hacker-news.firebaseio.com/v0/topstories.json',))
			thread.start()
			thread.join()
		except Exception as e:
			print (e)

	def callback(self):
		global keys
		print("callback")
		sublime.active_window().show_quick_panel(keys, self.goto)

	def goto(self, arrpos):
		#print(arrpos)
		global detail_data_list
		print(arrpos)
		if arrpos < 0:
			return
		if len(detail_data_list) <= 0:
			return
		if arrpos >= len(detail_data_list) - 1:
			return
		content_data = detail_data_list[arrpos]
		webbrowser.open_new(content_data["url"])
		pass

class TopicListHandler(request.HTTPSHandler):
	@staticmethod
	def https_response(req, response):
		global keys
		global urlQueue

		topics = json.loads(response.read().decode("utf-8"))
		topics_list = topics[:5]
		#print(topics_list)
		for i in range(5):
			topic_id = topics_list[i]
			urlQueue.put("https://hacker-news.firebaseio.com/v0/item/" + str(topic_id) + ".json")
		return response

	@staticmethod
	def goto(self, arrpos):
		#print(arrpos)
		content_data = self.detail_data_list[arrpos]
		webbrowser.open_new(content_data["url"])
		pass

class ThreadUrl(threading.Thread):
	"""Threaded Url Grab"""
	def __init__(self, que, callback):
		threading.Thread.__init__(self)
		self.callback = callback
		self.que = que

	def run(self):
		global keys, detail_data_list
		keys = []
		detail_data_list = []
		while True:
		#grabs host from queue
			host = self.que.get()
			topic_resp = request.urlopen(host)
			topic_data = json.loads(topic_resp.read().decode("utf-8"))
			print(topic_data)
			detail_data_list.append(topic_data)
			keys.append(topic_data["title"])
			self.que.task_done()
			print(self.que.qsize())
			if len(keys) > 0 and self.que.qsize() <= 0:
				self.callback()
			