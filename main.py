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

    def check(self, letter, word):
        return letter.lower() in word

    def show_word_change(self):
        ind = [i for i, j in enumerate(self.right_answer) if j == self.letter]
        for index in ind:
            self.printinglist[index] = self.right_answer[index]
        return self.printinglist

    def is_finishing(self):
        if self.user_error == TRIES:
            self.lose += 1
            self.contentpopuptext.text = (
                'Вы проиграли...' + '\n' + 'Правильное слово: ' + self.right_word)
            return self.lose, self.contentpopuptext.text, True
        elif self.right_answer == self.printinglist:
            self.win += 1
            self.contentpopuptext.text = 'Правильно! Это ' + self.right_word
            return self.win, self.contentpopuptext.text, True
        else:
            return False

    def restart(self, arg):
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
        App.get_running_app().stop()

    def build(self):
        # name window
        self.title = 'Виселица'
        self.category_word, self.right_word = random.choice(list(RANDOM_WORDS.items()))
        self.right_word = random.choice(self.right_word)
        self.right_answer = [x for x in self.right_word]
        self.printinglist = ['_' for x in range(len(self.right_answer))]
        self.word = ' '.join(self.printinglist)
        self.user_error = 0
        self.win = 0
        self.lose = 0
        mainbox = BoxLayout(orientation='vertical', padding=[6])
        topbox = BoxLayout(orientation='vertical', size_hint=(1, .6))
        toppanel = BoxLayout(orientation='horizontal', size_hint=(1, .2))
        self.user_er = Label(text='Ошибок: ' + str(self.user_error)+'/'+str(TRIES),
                             font_size=14, halign='left',
                             valign='top', text_size=(280, 50),
                             color=[.35, .46, .50, 1])
        self.category = Label(text=self.category_word, font_size=28, color=[.35, .46, .50, 1])
        self.winlose = Label(text='Побед/Проигрышей: '+str(self.win)+'/'+str(self.lose),
                             font_size=14,
                             halign='right', valign='top',
                             text_size=(200, 50),
                             color=[.35, .46, .50, 1])
        toppanel.add_widget(self.user_er)
        toppanel.add_widget(self.category)
        toppanel.add_widget(self.winlose)
        self.word_to_show = Label(text=self.word,
                                  font_size=50, size_hint=(1, .7),
                                  halign='center', valign='center',
                                  text_size=(800, 300))
        topbox.add_widget(toppanel)
        topbox.add_widget(self.word_to_show)
        mainbox.add_widget(topbox)
        alphabet = GridLayout(cols=7, spacing=[2], size_hint=(1, .4))
        self.alphabet_button = ALPHABET_RU
        for letter in range(0, len(self.alphabet_button) - 5):
            self.alphabet_button[letter] = Button(
                text=self.alphabet_button[letter],
                font_size=26,
                on_press=self.user_letter,
                background_color=[.64, .74, .76, 1],
                background_normal='')
            alphabet.add_widget(self.alphabet_button[letter])
        alphabet.add_widget(Widget())
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
        self.contentpopup = BoxLayout(orientation='vertical',
                                      padding=[6])
        self.contentpopuptext = Label(text='Побед/Проигрышей: '+str(self.win)+'/'+str(self.lose),
                                      size_hint=(1, .8))
        contentpopupbutton = GridLayout(cols=2, spacing=[2], size_hint=(1, .2))
        self.contentpopupbutton1 = Button(text="Выход",
                                          background_color=[.64, .74, .76, 1],
                                          background_normal='',
                                          on_press=self.exithangman)
        self.contentpopupbutton2 = Button(text="Еще раз",
                                          background_color=[.64, .74, .76, 1],
                                          background_normal='',
                                          on_press=self.restart)
        contentpopupbutton.add_widget(self.contentpopupbutton1)
        contentpopupbutton.add_widget(self.contentpopupbutton2)
        self.contentpopup.add_widget(self.contentpopuptext)
        self.contentpopup.add_widget(contentpopupbutton)
        self.popup = Popup(title='Сыграем еще раз?',
                           content=self.contentpopup,
                           size_hint=(None, None), size=(400, 300),
                           auto_dismiss=False, background_color=(.86, .90, .93, .7),
                           separator_color=(.86, .90, .93, .7))
        return mainbox

    def user_letter(self, instance):
        self.letter = str(instance.text)
        instance.font_size = 20
        instance.disabled = True
        if self.check(self.letter, self.right_answer):
            instance.background_color = [0, 1, 0, 1]
            instance.background_normal = ''
            ind = [i for i, j in list(enumerate(self.right_answer)) if j == self.letter]
            for index in ind:
                self.printinglist[index] = self.right_answer[index]
            self.word_to_show.text = ' '.join(self.printinglist)
            if self.is_finishing():
                self.popup.open()
        else:
            instance.background_color = [1, 0, 0, 1]
            instance.background_normal = ''
            self.user_error += 1
            self.user_er.text = 'Ошибок: '+str(self.user_error)+'/'+str(TRIES)
            if self.is_finishing():
                self.popup.open()


if __name__ == '__main__':
    HangmanApp().run()