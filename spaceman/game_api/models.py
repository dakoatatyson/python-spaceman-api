from django.db import models
from django.contrib.postgres.fields import JSONField

from django.core import validators

from django.db.models.signals import pre_init
from django.dispatch import receiver

class Game(models.Model):
    word = models.CharField( max_length = 30, validators=[
        validators.MinLengthValidator(3, message="Word must be at least 3 characters long" ), 
        validators.RegexValidator( regex='^[A-Z]$', message="Word must only contain capital letters", code='invalid_word_characters')
    ])
    guesses_allowed = models.IntegerField( default= 10)
    guesses_taken = models.IntegerField( default = 0)
    
    letters_available = JSONField( default = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") )
    letters_guessed = JSONField( default = [] )
    guessed_word_state = JSONField( default = [] )

    is_game_over = models.BooleanField( default = False )

    ## Private methods
    def __isGuessInWord( self, guessed_letter ):
        return guessed_letter.upper() in self.word

    def __addGuessedLetter( self, guessed_letter):
        self.letters_guessed.append( guessed_letter )
        self.__updateAvailableLetters()

    def __updateAvailableLetters( self ):
        for guess in set( self.letters_available ) & set( self.letters_guessed ):
            self.letters_available.remove( guess )

    def __updateIsGameOver( self ):
        self.is_game_over = self.guesses_taken == self.guesses_allowed or not ('' in self.guessed_word_state)

    def __updateGuessedWordState( self ):
        new_word_state = []
        for letter in self.word:
            if letter in self.letters_guessed:
                new_word_state.append(letter)
            else:
                new_word_state.append('')
        self.guessed_word_state = new_word_state

    def __incrementGuessesTaken( self ):
        self.guesses_taken = self.guesses_taken + 1
    
    ## Public methods
    def handleGuess( self, guessed_letter ):
        self.__addGuessedLetter( guessed_letter )

        if self.__isGuessInWord( guessed_letter ):
            self.__updateGuessedWordState()
        else:
            self.__incrementGuessesTaken()

        self.__updateIsGameOver()


@receiver(pre_init, sender=Game)
def __pre_init( sender, args, **kwargs ):
    """
        Signal method for sanitizing the data before is it saved to the database. Specifically,
        we need to capitialize the word, initialized the guessed word state to a list of empty
        strings, and initialize the letters available to all the letters in the alphabet.
    """
    word = kwargs.get('kwargs', {}).get('word')
    guessed_word_state = kwargs.get('kwargs', {}).get('guessed_word_state')
    letters_available = kwargs.get('kwargs', {}).get('letters_available')

    if word:
        kwargs['kwargs']['word'] = word.upper()

        if not guessed_word_state:
            kwargs['kwargs']['guessed_word_state'] = [''] * len( word )

    if not letters_available:
        kwargs['kwargs']['letters_available'] = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')