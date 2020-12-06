from kivy.app import App 

from kivy.app import App
# Play audio
from kivy.uix.button import Button
# Mostly vertical layout
from kivy.uix.boxlayout import BoxLayout 
# Text, titles
from kivy.uix.label import Label
# Virtual keyboard, can mess with later
from kivy.uix.vkeyboard import VKeyboard
# For background image
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

def on_enter(instance, value):
    # enter key 
    print('User pressed enter in', instance)
    print(value)

class BambookApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        type_in = TextInput(text='Hello', multiline=False)
        type_in.bind(on_text_validate=on_enter)

        layout.add_widget(type_in)
        return layout
        # #bg = Image(source='assets/bamboo.png')
        # parent = BoxLayout(orientation='vertical')
        # #parent.add_widget(bg)
        # l = Label(text="The quick brown fox...") 
        # keeb = VKeyboard()
        # parent.add_widget(l)
        # parent.add_widget(keeb)
        # bg.add_widget(parent)
        # #return Button()
        # return bg
        


if __name__ == '__main__':
    # Attempt to load audio here first


    app = BambookApp()
    app.run()