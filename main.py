'''
Pathfinder Spell Manager v0.0.1
Author: Gary Ray Krause
Contact: krauseling@gmail.com
'''

# import kivy tools
from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label 
from kivy.uix.stacklayout import StackLayout 
from kivy.uix.button import Button
from kivy.uix.listview import ListView 
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.uix.listview import ListItemButton
from kivy.properties import ListProperty
from kivy.uix.listview import ListItemLabel

# import tools for db parsing
import pandas as pd
import xlrd

sp = pd.read_excel('/Users/garykrause/Dropbox/PathfinderSpellManager/SpellMan/spell_full_1.xlsx', sheet_name=0)
user_spells = pd.DataFrame()
user_spells = sp[sp['name'] == 'Bless']
user_spell_list = []
selected_spells_list = ['test']
cols = ['name', 'short_description', 'school', 'subschool', 'descriptor', 'casting_time', 'components', 'range', 'area', 'effect', 'targets', 'duration', 'saving_throw', 'spell_resistence','domain', 'description', 'source']

class SpellListButton(ListItemButton):
    pass

class ListLabel(ListItemLabel):
    pass

class SpellDescriptionLabel(Label):
    pass

class MainScreen(Screen):

    def clear_list(self):
        global user_spell_list
        user_spell_list.clear()
        pass

    def class_level_list_generator(self):
        # run this function on load to setup drop downs for main menu
        columns= list(sp)
        classes = []
        classes.extend(columns[26:41])
        classes.extend(columns[78:88])
        classes.sort()
        levels = range(1,10)
        # add levels to dropdown
        for l in levels:
            # manually specify button height and label it by level number
            btn = Button(text=str(l), size_hint_y=None, height=50)
            # update button text with that of selection
            btn.bind(on_release=lambda btn: self.ids.dd_level.select(btn.text))
            # add button to dropdown
            self.ids.dd_level.add_widget(btn)
        self.ids.dd_level.bind(on_select=lambda instance, x: setattr(self.ids.btn_level_dropdown, 'text', x))

        # add classes to dropdown
        for c in classes:
            btn = Button(text=str(c), size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.ids.dd_class.select(btn.text))
            self.ids.dd_class.add_widget(btn)
        self.ids.dd_class.bind(on_select=lambda instance, x: setattr(self.ids.btn_class_dropdown, 'text', x))
        pass

    def f_btn_manager(self):
        # input data and filter based on dropdowns
        global user_spells, user_spell_list, selected_spells_list
        # user validation
        try:
            user_level = int(self.ids.btn_level_dropdown.text)
        except ValueError:
            user_level = 1
        user_class = self.ids.btn_class_dropdown.text
        # user validation
        if user_class == 'Select a class...':
            user_class = 'wiz'
        user_spells = sp.loc[sp[user_class] <= user_level]
        user_spell_list.extend(user_spells['name'].tolist())
        self.manager.current = 'spell_select_screen'
        selected_spells_list = []

class SpellScreen(Screen):
    speller = ListProperty()
    
    def __init__(self, **kwargs):
        super(SpellScreen, self).__init__(**kwargs)

    def f_btn_rest(self):
        global selected_spells_list
        self.ids.left_top_box.adapter.data = []
        selected_spells_list = []
        self.manager.current = 'spell_select_screen'

    def load_spells(self):
        """ this will execute on entering the spell screen """
        global selected_spells_list
        self.speller = selected_spells_list
        self.ids.left_top_box.adapter.bind(on_selection_change=self.spell_selection)

    def f_btn_main(self):
        self.manager.current = 'main_screen'

    def spell_selection(self, *args):
        """ this will run when a spell is selected from the list to display all properties of the spell"""
        self.ids.right_box.clear_widgets()
        try:
            name = self.ids.left_top_box.adapter.selection[0].text
        except IndexError:
            name = 'Error!'
        self.ids.right_box.height = 0
        if name != 'Error!':
            for col in cols:
                text = str(user_spells[user_spells['name'] == name][col].iloc[0])
                if text == 'nan':
                    continue
                elif name == text:
                    lbl = SpellDescriptionLabel(
                    text=text,
                    id=name,
                    bold=True,
                    underline=True,
                    halign='left',
                    padding=(0, 1),
                    )
                else:
                    lbl = SpellDescriptionLabel(
                    text=col + ':  ' + text,
                    id=name,
                    halign='left',
                    padding=(0, 1),
                    )
                self.ids.right_box.add_widget(lbl)
            


class SpellSelectScreen(Screen):
    speller = ListProperty()

    # called on screen load to populate selectable list on left side of screen
    def list_user_spells(self):
        global user_spell_list
        user_spell_list.sort()
        self.speller = user_spell_list
        self.ids.user_spell_list_view.adapter.bind(on_selection_change=self.spell_selection)


    # call on screen exit
    def complete_rest(self):
        global selected_spells_list
        #selected_spells_list.append('test2')
        #selected_spells_list.append(self.ids.user_spell_list_view.adapter.selection)
        for s in self.ids.user_spell_list_view.adapter.selection:
           selected_spells_list.append(s.text)
           selected_spells_list.sort()
        self.manager.current = 'spell_screen'

    def spell_selection(self, *args):
        """ this will run when a spell is selected from the list to display all properties of the spell"""
        self.ids.all_spells_description.clear_widgets()
        try:
            name = self.ids.user_spell_list_view.adapter.selection[-1].text
        except IndexError:
            name = 'Error!'
        # self.ids.right_box.height = 0
        if name != 'Error!':
            for col in cols:
                text = str(user_spells[user_spells['name'] == name][col].iloc[0])
                if text == 'nan':
                    continue
                elif name == text:
                    lbl = SpellDescriptionLabel(
                    text=text,
                    id=name,
                    bold=True,
                    underline=True,
                    halign='left',
                    padding=(0, 1),
                    )
                else:
                    lbl = SpellDescriptionLabel(
                    text=col + ':  ' + text,
                    id=name,
                    halign='left',
                    padding=(0, 1),
                    )
                self.ids.all_spells_description.add_widget(lbl)


# main kivy app
class SpellManApp(App):

    def build(self): 

        spellman = ScreenManager()
        main_screen = MainScreen(name='main_screen', id='main_screen')
        spell_screen = SpellScreen(name='spell_screen', id='spell_screen')
        spell_select_screen = SpellSelectScreen(name='spell_select_screen', id='spell_select_screen')
        spellman.add_widget(main_screen)
        spellman.add_widget(spell_screen)
        spellman.add_widget(spell_select_screen)

        return spellman

# run the app
if __name__ == "__main__":
    SpellManApp().run()    