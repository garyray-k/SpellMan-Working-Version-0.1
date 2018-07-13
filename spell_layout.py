from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label 
from kivy.uix.stacklayout import StackLayout 
from kivy.uix.button import Button 
from kivy.uix.listview import ListView 

class Layout(App):
    def build(self):
        # screen manager steup
        sm = ScreenManager()

        # main menu setup
        main_menu = 

        # define Spell screen
        spell_layout = BoxLayout()
        # add big_layout to ScreenManger
        sm.add_widget(spell_layout)
        left_box = BoxLayout(orientation='vertical', spacing=10, size_hint=(.3, 1))
        right_box = StackLayout(size_hint=(.7, 1))
        left_top_box = ListView(size_hint=(1, .8))
        left_bottom_box = BoxLayout(size_hint=(1, .2))

        rb = Label(text='right box')
        ltb = Label(text='left top box')
        btn_rest = Button(text='Rest')
        btn_main = Button(text='Main Menu')
        btn_quit = Button(text='Quit')

        spell_layout.add_widget(left_box)
        spell_layout.add_widget(right_box)

        left_box.add_widget(left_top_box)
        left_box.add_widget(left_bottom_box)

        right_box.add_widget(rb)
        left_top_box.add_widget(ltb)
        left_bottom_box.add_widget(btn_rest)
        left_bottom_box.add_widget(btn_main)
        left_bottom_box.add_widget(btn_quit)

        return sm

if __name__ == "__main__":
    Layout().run()