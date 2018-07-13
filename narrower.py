from selenium import webdriver
from selenium.webdriver.support.ui import Select
import csv as csv
import tkinter as tk
from tkinter import ttk as ttk
from tkinter import messagebox
import time as T
import psutil

class SelectionError(Exception):
    pass

class Narrower():
    def __init__(self,browser,root,progbar):
        self.fields = []
        self.browser = browser
        self.root = root
        self.progress = progbar
        self.selectToOptions = {}
    def defineParameterlist(self):
        o = T.time()
        self.allSelects = self.browser.find_elements_by_xpath('//select[@class="input-xlarge"]')
        print(T.time()-o)
        if len(self.allSelects) == 0:
            raise SelectionError("Can't find any Selects")
        return len(self.allSelects)
    
    def pullOptions(self):
        try:
            for individual in self.allSelects:
                select = Select(individual)
                temp = [x.text for x in select.all_selected_options]
                print(temp)
                self.selectToOptions[individual.get_attribute('name')] = temp
                self.progress.step()
        except:
            messagebox.showerror('Error!','There was an error pulling your selections, try again')
            self.browser.quit()
            self.root.destroy()
        self.progress.configure(mode='indeterminate')
        self.progress.start()
        try:
            self.writeMap()
        except:
            messagebox.showerror('Error!','There was an error writing your selections, if you have the file open, please close it!')
            self.browser.quit()
            self.root.destroy()
        messagebox.showinfo('Complete',"All tags have been updated")
        self.root.destroy()
        killProcess('chromedriver.exe')
        
        
    def writeMap(self):
        #file = open("../tags.csv",'w',newline='')
        file = open("tags.csv",'w',newline='')
        fileWriter = csv.writer(file)
        for name in self.selectToOptions:
            print(name, '\n',self.selectToOptions[name])
            if self.selectToOptions[name] != [] and self.selectToOptions[name] != ['-All-']:
                fileWriter.writerow([name]+ self.selectToOptions[name])
        file.close()

def killProcess(string):
    for proc in psutil.process_iter():
        if proc.name() == string:
            print('donzo')
            proc.kill()
            
