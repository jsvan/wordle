# wordle

Dataset: found online from a different git repo that apprently got it from wordle source code.

General alg: rule based, narrow down possible words. Remaining words are scored and ranked by a few different methods. When word scores are similar, word frequency is used as the ranking heuristic.

Performance: 85-90% win rate, avg 4.33 attempts / win.

Files: 
  wordle.py -- general game. 
  wordle_analysis.py -- statistical code for finding best starting words by looking at character distributions etc.
  julian_wordle.py -- disorganized code that plays wordle. Has multiple bot algorithms, tests, and a recommendation system for human games. 
 
Discovered best starting words: The word that has the best chance of immediately getting yellow and green matches is TARES. The word that offers more paths for quickly crossing more letters off the board (scaled to letter frequency) within the first two turns is AROSE, or any word with those letters. 
