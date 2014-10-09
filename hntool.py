import json
import urllib.request as request
import webbrowser
import sublime, sublime_plugin

class HntoolCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.keys = []
		self.top10 = []
		self.limit = 5
		self.detail_data_list = []
		try:
			resp = request.urlopen("https://hacker-news.firebaseio.com/v0/topstories.json")
			topics = json.loads(resp.read().decode("utf-8"))
			self.top10 = topics[0:self.limit]
			self.detail_data_list = []
			for i in range(self.limit):
				topic_id = self.top10[i]
				#https://hacker-news.firebaseio.com/v0/item/8863.json
				topic_url = "https://hacker-news.firebaseio.com/v0/item/" + str(topic_id) + ".json"
				topic_resp = request.urlopen(topic_url)
				topic_data = json.loads(topic_resp.read().decode("utf-8"))
				self.detail_data_list.append(topic_data)
				self.keys.append(topic_data["title"])
				pass
			sublime.active_window().show_quick_panel(self.keys, self.goto)
		except Exception as ex:
			print(ex)

	def goto(self, arrpos):
		#print(arrpos)
		content_data = self.detail_data_list[arrpos]
		webbrowser.open_new(content_data["url"])
		pass