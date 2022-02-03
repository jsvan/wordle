# wordle

Dataset: english.txt: A list of wordle words. Found online from a different git repo that apprently got it from wordle source code. 
  freq.txt: wikipedia word frequency data mapped onto wordle vocab. 

General alg: Command line based, rule based, narrow down possible words. Remaining words are scored and ranked by a few different methods. When word scores are similar, word frequency is used as the ranking heuristic.

Performance: 85-90% win rate, avg 4.33 attempts / win with my uniformly at random tests, but may perform better in real life. If I restrict the guess/answer set only to the leaked wordle words, the solution set shrinks from ~12000 to ~2000 and I get 99.5% accuracy and an avg of 3.6 guesses/win (1000 trials).


Files: 
  wordle.py -- general game. 
  wordle_analysis.py -- statistical code for finding best starting words by looking at character distributions etc.
  julian_wordle.py -- disorganized code that plays wordle. Has multiple bot algorithms, comparisson tests, and a recommendation system for human games. 
 
Discovered best starting words: The word that has the best chance of immediately getting yellow and green matches with only wordle solutions is STARE. The same for all valid solutions is TARES. The word that offers more paths for quickly crossing more letters off the board (scaled to letter frequency) within the first two turns is LATER/ALTER for wordle solutions, and for the valid word AROSE, or any word with those letters. 
