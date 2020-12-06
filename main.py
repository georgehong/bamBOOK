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
import re

TRIES = 6
ALPHABET = [chr(x) for x in range(97, 97 + 26)]

class Bambook(App):
    def build(self):
        # Window title
        # Words to display
        self.cursor_index = 0
        self.excerpt = "Elephants are the largest land animals They eat only plants Even though elephants are very strong, they are the only mammals that cannot jump"
        excerpt_ = self.excerpt.split(" ")
        blanks_ = ['-' * len(x) for x in excerpt_]
        self.final_blanks = " ".join(blanks_)



        self.title = 'Bambook'
        mainbox = BoxLayout(orientation='vertical', padding=[6])
        topbox = BoxLayout(orientation='vertical', size_hint=(1, .6))
        toppanel = BoxLayout(orientation='horizontal', size_hint=(1, .2))

        # TODO Add corner stats/info?
        self.center_label = Label(text=self.excerpt, text_size=(800, 300), color=[0, 0, 0, 1])
        #toppanel.add_widget("LEFT")
        toppanel.add_widget(self.center_label)
        #toppanel.add_widget("RIGHT")

        # Typing Progress 
        self.progress_text = Label(text=self.final_blanks,
                                  font_size=40, size_hint=(1, .7),
                                  halign='center', valign='center',
                                  text_size=(800, 300), color=[0, 0, 0, 1])
        topbox.add_widget(toppanel)
        topbox.add_widget(self.progress_text)
        mainbox.add_widget(topbox)

        alphabet = GridLayout(cols=7, spacing=[2], size_hint=(1, .4))
        self.alphabet_button = ALPHABET

        for letter in range(0, len(self.alphabet_button) - 5):
            self.alphabet_button[letter] = Button(
                text=self.alphabet_button[letter],
                font_size=26,
                on_press=self.user_letter,
                background_color=[.64, .74, .76, 1],
                background_normal='')
            alphabet.add_widget(self.alphabet_button[letter])

        #alphabet.add_widget(Widget())

        for letter in range(len(self.alphabet_button) - 5, len(self.alphabet_button)):
            self.alphabet_button[letter] = Button(
                text=self.alphabet_button[letter],
                font_size=26,
                on_press=self.user_letter,
                background_color=[.64, .74, .76, 1],
                background_normal='')
            alphabet.add_widget(self.alphabet_button[letter])
        
        self.space_button = Button(
                text="space",
                font_size=26,
                on_press=self.user_letter,
                background_color=[.64, .74, .76, 1],
                background_normal='')
        self.delete_button = Button(
                text="delete",
                font_size=26,
                on_press=self.user_letter,
                background_color=[.64, .74, .76, 1],
                background_normal='')
        alphabet.add_widget(self.space_button)
        alphabet.add_widget(self.delete_button)

        mainbox.add_widget(alphabet)

        return mainbox
    

    def user_letter(self, instance):
        # Get button letter
        self.letter = str(instance.text)
        # easier access to critical variables
        dex = self.cursor_index
        curr = self.final_blanks
        # Update displayed text, button text, move cursor
        self.final_blanks = curr[:dex] + self.letter + curr[dex + 1:]
        self.progress_text.text = self.final_blanks
        # To check at every character, look at same index of the above string and self.excerpt and check for a match
        self.cursor_index += 1

        # if self.progress_text == self.excerpt:
        #     print("GOOD JOB")
        # else:
        #     print("cHeCk YoUr WoRk")
        #print("HI")
    

if __name__ == '__main__':
    Bambook().run()