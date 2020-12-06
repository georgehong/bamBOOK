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
from playsound import playsound
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from gtts import gTTS

# size window
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 900)
Config.set('graphics', 'height', 1200)
Window.clearcolor = (.86, .90, .93, 1)
 
TRIES = 6
ALPHABET = [chr(x) for x in range(97, 97 + 26)]

# Load first level from text file
file1 = open('levelN.txt', 'r') 
Lines = file1.readlines() 
final_lines = []
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
# Removing punctuations in string 
# Using loop + punctuation string 
for line in Lines:
    current = line
    for ele in current:  
        if ele in punc:  
            current = current.replace(ele, "")  
    final_lines.append(current)
LEVELS = [line.strip() for line in final_lines]
file1.close()

class Bambook(App):
    def play_audio(value, *args):
        playsound('output.mp3')

    def exit_level(self, *args):
        App.get_running_app().stop()

    def next_level(self, arg):
        # Final completion button
        if self.level == len(LEVELS):
            self.pb.value = self.level * 10
            self.popup2.open()
            return

        self.cursor_index = 0
        # Update text
        self.excerpt = LEVELS[self.level]
        self.raw_excerpt = Lines[self.level]

        excerpt_ = self.excerpt.split(" ")
        blanks_ = ['-' * len(x) for x in excerpt_]

        self.final_blanks = " ".join(blanks_)
        self.final_blank_check = " ".join(blanks_)
        self.center_label.text = self.raw_excerpt
        self.progress_text.text = self.final_blanks
        self.pb.value = self.level * 10

        filepath = 'assets/lv' + str(self.level) + '.png'
        self.im2.source = filepath
        # Increment level counter
        self.level += 1

        # Auto playback
        tts = gTTS(self.excerpt)
        tts.save('output.mp3')
        Clock.schedule_once(self.play_audio, 1)

        self.popup.dismiss()
        self.popup0.dismiss()

    def build(self):
        
        self.contentpopup0 = BoxLayout(orientation='vertical',
                                      padding=[6])
        contentpopupbutton0 = GridLayout(cols=1, spacing=[2], size_hint=(1, 1))
        self.contentpopupbutton0 = Button(text="", background_normal='assets/screen.png', background_down='assets/normal5.png', on_press=self.next_level ,size_hint=(1, 1))
        
        self.contentpopup0.add_widget(contentpopupbutton0)
        contentpopupbutton0.add_widget(self.contentpopupbutton0)
        
        self.popup0 = Popup(title=' ',
                           content=self.contentpopup0,
                           size_hint=(None, None), size=(900, 900),
                           auto_dismiss=False, background_color=(.43, .51, .83, .7),
                           separator_color=(.43, .51, .83, .7))
        
        
        # Window title, Words to display
        self.cursor_index = 0
        # Controls which text excerpt to use
        self.level = 0
        self.excerpt = LEVELS[self.level]  
        self.raw_excerpt = Lines[self.level]

        excerpt_ = self.excerpt.split(" ")
        blanks_ = ['-' * len(x) for x in excerpt_]
        self.final_blanks = " ".join(blanks_)
        self.final_blank_check = " ".join(blanks_)

        tts = gTTS(self.excerpt)
        tts.save('output.mp3')

        self.title = 'Bambook'
        mainbox = BoxLayout(orientation='vertical', padding=[24])
        middle_panel = BoxLayout(orientation='vertical', size_hint=(1, .4))
        toppanel = BoxLayout(orientation='horizontal', size_hint=(1, .2))
        toppanel2 = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        bottom_panel = BoxLayout(orientation='horizontal', size_hint=(1, .3))

        self.center_label = Label(text=self.raw_excerpt, text_size=(800, 1100), font_size=40, color=[0, 0, 0, 1], valign='center', halign='center') 
        im = Image(source='assets/logo1.png', size=(100,100))
        b = Button(text="", background_normal='assets/normal6.png', background_down='assets/normal6.png', on_press=self.play_audio, size=(50,75))
        toppanel.add_widget(im)
        toppanel.add_widget(Widget())
        toppanel.add_widget(b)
        toppanel2.add_widget(self.center_label)
 
        # Typing Progress
        self.progress_text = Label(text=self.final_blanks,
                                  font_size=40, size_hint=(1, .7),
                                  halign='center', valign='center',
                                  text_size=(800, 300), color=[0, 0, 0, 1])
        mainbox.add_widget(toppanel)
        middle_panel.add_widget(toppanel2)
        middle_panel.add_widget(self.progress_text)

        filepath = 'assets/lv' + str(self.level) + '.png'
        self.im2 = Image(source=filepath)
        bottom_panel.add_widget(self.im2)
        self.pb = ProgressBar(value=10 * self.level, max=10 * len(LEVELS))
        bottom_panel.add_widget(self.pb)
        mainbox.add_widget(middle_panel)
 
        alphabet = GridLayout(cols=7, spacing=[5], size_hint=(1, .4))
        self.alphabet_button = ALPHABET
 
        for letter in range(0, len(self.alphabet_button) - 5):
            self.alphabet_button[letter] = Button(
                text=self.alphabet_button[letter],
                font_size=26,
                on_press=self.user_letter,
                background_color=[.46, .61, .56, 1],
                background_normal='')
            alphabet.add_widget(self.alphabet_button[letter])
 
        alphabet.add_widget(Widget())
 
        for letter in range(len(self.alphabet_button) - 5, len(self.alphabet_button)):
            self.alphabet_button[letter] = Button(
                text=self.alphabet_button[letter],
                font_size=26,
                on_press=self.user_letter,
                background_color=[.46, .61, .56, 1],
                background_normal='')
            alphabet.add_widget(self.alphabet_button[letter])
       
        self.space_button = Button(
                text="space",
                font_size=26,
                on_press=self.user_letter,
                background_color=[.46, .61, .56, 1],
                background_normal='')
        alphabet.add_widget(self.space_button)
 
        mainbox.add_widget(alphabet)
        mainbox.add_widget(bottom_panel)
        # Restart Splash Screen
        self.contentpopup = BoxLayout(orientation='vertical',
                                      padding=[6])
        self.contentpopuptext = Label(text='Level Passed!', size_hint=(1, .8))
        contentpopupbutton = GridLayout(cols=2, spacing=[2], size_hint=(1, .2))
        self.contentpopupbutton1 = Button(text="Exit",
                                          background_color=[.46, .61, .56, 1],
                                          background_normal='',
                                          on_press=self.exit_level)
        self.contentpopupbutton2 = Button(text="Next Level",
                                          background_color=[.46, .61, .56, 1],
                                          background_normal='',
                                          on_press=self.next_level)
        contentpopupbutton.add_widget(self.contentpopupbutton1)
        contentpopupbutton.add_widget(self.contentpopupbutton2)
        self.contentpopup.add_widget(self.contentpopuptext)
        self.contentpopup.add_widget(contentpopupbutton)
        
        self.popup = Popup(title='Good Job!',
                           content=self.contentpopup,
                           size_hint=(None, None), size=(400, 300),
                           auto_dismiss=False, background_color=(.43, .51, .83, .7),
                           separator_color=(.43, .51, .83, .7))
        # Construct completion popup
        self.contentpopup2 = BoxLayout(orientation='vertical',
                                      padding=[6])
        self.contentpopuptext2 = Label(text='Practice Complete', size_hint=(1, .8))
        contentpopupbutton2 = GridLayout(cols=2, spacing=[2], size_hint=(1, .2))
        self.contentpopupbutton3 = Button(text="Done",
                                          background_color=[.46, .61, .56, 1],
                                          background_normal='',
                                          on_press=self.exit_level)
        self.contentpopupbutton4 = Button(text="Next",
                                          background_color=[.46, .61, .56, 1],
                                          background_normal='',
                                          on_press=self.exit_level)
        contentpopupbutton2.add_widget(self.contentpopupbutton3)
        contentpopupbutton2.add_widget(self.contentpopupbutton4)
        self.contentpopup2.add_widget(self.contentpopuptext2)
        self.contentpopup2.add_widget(contentpopupbutton2)
        
        self.popup2 = Popup(title='Good Job!',
                           content=self.contentpopup2,
                           size_hint=(None, None), size=(400, 300),
                           auto_dismiss=False, background_color=(.43, .51, .83, .7),
                           separator_color=(.43, .51, .83, .7))

        Clock.schedule_once(self.popup0.open, 0.1)
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
               
        # easier access to critical variables
        else:
            replace_letter = self.letter
            # Update displayed text, button text, move cursor
            if self.letter == self.excerpt[dex].lower():
                replace_letter = self.excerpt[dex]
            self.final_blanks = curr[:dex] + replace_letter + curr[dex + 1:]
            self.progress_text.text = self.final_blanks
            # To check at every character, look at same index of the above string and self.excerpt and check for a match
        if self.letter == self.excerpt[dex].lower():
            self.cursor_index += 1
        
        if self.cursor_index == len(self.excerpt):
            self.progress_text.text = self.raw_excerpt
            self.popup.open()
 
   
 
if __name__ == '__main__':
    Bambook().run()