from django.test import TestCase
from game_api.models import Game

from django.core.exceptions import ValidationError

class GameModelTests( TestCase ):

    ### word field
    def test_init_should_assign_given_word(self):
        game = Game( word= "TESTWORD")
        self.assertEquals( game.word, "TESTWORD" )
    
    def test_word_is_required( self ):
        with self.assertRaises( ValidationError ):
            game = Game()
            game.full_clean()

    def test_word_is_less_than_3_chars( self ):
        with self.assertRaises( ValidationError ):
            game = Game( word = "AA")
            game.full_clean()

    def test_word_is_only_letters( self ):
        with self.assertRaises( ValidationError ):
            game = Game( word = "A1B")
            game.full_clean()

    def test_word_is_capitalized( self ):
        testword = "testword"
        game = Game( word=testword )
        self.assertEquals(testword.upper(), game.word)


    ### guessed_word_state field
    def test_guessed_word_state_same_length_of_word( self ):
        testword = "apple"
        game = Game( word=testword )
        self.assertEquals( len( testword ), len( game.guessed_word_state ) )

    def test_geussed_word_state_is_only_empty_strings( self ):
        testword = "apple"
        game = Game( word=testword )
        self.assertEquals( ["", "", "", "", ""], game.guessed_word_state )

    ### guessed_word_state field
    def test_guessed_word_state_is_unchanged_if_guess_not_in_word( self ):
        initialGuessedWordState = ['','','S','','W','O','R','']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= initialGuessedWordState,
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        game.handleGuess('X')
        self.assertEquals( initialGuessedWordState, game.guessed_word_state )

    def test_guessed_word_state_is_updated_with_guessed_letter_in_word( self ):
        initialGuessedWordState = ['','','S','','W','O','R','']
        expectedGuessedWordState = ['T','','S','T','W','O','R','']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= initialGuessedWordState,
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        game.handleGuess('T')
        self.assertEquals( expectedGuessedWordState, game.guessed_word_state )


    ### available_letters field
    def test_init_should_set_letters_available_to_alphabet( self ):
        game = Game( word= "TESTWORD")
        self.assertEquals( game.letters_available, list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    
    def test_available_letters_should_remove_guessed_letters_when_letter_in_word( self ):
        initialLettersAvailable = ['B', 'D', 'E', 'T', 'Q']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            letters_available = initialLettersAvailable,
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'T'

        game.handleGuess(guess)
        expectedLettersAvailable = [letter for letter in initialLettersAvailable if not letter in [guess]]
        self.assertEquals( game.letters_available, expectedLettersAvailable )
        
    def test_available_letters_should_remove_guessed_letters_when_letter_not_in_word( self ):
        initialLettersAvailable = ['B', 'D', 'E', 'T', 'Q']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            letters_available = initialLettersAvailable,
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'Q'

        game.handleGuess(guess)
        expectedLettersAvailable = [letter for letter in initialLettersAvailable if not letter in [guess]]
        self.assertEquals( game.letters_available, expectedLettersAvailable )

    ### letters_guessed field
    def test_letters_guessed_should_add_guessed_letter_when_letter_in_word( self ):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'T'
        game.handleGuess(guess)
        expectedLettersGuessed = initialLettersGuessed + [guess]
        self.assertEquals( game.letters_guessed, expectedLettersGuessed )
    
    def test_letters_guessed_should_add_guessed_letter_when_letter_not_in_word( self ):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'Q'
        game.handleGuess(guess)
        expectedLettersGuessed = initialLettersGuessed + [guess]
        self.assertEquals( game.letters_guessed, expectedLettersGuessed )