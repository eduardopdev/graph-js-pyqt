from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

from PyQt6.QtCore import QObject, pyqtSlot, QUrl, QVariant
import sys
import os

class CallHandler(QObject):


    @pyqtSlot(result=QVariant)
    def test(self):
        print('call received')
        return QVariant({"abc": "def", "ab": 22})
    
    # take an argument from javascript - JS:  handler.test1('hello!')
    @pyqtSlot(QVariant, result=QVariant)
    def test1(self, args):
      print('i got')
      print(args)
      return "ok"

class WebView(QWebEngineView):

    def __init__(self):
        super(WebView, self).__init__()

        self.channel = QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject('handler', self.handler)
        self.page().setWebChannel(self.channel)

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
        local_url = QUrl.fromLocalFile(file_path)

        self.load(local_url)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  view = WebView()
  view.show()
  sys.exit(app.exec())
