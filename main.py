from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from playsound import playsound
from kivy.core.audio import SoundLoader
from kivy.uix.progressbar import ProgressBar
from gtts import gTTS

# size window
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 900)
Config.set('graphics', 'height', 650)
from kivy.core.window import Window

# background color
Window.clearcolor = (.86, .90, .93, 1)
#import random
#from words_for_hangman import RANDOM_WORDS
#from words_for_hangman import ALPHABET_RU
#import re
 
TRIES = 6
ALPHABET = [chr(x) for x in range(97, 97 + 26)]
LEVELS = ["l", "i", "hello world pleased to meet you", "h u", "Elephants are the largest land animals they eat only plants Even though elephants are very strong, they are the only mammals that cannot jump"]

class Bambook(App):
    def play_audio(value, *args):
        playsound('output.mp3')

    def exit_level(self, *args):
        # obvious
        App.get_running_app().stop()

    def next_level(self, arg):

        # Increment level counter
        self.level += 1
        self.cursor_index = 0
        # Update text
        self.excerpt = LEVELS[self.level]
        excerpt_ = self.excerpt.split(" ")
        blanks_ = ['-' * len(x) for x in excerpt_]

        self.final_blanks = " ".join(blanks_)
        self.final_blank_check = " ".join(blanks_)

        self.center_label.text = self.excerpt
        self.progress_text.text = self.final_blanks

        # Auto playback
        tts = gTTS(self.excerpt)
        tts.save('output.mp3')
        Clock.schedule_once(self.play_audio, 1)
        self.popup.dismiss()

    def build(self):
        # Window title
        # Words to display
        self.cursor_index = 0
        # Controls which text excerpt to use
        self.level = 0
        self.excerpt = LEVELS[self.level]#"luv u" #Elephants are the largest land animals they eat only plants Even though elephants are very strong, they are the only mammals that cannot jump"
        excerpt_ = self.excerpt.split(" ")
        blanks_ = ['-' * len(x) for x in excerpt_]
        self.final_blanks = " ".join(blanks_)
        self.final_blank_check = " ".join(blanks_)

        tts = gTTS(self.excerpt)
        tts.save('output.mp3')
        #sound = SoundLoader.load('output.wav')

        self.title = 'Bambook'
        mainbox = BoxLayout(orientation='vertical', padding=[6])
        middle_panel = BoxLayout(orientation='vertical', size_hint=(1, .6))
        toppanel = BoxLayout(orientation='horizontal', size_hint=(1, .2))
        bottom_panel = BoxLayout(orientation='horizontal', size_hint=(1, .2))

        #logobox = BoxLayout(orientation='horizontal',)
        #middle_panel.add_widget(im)
        #logobox.add_widget(im)
        #logobox.add_widget(Widget())

        #mainbox.add_widget(im)
        # TODO Add corner stats/info?
        #self.center_label = Label(text=self.excerpt, text_size=(800, 300), color=[0, 0, 0, 1], valign='center')
        self.center_label = Label(text=self.excerpt, text_size=(800, 300), color=[0, 0, 0, 1], valign='center', halign='center')
        im = Image(source='assets/logo.png')
        b = Button(text="Replay", on_press=self.play_audio)
        toppanel.add_widget(im)
        toppanel.add_widget(self.center_label)
        toppanel.add_widget(b)
 
        # Typing Progress
        self.progress_text = Label(text=self.final_blanks,
                                  font_size=40, size_hint=(1, .7),
                                  halign='center', valign='center',
                                  text_size=(800, 300), color=[0, 0, 0, 1])
        middle_panel.add_widget(toppanel)
        middle_panel.add_widget(self.progress_text)
        im2 = Image(source='assets/lv1.png')
        bottom_panel.add_widget(im2)
        pb = ProgressBar(value=10 * self.level, max=100)
        bottom_panel.add_widget(pb)
        #mainbox.add_widget(middle_panel)
        bottom_panel.add_widget(middle_panel)
        mainbox.add_widget(bottom_panel)

 
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
#        self.delete_button = Button(
#                text="delete",
#                font_size=26,
#                on_press=self.user_letter,
#                background_color=[.64, .74, .76, 1],
#                background_normal='')
        alphabet.add_widget(self.space_button)
#        alphabet.add_widget(self.delete_button)
 
        mainbox.add_widget(alphabet)

        # Restart Splash Screen
        self.contentpopup = BoxLayout(orientation='vertical',
                                      padding=[6])
        self.contentpopuptext = Label(text='You Earned a New Seed!', size_hint=(1, .8))
        contentpopupbutton = GridLayout(cols=2, spacing=[2], size_hint=(1, .2))
        self.contentpopupbutton1 = Button(text="Exit",
                                          background_color=[.64, .74, .76, 1],
                                          background_normal='',
                                          on_press=self.exit_level)
        self.contentpopupbutton2 = Button(text="Next Level",
                                          background_color=[.64, .74, .76, 1],
                                          background_normal='',
                                          on_press=self.next_level)
        contentpopupbutton.add_widget(self.contentpopupbutton1)
        contentpopupbutton.add_widget(self.contentpopupbutton2)
        self.contentpopup.add_widget(self.contentpopuptext)
        self.contentpopup.add_widget(contentpopupbutton)
        
        self.popup = Popup(title='Good Job!',
                           content=self.contentpopup,
                           size_hint=(None, None), size=(400, 300),
                           auto_dismiss=False, background_color=(.86, .90, .93, .7),
                           separator_color=(.86, .90, .93, .7))
        #sound.play()
        Clock.schedule_once(self.play_audio, 1)
        return mainbox
   
 
    def user_letter(self, instance):
        # Get button letter
        self.letter = str(instance.text)
        dex = self.cursor_index
        curr = self.final_blanks
       
        if self.letter == "space":
            self.letter = " "
            self.final_blanks = curr[:dex] + self.letter + curr[dex + 1:]
            self.progress_text.text = self.final_blanks
               
#        if self.letter == "delete":
#            if dex != 0:
#                self.final_blanks = curr[:dex -1] + self.final_blank_check[dex:]
#                self.cursor_index -= 1
#                dex = self.cursor_index
        # easier access to critical variables
        else:
            # Update displayed text, button text, move cursor
            self.final_blanks = curr[:dex] + self.letter + curr[dex + 1:]
            self.progress_text.text = self.final_blanks
            # To check at every character, look at same index of the above string and self.excerpt and check for a match
        # make a check to change letter to red
        if self.letter == self.excerpt[dex].lower():
            self.cursor_index += 1
        
        if self.cursor_index == len(self.excerpt):
            self.popup.open()
 
        # if self.progress_text == self.excerpt:
        #     print("GOOD JOB")
        # else:
        #     print("cHeCk YoUr WoRk")
        #print("HI")
   
 
if __name__ == '__main__':
    Bambook().run()