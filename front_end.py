# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:56:26 2019

@author: Chaitali
"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from start_main import getAnswerStr, start, getQues
 
 
class DemoApp(App):
    def build(self):
        self.box = BoxLayout(orientation='vertical', spacing=10)
        self.txt_question = TextInput()
        self.txt_answer = TextInput(readonly = 'True')
        self.txt_sugg_question = TextInput(readonly = 'True')
        self.btn_reset = Button(text='Reset', on_press=self.clear_txt)
        self.btn_answer = Button(text='Get Answer', on_press=self.get_ans)
        self.box.add_widget(self.txt_question)
        self.box.add_widget(self.txt_answer)
        self.box.add_widget(self.txt_sugg_question)
        self.box.add_widget(self.btn_answer)
        self.box.add_widget(self.btn_reset)
        return self.box
         
    def clear_txt(self, instance):
        self.txt_question.text = ''
        self.txt_answer.text = ''
        self.txt_sugg_question.text = ''
    
    def get_ans(self, instance):
        start(self.txt_question.text)
        self.txt_answer.text = getAnswerStr().strip()
        self.txt_sugg_question.text = getQues.strip()
 
if __name__ == '__main__':
    DemoApp().run()