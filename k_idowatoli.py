from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.properties import ObjectProperty, StringProperty
import pickle
from hmm import hmm
from smartdictionary import SmartDictionary
import numpy as np
import operator

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '200')


class GridLayout(GridLayout):
	label_wid = ObjectProperty()
	text_wid = ObjectProperty()
	b1_wid = ObjectProperty()
	b2_wid = ObjectProperty()
	b3_wid = ObjectProperty()
	with open('trained_test.pkl', 'rb') as finput:
		load_net = pickle.load(finput)
	net = load_net
	sd = SmartDictionary(SmartDictionary.SMART_WORDSEN_BIGRAM)
	previous_len = 0

	def do_action(self):
		self.label_wid.text = self.text_wid.text

	def whitelist_chars(self, text):
		if len(text) > 0:
			if text[-1] == ' ':
				self.correct()

	def correct(self):
		# print(self.vitello)
		inserted = self.text_wid.text.split()
		# print(len(inserted))
		# print(inserted)
		# print(self.previous_len)
		if len(inserted) == 1:
			correct, _ = self.net.build_viterbi(2, 25, inserted[0], self.sd)
			# print(correct)
			self.previous_len = 1
			self.label_wid.text = ' '.join(correct)
			self.b1_wid.text = ' '.join(correct)
		elif len(inserted) == self.previous_len + 1:
			self.net.add_viterbi_layer(2, 25, inserted[-1], auto_reconstruct=False)
			# ordino e prendo i 3 max
			self.net.prob
			col = self.net.prob[:, -1]
			# print(col)
			p = np.argsort(col)
			l = {}
			for i in range(0, len(p)):
				l[' '.join(self.net.reconstruct_viterbi_index(
					p[i])[-2:])] = (col[p[i]], p[i])
			sorted_l = sorted(
				l.items(), key=operator.itemgetter(1), reverse=True)
			# print(self.net.reconstruct_viterbi_index(p[-1]))
			# print(sorted_l)
			# print(sorted_l[2][0])
			correct1_label = self.net.reconstruct_viterbi_index(p[-1])
			#correct2 = self.net.reconstruct_viterbi_index(p[-2])[-2:]
			#correct3 = self.net.reconstruct_viterbi_index(p[-3])[-2:]
			correct1 = sorted_l[0][0]
			correct2 = sorted_l[1][0]
			correct3 = sorted_l[2][0]
			# print(correct1)
			# print(correct2)
			# print(correct3)
			self.previous_len += 1
			self.label_wid.text = ' '.join(correct1_label)
			self.b1_wid.text = ''.join(correct1)
			self.index_change = []
			self.index_change.append(sorted_l[0][1][1])
			self.b2_wid.text = ''.join(correct2)
			self.index_change.append(sorted_l[1][1][1])
			self.b3_wid.text = ''.join(correct3)
			self.index_change.append(sorted_l[2][1][1])
		else:
			return

	def change_prob(self, index):
		k = self.index_change[index - 1]
		# print(k)
		# print(self.net.prob)
		for i in range(self.net.prob.shape[0]):
			if i == k:
				self.net.prob[i, self.net.prob.shape[1] - 1] = 1e10
			else:
				self.net.prob[i, self.net.prob.shape[1] - 1] = -1e-40
		self.label_wid.text = ' '.join(self.net.reconstruct_viterbi()[0])
		# print(self.net.prob)


class GridLayoutApp(App):
    def build(self):
        return GridLayout()


prova = GridLayoutApp()
prova.run()