import webdriver
from selenium.webdriver.common.service import Service
import errno
import os
import platform
import subprocess
from subprocess import PIPE
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils
from win32process import CREATE_NO_WINDOW
from selenium.webdriver.chrome.options import Options as ChromeOptions
try:
    from subprocess import DEVNULL
    HAS_NATIVE_DEVNULL = True
except ImportError:
    DEVNULL = -3
    _HAS_NATIVE_DEVNULL = False


class myService(Service):
    def start(self):
        """
        Starts the Service.

        :Exceptions:
         - WebDriverException : Raised either when it can't start the service
           or when it can't connect to the service
        """
        try:
            cmd = [self.path]
            cmd.extend(self.command_line_args())
            if any("hide_console" in arg for arg in self.command_line_args()):
                self.process = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, creationflags=0x08000000)
            else:
                self.process = subprocess.Popen(cmd, env=self.env, close_fds=platform.system() != 'Windows', stdout=self.log_file, stderr=self.log_file, stdin=PIPE)
        except TypeError:
            raise
        except OSError as err:
            if err.errno == errno.ENOENT:
                raise WebDriverException(
                    "'%s' executable needs to be in PATH. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            elif err.errno == errno.EACCES:
                raise WebDriverException(
                    "'%s' executable may have wrong permissions. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            else:
                raise
        except Exception as e:
            raise WebDriverException(
                "The executable %s needs to be available in the path. %s\n%s" %
                (os.path.basename(self.path), self.start_error_message, str(e)))
        count = 0
        while True:
            self.assert_process_still_running()
            if self.is_connectable():
                break
            count += 1
            time.sleep(1)
            if count == 30:
                raise WebDriverException("Can not connect to the Service %s" % self.path)
            

def createBrowser(url = '', headless=False, blockImages=True, hideConsole = False):
    chromeOptions = ChromeOptions()
    if blockImages: prefs = {"profile.managed_default_content_settings.images":2}; chromeOptions.add_experimental_option("prefs",prefs)
    if headless: chromeOptions.add_argument("--headless"); chromeOptions.add_argument("--window-size=1920x1080")
    chrome_serv = myService('path--to--exe.exe')
    chrome_serv.service_args = ["hide_console", ]
    if hideConsole: browser = webdriver.myWebDriver(chrome_options=chromeOptions, service_args=chrome_serv.service_args)
    else: browser = webdriver.myWebDriver(chrome_options=chromeOptions)
    #browser = webdriver.Chrome(chrome_options=chromeOptions)
    if url:
        browser.get(url)
    return browser
