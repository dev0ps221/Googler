#!/usr/bin/env python3
from sys import argv
from googlesearch import search
from os import system
import flet as ft
from colorama import just_fix_windows_console,init as init_colors,Fore, Back, Style
just_fix_windows_console()
init_colors()
class bcolors:
    def colorize(self,text,fore='magenta'):
        fore           =       getattr(Fore,fore.upper()) if hasattr(Fore,fore.upper()) else ""
        return          fore   +       text  

def text(msg,color='magenta'):
    print(bcolors.colorize(bcolors,msg,color))
    print(Style.RESET_ALL)

class Googler:
    def search(self,query):
        res,err             =   None,None
        try:
            res = search(query, advanced=True, lang=self.lang)
        except Exception as e:
            err = e        
        return res,err
    def process_single_console_search(self,query):
        res,err = self.search(query)
        if(res) : 
            text('search results for :'+query)
            for r in res:
                text("[["+r.title+"]]",'blue')
                text(r.description+':','white')
                text("Lien ici: ]=-> "+r.url+" <-=[",'green')
        if err:
            text('erreurs: ','orange')
            text(e, 'red')
    def process_single_gui_search(self,query):
        query = self.search_field.value
        res,err = self.search(query)
        if(res) :
            self.search_results.controls =  [

            ] 
            for r in res:
                self.search_results.controls .append(
                    ft.Row(
                        [
                            ft.Text(r.title,style=ft.TextThemeStyle.HEADLINE_MEDIUM)
                            ,ft.Text(r.description,style=ft.TextThemeStyle.HEADLINE_MEDIUM)
                            ,ft.Text(r.url,style=ft.TextThemeStyle.HEADLINE_MEDIUM)
                        ]
                    )
                )
                self.page.update()
        if err:
            text('erreurs: ','orange')
            text(e, 'red')
    def updateGuiTitle(self,title):
        if self.page:
            self.page.title = title
            self.page.update()
    def gui(self,page: ft.Page):
        self.page                           = page
        self.page.title                     = self.updateGuiTitle('Googler Gui v1') 
        self.search_field                   = ft.TextField(label="recherche...")
        self.search_button                  = ft.FilledButton(text="googler")
        self.search_button.on_click         = self.process_single_gui_search
        self.search_results                 = ft.Column()
        self.page.add(
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.search_field,self.search_button
                ]
            ),self.search_results
        )
        self.page.update()
    def gui_search(self):
        ft.app(target=self.gui)
    def console_search(self):
        query = ""
        if len(argv) > 1:
            query = " ".join(argv[1:])
        else:
            query = input("Googler>")
        while query != 'exit' or query != 'quit':
            self.process_single_console_search(query)
            query = input("Googler>")
    def __init__(self,lang='fr',type='console'):
        self.type = type
        self.lang = lang
    def run(self):
        if  self.type == 'console':
            self.console_search()
        if  self.type == 'gui':
            self.gui_search()
