__author__ = "Mehmet Cagri Aksoy - github.com/mcagriaksoy"
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Mehmet Cagri Aksoy"

# import libraries
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.uic import loadUi

from datetime import date
import requests, shutil, platform, sys, ctypes

# global variables
host_file_path = ""

# main window class
class main_window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        loadUi("ui.ui", self)
        self.pushButton.clicked.connect(self.updateFromNetwork)
        self.pushButton_2.clicked.connect(self.copyHostFiletoSystem)
    
    def downloadfilefromUrl(self, level):
        url = "https://o0.pages.dev/" + level + "/hosts.txt"
        r = requests.get("https://o0.pages.dev/mini/hosts.txt", allow_redirects=True)
        open("./hosts", 'wb').write(r.content)
        today = date.today()
        self.label_8.setText(today.strftime("%d/%m/%Y"))
    
    def copyHostFiletoSystem(self):
        shutil.copyfile("./hosts", host_file_path)
        self.label_9.setStyleSheet("background-color: cyan")
        self.label_9.setText("Protected")

    def updateFromNetwork(self):
        protection_level = self.horizontalSlider.value()
        if protection_level == 1:
            level = "mini"
        elif protection_level == 2:
            level = "Lite"
        elif protection_level == 3:
            level = "Pro"
        elif protection_level == 4:
            level = "Xtra"
        else:
            return
        
        self.downloadfilefromUrl(level)
    
def am_i_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# start ui design
def start_ui_design():
    if am_i_admin():
        # Code of your program here
        global host_file_path 
        if platform.system() == "Windows":
            host_file_path = "C:\Windows\System32\drivers\etc\hosts"
        elif platform.system() == "Linux":
            host_file_path = "/etc/hosts"
        else:
            print("Your system is not supported")
            return

        app = QApplication(sys.argv)
        widget = main_window()
        widget.show()
        sys.exit(app.exec())
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
