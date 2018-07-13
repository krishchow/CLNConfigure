import Master
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import getpass
import tkinter as tk
from tkinter import ttk as ttk
from narrower import Narrower
from narrower import killProcess
from narrower import SelectionError
from threading import Thread
import time as T
from tkinter import messagebox
import sys

class LatencyException(Exception):
    pass

def navigate(user,password):
    try:
        WebDriverWait(browser,60).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "UTORid Login") and @class="btn btn-primary"]')))
    except:
        raise LatencyException("Your internet is lagging!")
    
    Utro = browser.find_element_by_xpath('//a[contains(text(), "UTORid Login") and @class="btn btn-primary"]')
    browser.execute_script("arguments[0].click();", Utro)
        
    userName = browser.find_element_by_id('inputID')
    passwordName = browser.find_element_by_id('inputPassword')

    userName.send_keys(user)
    passwordName.send_keys(password.strip())
    passwordName.submit()
    WebDriverWait(browser,180).until(EC.presence_of_element_located((By.ID, 'sideHorizMenuDiv')))

    jobs = browser.find_element_by_xpath('//a[contains(text(), "Jobs")]')
    browser.execute_script("arguments[0].click();", jobs)
    WebDriverWait(browser,60).until(EC.presence_of_element_located((By.ID, 'sideHorizMenuDiv')))

    jobs = browser.find_element_by_xpath('//a[contains(text(), "Off-Campus Jobs")]')
    browser.execute_script("arguments[0].click();", jobs)

    WebDriverWait(browser,60).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), " Search Off-Campus Job Postings ")]')))
    browser.execute_script("arguments[0].click();", browser.find_element_by_xpath('//a[contains(text(), " Search Off-Campus Job Postings ")]'))

    WebDriverWait(browser,60).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Search Job Postings")]')))
    button = browser.find_element_by_xpath('//a[contains(text(), "Search Job Postings")]')
    browser.execute_script("arguments[0].id = 'PLACEHOLERVALUE123';", button)
    browser.execute_script("document.getElementById('PLACEHOLERVALUE123').style.display = 'none';")
    browser.execute_script("document.getElementById('sideHorizMenuDiv').style.display = 'none';")

    render()

def render():
    root = tk.Tk()
    root.wm_geometry("200x100")
    tk.Label(root,text='Please make your selection').pack(side='top')
    pb = ttk.Progressbar(root,orient='horizontal',length=200,mode='indeterminate',maximum=18)
    pb.pack(side='top')
    pb.start()
    tk.Button(root,text='Submit Selection',command=lambda r=root,b=browser,prog=pb: writeNarrowed(r,b,prog)).pack(side='bottom')
    tk.mainloop()

def renderUserInfo():
    userinfo = []
    root = tk.Tk()
    root.wm_geometry("300x150")
    tk.Label(root,text='Login Information', anchor='center',font=('Arial',15)).pack(side='top',fill='x')
    userFrame = tk.Frame(root)
    passFrame = tk.Frame(root)
    tk.Label(userFrame, text='Username:', anchor='w', font=('Arial',15)).pack(side='left')
    tk.Label(passFrame, text='Password:', anchor='w', font=('Arial',15)).pack(side='left')
    UN = tk.Entry(userFrame);UN.pack(fill='x',expand=True)
    PW = tk.Entry(passFrame, show='\u2022');PW.pack(fill='x',expand=True)
    PW.bind("<Enter>", lambda e: PW.config(show=""))
    PW.bind("<Leave>", lambda e: PW.config(show="\u2022"))
    userFrame.pack(side='top',fill='x',pady=5)
    passFrame.pack(side='top',fill='x',pady=5)
    def paste():
        if UN.get() and PW.get():
            userinfo.append(UN.get())
            userinfo.append(PW.get())
            root.destroy()
    tk.Button(root,text='Submit',command=paste).pack(side='bottom',anchor='e')
    root.bind('<Return>', lambda e: paste())
    tk.mainloop()
    return userinfo

def writeNarrowed(root, browser,prog):
    narrow = Narrower(browser,root,prog)
    length = ''
    try:
        length = narrow.defineParameterlist()
    except SelectionError as e:
        messagebox.showerror('Select Error', e)
        killProcess('chromedriver.exe')
        browser.quit()
        root.destroy()
        sys.exit()
    except WebDriverException as e:
        messagebox.showerror('Closed Browser', e)
        killProcess('chromedriver.exe')
        browser.quit()
        root.destroy()
        sys.exit()
    if length:
        print(length)
        prog.stop()
        prog.configure(mode='determinate')
        prog["maximum"]=length
        runT = Thread(target = narrow.pullOptions)
        runT.setDaemon(True)
        runT.start()

if __name__ == '__main__':
    i = renderUserInfo()
    username = i[0]
    _pass = i[1]

    browser = Master.createBrowser(url='https://cln.utoronto.ca/home.htm',headless=False,blockImages=False,hideConsole=True)
    try:
        navigate(username,_pass)
    except LatencyException as e:
        messagebox.showerror('Internet Issues', e)
    except WebDriverException as e:
        messagebox.showerror('Chrome Closed', e)
    finally:
        browser.quit()
        
    killProcess('chromedriver.exe')
