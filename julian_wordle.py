"""This file is for game playing wordle. There are bots, bot tests, bot analysis, and a human advisor for when you're playing a game. """

"""The algorithm is variations on refining the possible wordlist given wordle guess results. Words are ranked by the expected number of letter matches for all further possible words. Yellows are 1 point and Greens are 2 points. In the human game, when scores are very near the max score, all reasonably good candidates are ranked by word frequency (using wikipedia database). I believe word frequency is a good heuristic because while the game allows many different words, they bias their solution sets to words people know for the sake of fun and popularity. """

WORDLENGTH = 5
ATTEMPTS = 4
DEBUG = False

with open("english.txt") as F:
        words = [x for x in F.read().split("\n") if len(x) == WORDLENGTH]

import wordle
import random


def wordsetjaquery(wordset, chr, i, realword):
	reswords = [x for x in wordset if x[i] == chr]
	if DEBUG:
		print("JAquery\nrealword[i] == chr")
		print(realword[i] == chr)
		print("C ja", chr, len(reswords))
	return reswords


def wordsetjeinquery(wordset, chr, i, alli, realword):
	reswords = []

	# First, remove all matches from kinda's own position. Any word with such a letter is not allowed. 
	wordset = [x for x in wordset if x[i] != chr]

	#for every word
	for w in wordset:

		#if it has a valid character in there add it
		for ci, c in enumerate(w):

			#print(w, c, ci, chr, c == chr)
			#input()
			# as long as it's not a 'ja'
			if DEBUG and w == realword:
				print("\nJEINquery\nc == chr", w, realword)
				print(c, '=', chr, c == chr)
				print("ci in alli true==break", ci, alli, ci in alli)
			if ci == i or ci in alli:
				# If char not in position of a YES or NO
				continue
			if c == chr:
				# And that char is the same, add it
				reswords.append(w)
				if DEBUG and w == realword:
					print("GOT IT")
				break

	if DEBUG:
		print("C jein", chr, len(reswords))
	return reswords


def wordsetneinquery(wordset, chr, realword, jascount):
	
	reswords = [x for x in wordset if x.count(chr) <= jascount]
	if DEBUG:
		print("Removing all",chr," from wordset")
		print("NEINquery\nchr not in realword (should be true)")
		print(chr, realword)
		print(chr, jascount)
		print(chr not in realword)
		print("C nein", chr, len(reswords))
	return reswords


def findwords(guess, results, wordset, realword):
	if DEBUG:
		print("Finding", realword, "with", guess)
		print("CAN GUESS", realword in wordset)		
	alli = []
	jas = []

	#do ja's first
	for i, r in enumerate(results):
		if r == 'ja':
			wordset = wordsetjaquery(wordset, guess[i], i, realword)
			alli.append(i)
	if DEBUG:
		print("CAN GUESS JA", realword in wordset)	
		
	# bad code, but the logical !Nein for preparing doubles in nein
	for i, r in enumerate(results):
		if r != "nein":
			jas.append(guess[i])

	for i, r in enumerate(results):
		if r == 'nein':

			# There is at least a doubled letter, one of which is needed
			wordset = wordsetneinquery(wordset, guess[i], realword, jas.count(guess[i]))
			# def a bug because nein mean global no, not locationally alli.append(i)
	if DEBUG:
		print("CAN GUESS NEIN", realword in wordset)	
	
	for i, r in enumerate(results):
		if r == 'jein':
			wordset = wordsetjeinquery(wordset, guess[i], i, alli, realword)

	if DEBUG:
		print("CAN GUESS JEIN", realword in wordset)		
	return wordset



def setmaxattempts(x):
	global ATTEMPTS
	ATTEMPTS = x


def getattempts():
	print(ATTEMPTS)


def stats(tries=50000, wordset=words):
	oneresults = dict()
	tworesults = dict()

	for i in range(tries):
		print(i, end = '\r')
		results = playgame(wordset)

		CUM = 1 if results[0] else -1
		if results[1][0] not in oneresults:
			oneresults[results[1][0]] = 0

		oneresults[results[1][0]] = oneresults[results[1][0]] + CUM

		if len(results[1]) < 2:
			results[1].append(results[1][0])

		wordA = results[1][0] 
		wordB = results[1][1]
		if wordA not in tworesults:
			tworesults[wordA] = dict()
		if wordB not in tworesults[wordA]:
			tworesults[wordA][wordB] = 0

		tworesults[wordA][wordB] = tworesults[wordA][wordB] + CUM

	import operator
	onesorted = sorted(oneresults.items(), key=operator.itemgetter(1))

	return [onesorted, tworesults]


def twentystats():
	oneresults = dict()
	tworesults = dict()
	for word in words:
		
		for i in range(20):
			print(i, end = '\r')
			results = playgame([word])

			CUM = 1 if results[0] else 0
			if results[1][0] not in oneresults:
				oneresults[results[1][0]] = 0
	
			oneresults[results[1][0]] = oneresults[results[1][0]] + CUM

			if len(results[1]) < 2:
				results[1].append(results[1][0])

			wordA = results[1][0] 
			wordB = results[1][1]
			if wordA not in tworesults:
				tworesults[wordA] = dict()
			if wordB not in tworesults[wordA]:
				tworesults[wordA][wordB] = 0

			tworesults[wordA][wordB] = tworesults[wordA][wordB] + CUM

	import operator
	onesorted = sorted(oneresults.items(), key=operator.itemgetter(1))

	return [onesorted, tworesults]

	

def open_freq_heuristics():
	with open('freq.txt') as F:
		a = [x.split(' ') for x in F.read().split('\n')]
	return {x[0]: int(x[1]) for x in a}


def humanplay(bestfirstword=True, reset_chardic=True, freq_heur=True):
	code = 1
	while code == 1:
		code = humanplayloop(bestfirstword, reset_chardic, freq_heur)
	

"""This is a tool to play your games for you, or to advise you on good moves."""
"""the inputs choose different algorithms. Freq_heur is if you want to rate word choices for when there are fewer than a dozen words towards words that are more common (using wikipedia dataset)"""

def humanplayloop(bestfirstword=True, reset_chardic=True, freq_heur=True):
	print("Not"*(not bestfirstword), "Using Best First Word")
	if not bestfirstword:
		print("Not"*(not reset_chardic), "Resetting CharacterDictionaries per Guess")
	print("Not"*(not freq_heur), "Biasing Final Choices Towards Common Words")
	import wordle_analysis as wa
	import operator
	ansmap = {'y':'ja', 'n':'nein', 'k':'jein'}
	chd = wa.chardic()
	if freq_heur:
		freq = open_freq_heuristics()

	print("Start with TARES or AROSE")
	wordset = words
	while(True):
		guess = input("What did you guess?")
		print(guess)
		print("results? y/n/k Yes No Kinda")
		results = input().strip()
		while len(results) != 5 or results == 'restart':
			if results == 'restart':
				print()
				return 1
			results = input().strip()[:5]
			

		results = list(map(lambda x: ansmap[x], list(results)))

		print(results)
		wordset = findwords(guess, results, wordset, "spook")
		
		if bestfirstword:
			print("By best first word")
			wordscores = wa.find_best_first_word(wordset)
		else:	
			print("By character study")
			if reset_chardic:
				chd.set(wordset)
			wordscores = [(x, wa.score(x, chd.charD)) for x in wordset]

		""" Replacing with always ordering the words within 5 of the max with popularity. 
		# If all words are within 5 points of each other, sort by frequency
		if freq_heur and max(wordscores, key=lambda n: n[1])[1] - min(wordscores, key=lambda n: n[1])[1] < 5:
			print("By popularity")
			wordscores = [(x, getwordfreq(x, freq)) for x in wordset]
		"""
		
		sortedwordscores = sorted(wordscores, key=operator.itemgetter(1))
		print(sortedwordscores[-50:])
		
		# For all words within 5 points of the max, sort by frequency
		m = max(wordscores, key=lambda n: n[1])[1]
		wordscores = [(x[0], getwordfreq(x[0], freq)) for x in sortedwordscores if m - x[1] < 5]
		print("Top words by popularity:")
		print(sorted(wordscores, key=operator.itemgetter(1)))



def getwordfreq(word, d):
	if word in d:
		return d[word]
	return 1


"""This basically maxes the spread of all the possible characters. Maxes yellows, ignores duplicate letters for the sake of the spread."""

def charplay(reset_chardic=True, freq_heur=True):
	import wordle_analysis as wa
	import operator
	if freq_heur:
		freq = open_freq_heuristics()

	g = wordle.game()
	wordset = words
	results = [''] * 5
	guesses = []
	attempts = 0
	chd = wa.chardic()
	
	#initial attempt
	attempts += 1
	guesses.append( "arose" )
	results = g.guess(guesses[ -1 ])
	wordset = findwords(guesses[ -1 ], results, wordset, g.word)

	while(attempts < ATTEMPTS and results.count('ja') < WORDLENGTH):
		attempts += 1
		if freq_heur and len(wordset) <= 12:
			guesses.append( max([(x, getwordfreq(x, freq)) for x in wordset], key=lambda x:x[1])[0] )
		else:
			guesses.append( max([(x, wa.score(x, chd.charD)) for x in wordset], key=lambda x:x[1])[0] )
		results = g.guess(guesses[ -1 ])
		wordset = findwords(guesses[ -1 ], results, wordset, g.word)
		if reset_chardic:
			chd.set(wordset)

	return results.count('ja') == 5, guesses, results, attempts, g.word



def randomplay(blank_input_for_test_A=False, blank_input_for_test_B=False, initialguesses=words):
	g = wordle.game()
	wordset = words
	results = [''] * 5
	guesses = []
	attempts = 0
	
	#initial attempt
	attempts += 1
	guesses.append( random.choice(initialguesses) )
	results = g.guess(guesses[ -1 ])
	wordset = findwords(guesses[ -1 ], results, wordset, g.word)

	while(attempts < ATTEMPTS and results.count('ja') < WORDLENGTH):
		attempts += 1
		guesses.append( random.choice(wordset) )
		results = g.guess(guesses[ -1 ])
		wordset = findwords(guesses[ -1 ], results, wordset, g.word)

	return results.count('ja') == 5, guesses, results, attempts, g.word



"""This scores every word on how well it matches characters of all possible remaining words. So this takes location into account."""
"""This is the slowest algorithm, because it does O(wordsearchset N: N^2) for every step of the game. The avg is somewhere around 1 game/second."""

def bestfirstplay(blank_input_for_testA=False, freq_heur=True):
	import wordle_analysis as wa
	import operator
	if freq_heur:
		freq = open_freq_heuristics()

	g = wordle.game()
	wordset = words
	results = [''] * 5
	guesses = []
	attempts = 0
	chd = wa.chardic()
	
	#initial attempt
	attempts += 1
	guesses.append( "tares" ) #best word according to wordle_analysis's best_first_word over the entire dataset.
	results = g.guess(guesses[ -1 ])
	wordset = findwords(guesses[ -1 ], results, wordset, g.word)

	while(attempts < ATTEMPTS and results.count('ja') < WORDLENGTH):
		attempts += 1
		if freq_heur and len(wordset) <= 12:
			guesses.append( max([(x, getwordfreq(x, freq)) for x in wordset], key=lambda x:x[1])[0] )
		else:
			guesses.append( max(wa.find_best_first_word(wordset), key=lambda x:x[1])[0] )
		results = g.guess(guesses[ -1 ])
		wordset = findwords(guesses[ -1 ], results, wordset, g.word)


	return results.count('ja') == 5, guesses, results, attempts, g.word



def test(rounds=100):
	functions = [randomplay, charplay, charplay, charplay, charplay, bestfirstplay, bestfirstplay]
	inputCD = [None, False, True, False, True, None, None]
	inputFH = [None, False, False, True, True, False, True]
	wins = [0] * len(functions)
	attempts = [0] * len(functions)
	setmaxattempts(6)

	for i, f in enumerate(functions):
		for r in range(rounds):
			print('>>>', i, r, '/', rounds, end='\r')
			results = f(inputCD[i], inputFH[i])
			if results[0]:
				wins[i] += 1
				attempts[i] += results[3]
	print("wins: random, char, refined char, FHchar, FHrefinedChar, BFP, FHBFP", wins)
	print("avg per win:", [attempts[i]/wins[i] for i in range(len(functions))])
	


	



### TODO:
""" The human game plays really well. If the scores are all within 5 of each other, word popularity comes into play. 
I want to play with this a bit more. """

