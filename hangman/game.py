from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, x, hit = None, miss = None):
        self.x = x
        self.hit = hit
        self.miss = miss
        if self.hit == True and self.miss == True:
            raise InvalidGuessAttempt()
    
    def is_hit(self):
        return bool(self.hit)
    
    def is_miss(self):
        return bool(self.miss)




class GuessWord(object):
    def __init__(self, word):
        self.answer = word.lower()
        num_ast = len(self.answer)
        self.masked = self._mask_word(self.answer)
        if word == '':
            raise InvalidWordException()


    def perform_attempt(self, char):
        har = char.lower()
        if len(char) > 1:
           raise InvalidGuessedLetterException() 
           
        if char.lower() not in self.answer:
            return GuessAttempt(char, miss=True)
        
        
        for c in self.answer:
#            if c not in previous_guesses:
#                previous_guesses.append(c)
            if char.lower() == c:
                list_c = [i for i, char in enumerate(self.answer) if char == c]
                for i in list_c:
                    self.masked = self.masked[:i] + c + self.masked[i + 1:]
                return GuessAttempt(char, hit=True)
        return GuessAttempt(char, miss=True)
        
    @classmethod
    def _mask_word(cls, word):
        return len(word) * '*'
 

class HangmanGame(object):
    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.word = GuessWord(self.select_random_word(word_list))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        

    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def is_lost(self):
        return self.remaining_misses == 0
    
    def is_won(self):
        return self.word.masked == self.word.answer
        
    def is_finished(self):
        return self.is_won() or self.is_lost()
    
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException()
        return (random.choice(list_of_words))
    
    
    def guess(self, char):
        char = char.lower()
        if len(char) > 1:
           raise InvalidGuessedLetterException() 
        
        if self.is_finished():
            raise GameFinishedException
        
        if char in self.previous_guesses:
           raise InvalidGuessedLetterException('invalid character')
        
        self.previous_guesses.append(char)
        
        attempt = self.word.perform_attempt(char)
        if attempt.is_miss():
            self.remaining_misses -= 1
        if attempt.is_hit():
            self.remaining_misses -= 0
        
        if self.is_won():
            raise GameWonException
        
        if self.is_lost():
            raise GameLostException
        
        return attempt
    
    
    
game = HangmanGame(['Python'])
attempt = game.guess('y')


