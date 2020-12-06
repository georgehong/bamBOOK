"""Hangman game."""
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

from kivy.config import Config
# size window
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 900)
Config.set('graphics', 'height', 650)

from kivy.core.window import Window
# background color
Window.clearcolor = (.86, .90, .93, 1)

import random
from words_for_hangman import RANDOM_WORDS
from words_for_hangman import ALPHABET_RU

TRIES = 6


class HangmanApp(App):
    # boolean to check that letter is in word
    def check(self, letter, word):
        return letter.lower() in word

    def show_word_change(self):
        ind = [i for i, j in enumerate(self.right_answer) if j == self.letter]
        for index in ind:
            self.printinglist[index] = self.right_answer[index]
        return self.printinglist

    def is_finishing(self):
        # Logic to actually determine the state of the game
        if self.user_error == TRIES:
            self.lose += 1
            self.contentpopuptext.text = (
                'Youve Lost...' + '\n' + 'The correct word was: ' + self.right_word)
            return self.lose, self.contentpopuptext.text, True
        elif self.right_answer == self.printinglist:
            self.win += 1
            self.contentpopuptext.text = 'Правильно! Это ' + self.right_word
            return self.win, self.contentpopuptext.text, True
        else:
            return False

    def restart(self, arg):
        # Resets all instance variables (that are not win/loss statistics) to default
        self.category_word, self.right_word = random.choice(list(RANDOM_WORDS.items()))
        self.category.text = self.category_word
        self.right_word = random.choice(self.right_word)
        self.right_answer = [x for x in self.right_word]
        self.printinglist = ['_' for x in range(len(self.right_answer))]
        self.word = ' '.join(self.printinglist)
        self.word_to_show.text = self.word
        self.user_error = 0
        self.user_er.text = 'Ошибок: ' + str(self.user_error)+'/'+str(TRIES)
        self.winlose.text = 'Побед/Проигрышей: '+str(self.win)+'/'+str(self.lose)
        for letter in range(33):
            self.alphabet_button[letter].font_size = 26
            self.alphabet_button[letter].disabled = False
            self.alphabet_button[letter].background_color = [.64, .74, .76, 1]
            self.alphabet_button[letter].background_normal = ''
        self.popup.dismiss()

    def exithangman(self, *args):
        # obvious
        App.get_running_app().stop()

    def build(self):
        # name window
        self.title = 'Game'
        # Displays category/hint
        self.category_word, self.right_word = random.choice(list(RANDOM_WORDS.items()))
        self.right_word = random.choice(self.right_word)
        # Truth arrays
        self.right_answer = [x for x in self.right_word]
        self.printinglist = ['_' for x in range(len(self.right_answer))]
        # Makes sure underscores are separate
        self.word = ' '.join(self.printinglist)
        self.user_error = 0
        self.win = 0
        self.lose = 0

        # TODO review padding for maximum tastefulness
        mainbox = BoxLayout(orientation='vertical', padding=[6])
        topbox = BoxLayout(orientation='vertical', size_hint=(1, .6))
        toppanel = BoxLayout(orientation='horizontal', size_hint=(1, .2))
        # Prints user errors
        self.user_er = Label(text='Failures: ' + str(self.user_error)+'/'+str(TRIES),
                             font_size=14, halign='left',
                             valign='top', text_size=(280, 50),
                             color=[.35, .46, .50, 1])
        self.category = Label(text=self.category_word, font_size=28, color=[.35, .46, .50, 1])
        self.winlose = Label(text='Win/Lose Ratio: '+str(self.win)+'/'+str(self.lose),
                             font_size=14,
                             halign='right', valign='top',
                             text_size=(200, 50),
                             color=[.35, .46, .50, 1])
        # Toppanel maintains all text in horizontal layout
        toppanel.add_widget(self.user_er)
        toppanel.add_widget(self.category)
        toppanel.add_widget(self.winlose)
        # This is the work the user has done
        self.word_to_show = Label(text=self.word,
                                  font_size=50, size_hint=(1, .7),
                                  halign='center', valign='center',
                                  text_size=(800, 300))
        topbox.add_widget(toppanel)
        topbox.add_widget(self.word_to_show)
        mainbox.add_widget(topbox)
        # Constructs "Keyboard",
        alphabet = GridLayout(cols=7, spacing=[2], size_hint=(1, .4))
        self.alphabet_button = ALPHABET_RU
        # Let alphabet button be a dictionary of all letters.  Pay attention to on_press function
        for letter in range(0, len(self.alphabet_button) - 5):
            self.alphabet_button[letter] = Button(
                text=self.alphabet_button[letter],
                font_size=26,
                on_press=self.user_letter,
                background_color=[.64, .74, .76, 1],
                background_normal='')
            alphabet.add_widget(self.alphabet_button[letter])
        # Empty widget?
        alphabet.add_widget(Widget())
        # Fills in the remaining 5 letters, centered
        for letter in range(len(self.alphabet_button) - 5, len(self.alphabet_button)):
            self.alphabet_button[letter] = Button(
                text=self.alphabet_button[letter],
                font_size=26,
                on_press=self.user_letter,
                background_color=[.64, .74, .76, 1],
                background_normal='')
            alphabet.add_widget(self.alphabet_button[letter])
        alphabet.add_widget(Widget())
        mainbox.add_widget(alphabet)
        # Done with most of the letters present?  At the end, construct buttons that are property of game object to refer to for later.
        self.contentpopup = BoxLayout(orientation='vertical',
                                      padding=[6])
        self.contentpopuptext = Label(text='WIN/LOSE Ratio: '+str(self.win)+'/'+str(self.lose),
                                      size_hint=(1, .8))
        contentpopupbutton = GridLayout(cols=2, spacing=[2], size_hint=(1, .2))
        self.contentpopupbutton1 = Button(text="Exit",
                                          background_color=[.64, .74, .76, 1],
                                          background_normal='',
                                          on_press=self.exithangman)
        self.contentpopupbutton2 = Button(text="Restart",
                                          background_color=[.64, .74, .76, 1],
                                          background_normal='',
                                          on_press=self.restart)
        contentpopupbutton.add_widget(self.contentpopupbutton1)
        contentpopupbutton.add_widget(self.contentpopupbutton2)
        self.contentpopup.add_widget(self.contentpopuptext)
        self.contentpopup.add_widget(contentpopupbutton)
        self.popup = Popup(title='What purpose does this serve?',
                           content=self.contentpopup,
                           size_hint=(None, None), size=(400, 300),
                           auto_dismiss=False, background_color=(.86, .90, .93, .7),
                           separator_color=(.86, .90, .93, .7))
        return mainbox

    # Logic that occurs when keystroke is pressed
    def user_letter(self, instance):
        # Why is this necessary?  
        # TODO: What is instance?
        self.letter = str(instance.text)
        # Change button properties once clicked
        instance.font_size = 20
        instance.disabled = True
        # If present in word
        if self.check(self.letter, self.right_answer):
            instance.background_color = [0, 1, 0, 1]
            instance.background_normal = ''
            # Locates indices where the correct letter occurs
            ind = [i for i, j in list(enumerate(self.right_answer)) if j == self.letter]
            
            for index in ind:
                self.printinglist[index] = self.right_answer[index]
            # Add displayed words back together
            self.word_to_show.text = ' '.join(self.printinglist)
            # check popup to end the game
            if self.is_finishing():
                self.popup.open()
        else:
            instance.background_color = [1, 0, 0, 1]
            instance.background_normal = ''
            self.user_error += 1
            # TODO: What does 
            self.user_er.text = 'Errors: '+str(self.user_error)+'/'+str(TRIES)
            if self.is_finishing():
                self.popup.open()


if __name__ == '__main__':
    HangmanApp().run()