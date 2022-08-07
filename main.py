import nltk
import string
nltk.download('words')

# https://github.com/DevangThakkar/wordle_archive/blob/master/src/data/words.js
textfile = open('words.txt', 'r')
filetext = textfile.read().splitlines()
textfile.close()

five_letter_words_js = [word[2:word.index(':')] for word in filetext]

five_letter_words_nltk = [word.lower() for word in nltk.corpus.words.words() if len(word) == 5]

five_letter_words = list(set(five_letter_words_nltk).union(set(five_letter_words_js)))

five_letter_words = five_letter_words_nltk

common_letters = dict.fromkeys(string.ascii_lowercase, 0)

def count_letters(string):
  for c in string:
    common_letters[c] += 1

for word in five_letter_words:
  count_letters(word)

word_to_score = dict.fromkeys(five_letter_words, 0)

def set_scores():
  for word in word_to_score:
    for i, c in enumerate(word):
      word_to_score[word] += common_letters[c]
      if c in word[:i]:
        word_to_score[word] -= common_letters[c]

set_scores()

sorted_words = sorted(word_to_score, key=word_to_score.get, reverse=True)

guesses = []
known_letters = set()
useless_letters = set()
real_word = [' '] * 5

def get_guesses():
  best_guesses = dict.fromkeys(five_letter_words, 0)
  for word in five_letter_words:
    for letter in known_letters:
      if not letter in word:
        best_guesses[word] = -1
        break
    for letter in useless_letters:
      if letter in word:
        best_guesses[word] = -1
        break
    if best_guesses[word] == -1:
      continue
    if len(set(real_word)) != 0:
      for i, c in enumerate(real_word):
        if c == ' ': continue
        if word[i] != c:
          best_guesses[word] = -1
          break
    if best_guesses[word] == -1:
      continue
    for i, c in enumerate(word):
      best_guesses[word] += common_letters[c]
      if c in word[:i]:
        best_guesses[word] -= common_letters[c]
  return sorted(best_guesses, key=best_guesses.get, reverse=True)

def get_discovery():
  discovery_guesses = dict.fromkeys(five_letter_words, 0)
  for word in five_letter_words:
    for letter in useless_letters:
      if letter in word:
        discovery_guesses[word] = -1
        break
    if discovery_guesses[word] == -1:
      discovery_guesses.pop(word)
      continue
    for i, c in enumerate(word):
      if not c in known_letters:
        discovery_guesses[word] += common_letters[c]
      if c in word[:i]:
        discovery_guesses[word] = -1
        break
  if len(discovery_guesses) == 0: return five_letter_words
  if discovery_guesses[sorted(discovery_guesses, key=discovery_guesses.get, reverse=True)[0]] == -1:
    for word in discovery_guesses:
      for i, c in enumerate(word):
        if not c in known_letters:
          discovery_guesses[word] += common_letters[c]
        if c in word[:i]:
          discovery_guesses[word] -= common_letters[c]

  return sorted(discovery_guesses, key=discovery_guesses.get, reverse=True)

def remove_useless_words():
  for letter in useless_letters:
    for word in five_letter_words:
      if letter in word:
        five_letter_words.remove(word)
        break

guessed_words = []

print(sorted_words[:10])
while (True):
  guessed_words.append(input('Your guess: '))
  while (input('Got correct letter?') == 'y'):
    if (input('Got correct place?') == 'y'):
      letter = input('Letter:')
      real_word[int(input('Index:')) - 1] = letter
      known_letters.add(letter)
    else:
      known_letters.add(input('Letter:'))
  for letter in guessed_words[-1]:
    if not letter in known_letters:
      useless_letters.add(letter)
  remove_useless_words()
  print(f'Best guesses to solve: {get_guesses()[:10]}')
  print(f'Best guesses to discover: {get_discovery()[:10]}')