import GUI
import sys
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc

## main ##
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  main_window = GUI.MainWindow(app) # appを引数に与えてインスタンスを生成
  main_window.show()
  sys.exit(app.exec())