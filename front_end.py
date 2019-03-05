# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:56:26 2019

@author: Chaitali
"""
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from start_main import getAnswerStr, start, getQues
 
 
class DemoApp(App):
    current_file = os.getcwd()
    global output_dir
    output_dir = current_file+ "\\outputModel"
    def build(self):
        self.box = BoxLayout(orientation='vertical', spacing=10)
        self.txt_question = TextInput()
        self.txt_answer = TextInput(readonly = 'True')
        self.txt_sugg_question = TextInput(readonly = 'True')
        self.btn_answer = Button(text='Get Answer', on_press=self.get_ans)
        self.box.add_widget(self.txt_question)
        self.box.add_widget(self.txt_answer)
        self.box.add_widget(self.txt_sugg_question)
        self.box.add_widget(self.btn_answer)
        return self.box
         
    def clear_txt(self, instance):
        self.txt_question.text = ''
        self.txt_answer.text = ''
        self.txt_sugg_question.text = ''
    
    def get_ans(self, instance):
        global output_dir
        start(str(self.txt_question.text), output_dir)
        self.txt_answer.text = str(getAnswerStr()).strip()
        self.txt_sugg_question.text = str(getQues()).strip()
 
if __name__ == '__main__':
    DemoApp().run()
