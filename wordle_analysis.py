
"""This file is for static statistical analysis of words and wordle."""


class chardic:
	from string import ascii_lowercase as abc
	
	def newcorpus(self):
		with open("english.txt") as F:
			self.words = F.read().split('\n')
		return self.words

	def __init__(self, corpus = None):
		if not corpus:
			corpus = self.newcorpus()
		self.set(corpus)

	def set(self, corpus):
		self.words = corpus
		self.charD = {x:0 for x in self.abc}
		for word in corpus:
			for c in set(word):
				self.charD[c] += 1
	


def score(wordA, charD):
	scoreA = 0
	prevlets = set()

	for char in wordA:
		if char not in prevlets:
			scoreA += charD[char]
			prevlets.add(char)
	return scoreA



"""This looks at all words, and which of those words cover the most common letters, and also which words allow follow up words which cover the most letters. Arose seems to be the best."""

def scoreallwords(chdic):
	results = dict()
	for iii, wordA in enumerate(chdic.words):
		print(iii, end='\r')
		scoreA = 0
		prevletsA = set()
		skip = False

		for char in wordA:
			if char not in prevletsA:
				scoreA += chdic.charD[char]
				prevletsA.add(char)
			else:
				skip = True
		if skip:
			continue 
			#fuck this word

		results[wordA] = scoreA

		# then for all other words, find their marginal score boost
		for wordB in chdic.words:
			prevletsB = set()
			scoreB = 0
			for char in wordB:
				if char not in prevletsA and char not in prevletsB:
					scoreB += chdic.charD[char]
					prevletsB.add(char)
				else:
					skip = True
			if not skip:		
				results[wordA] += scoreB

	import operator
	print(len(results))
	allsorted = sorted(results.items(), key=operator.itemgetter(1))


	return allsorted




"""This looks at what first word has the single best score for all other words"""
"""O(N*N) Runtime"""
def find_best_first_word(words=None):
	import wordle
	if not words: #Is a list of all possible words
		words = chardic().newcorpus()
	scoremap = {'nein':0, 'jein':1, 'ja':2}
	G = wordle.game()
	wordscores = list()
	for i, source in enumerate(words):
		print(i, end='\r')
		if i//100 == 0:
			print("Thinking maybe...", source, "(random example)")
		wordscore = 0
		for target in words:
			G.word = target
			for r in G.guess(source):
				wordscore += scoremap[r]
		wordscores.append((source, wordscore))

			
	return wordscores








