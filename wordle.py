with open("english.txt") as F:
	words = F.read().split("\n")

"""This class is the base wordle game."""

import random


class game:
	
	def __init__(self, word = None):
		if word:
			self.word = word
		else:
			self.word = random.choice(words)

		self.res = ['nein'] * 5
	
	def guess(self, gus):
		for i in range(len(self.res)):
			self.res[i] = 'nein'
		remaining = list(self.word)

		for i in range(len(gus)):
			if gus[i] == self.word[i]:
				self.res[i] = "ja"
				#remaining.__delitem__(i - (5-len(remaining)))
				remaining[i] = '-'
		for i in range(len(gus)):
			if self.res[i] != "nein":
				continue
			#if gus[i] in remaining:
			try:
				idx = remaining.index(gus[i])
				self.res[i] = "jein"
				remaining[idx] = '-'
			except ValueError:
				continue

		return self.res
