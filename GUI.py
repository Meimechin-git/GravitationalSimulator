import asyncio
import sys
import time
import PySide6.QtWidgets as Qw
import PySide6.QtGui as Qg
import PySide6.QtCore as Qc
import engine

TASKBAR_HEIGHT = 50
FPS = 30

class MainWindow(Qw.QMainWindow):
    #コンストラクタ
    def __init__(self, app:Qw.QApplication):
        super().__init__() 
        self.setWindowTitle('Gravitation Simulator')
        #QTabWidget を作成
        self.tabs = Qw.QTabWidget()
        self.fps = FPS

        #「world properties」ボタンの生成と設定
        self.world_properties = Qw.QPushButton('World Properties',self)
        self.world_properties.clicked.connect(self.world_properties_listner)
       
        #「new object」ボタンの生成と設定
        self.new_object = Qw.QPushButton('New Object',self)
        self.new_object.clicked.connect(self.new_object_listner)

        #「clear」ボタンの生成と設定
        self.clear = Qw.QPushButton('Clear',self)
        self.clear.clicked.connect(self.clear_listner)

        self.start = Qw.QPushButton('Start',self)
        self.start.clicked.connect(self.start_listner)

        self.stop = Qw.QPushButton('Stop',self)
        self.stop.clicked.connect(self.stop_listner)

        self.world = engine.World()
        self.simulation_thread = None  # スレッドの初期値

       
        # ウィンドウの位置をスクリーン中央に設定
        rect = Qc.QRect()
        rect.setSize(Qc.QSize(800,500))
        rect.moveCenter(app.primaryScreen().availableGeometry().center())
        self.setGeometry(rect)

    #タスクバーを最適化
    def resizeEvent(self,event):
        width = self.width()
        height = self.height()
        self.world_properties.setGeometry(0,0,int(width*0.15),TASKBAR_HEIGHT-10)
        self.new_object.setGeometry(int(width*0.15),0,int(width*0.15),TASKBAR_HEIGHT-10)
        self.clear.setGeometry(int(width*0.3),0,int(width*0.15),TASKBAR_HEIGHT-10)
        self.start.setGeometry(int(width*0.70),0,int(width*0.15),TASKBAR_HEIGHT-10)
        self.stop.setGeometry(int(width*0.85),0,int(width*0.15),TASKBAR_HEIGHT-10)

    #シミュレーション画面を最適化
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        painter = Qg.QPainter(self)
        painter.setBrush(Qg.QBrush(Qg.QColor(50, 50, 50)))
        painter.drawRect(0, TASKBAR_HEIGHT, width, height)

        for object in self.world.objects:
            p_x = (object.p_x/self.world.width+1)*width/2
            p_y = (-object.p_y/self.world.height+1)*(height-TASKBAR_HEIGHT)/2
            r_x = object.r*width/self.world.width
            r_y = object.r*(height-TASKBAR_HEIGHT)/self.world.height
            painter.setBrush(Qg.QBrush(Qg.QColor(object.color)))  # 塗りつぶし色を赤に
            painter.drawEllipse(p_x-r_x/2,p_y-r_y/2+TASKBAR_HEIGHT,r_x,r_y)

    def world_properties_listner(self,event):
        dialog = WorldPropertiesDialog(self,world=self.world,window=self)
        if dialog.exec():  # OKボタンが押された場合のみ実行
            data = dialog.get_data()
            
            # 新しいオブジェクトを作成（engine.Object を仮に想定
            self.world.width = data["width"]
            self.world.height = data["height"]
            self.world.g = data["g"]
            self.fps = data["FPS"]
            # 画面を更新
            self.update()

    def new_object_listner(self,event):
        dialog = NewObjectDialog(self)
        if dialog.exec():  # OKボタンが押された場合のみ実行
            data = dialog.get_data()
            
            # 新しいオブジェクトを作成（engine.Object を仮に想定）
            new_object = engine.Object(
                data["mass"],
                data["r"],
                data["p_x"],
                data["p_y"],
                data["v_x"],
                data["v_y"],
                data["color"] 
            )
            # シミュレーターに追加
            self.world.objects.append(new_object)
            # 画面を更新
            self.update()

    def clear_listner(self,even):
        msgbox_title = 'オブジェクトの削除'
        msgbox_text = 'シミュレーション中のオブジェクトをすべて削除しますか？\n一度削除すると二度と復元できません。\n'
        # メッセージボックスの生成、表示、応答(戻値)の取得 
        ret = Qw.QMessageBox.question(
            self,          # 親ウィンドウ
            msgbox_title,  # タイトル
            msgbox_text,   # メッセージ本体
            Qw.QMessageBox.StandardButton.Ok | Qw.QMessageBox.StandardButton.Cancel, # 表示ボタン
            Qw.QMessageBox.StandardButton.Cancel    # デフォルトボタン
          )
        # 戻値に応じた処理
        if ret == Qw.QMessageBox.StandardButton.Ok:
            self.world.objects = []
            self.update()
        elif ret == Qw.QMessageBox.StandardButton.Cancel :
            pass
        else :
            pass

    def start_listner(self,even):
        if self.simulation_thread and self.simulation_thread.isRunning():
            return  # すでに実行中なら何もしない
        
        self.simulation_thread = SimulationThread(self)
        self.simulation_thread.start()

    def stop_listner(self,even):
        if self.simulation_thread:
            self.simulation_thread.stop()
            self.simulation_thread = None

class WorldPropertiesDialog(Qw.QDialog):
    def __init__(self, parent=None, world=None, window=None):
        super().__init__(parent)
        self.setWindowTitle("世界の設定")
        self.setModal(True)  # ダイアログをモーダル（閉じるまで他の操作不可）にする
        self.resize(300, 200)

        layout = Qw.QVBoxLayout(self)

        self.width_input = Qw.QSpinBox(self)
        self.width_input.setRange(-10000, 10000)
        self.width_input.setValue(world.width)
        self.width_input.setPrefix("横幅： ")

        self.height_input = Qw.QSpinBox(self)
        self.height_input.setRange(-10000, 10000)
        self.height_input.setValue(world.height)
        self.height_input.setPrefix("縦幅： ")

        self.g_input = Qw.QSpinBox(self)
        self.g_input.setRange(0, 100000)
        self.g_input.setValue(world.g)
        self.g_input.setPrefix("万有引力定数： ")

        self.fps_input = Qw.QSpinBox(self)
        self.fps_input.setRange(10, 100)
        self.fps_input.setValue(window.fps)
        self.fps_input.setPrefix("FPS： ")

        # ボタン（OK / キャンセル）
        self.ok_button = Qw.QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = Qw.QPushButton("キャンセル", self)
        self.cancel_button.clicked.connect(self.reject)

        # レイアウトに追加
        layout.addWidget(self.width_input)
        layout.addWidget(self.height_input)
        layout.addWidget(self.g_input)
        layout.addWidget(self.fps_input)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        """ユーザーが入力した値を取得"""
        return {
            "width": self.width_input.value(),
            "height": self.height_input.value(),
            "g": self.g_input.value(),
            "FPS": self.fps_input.value(),
        }

class NewObjectDialog(Qw.QDialog):
    """オブジェクトの設定を入力するダイアログ"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新しいオブジェクトの追加")
        self.setModal(True)  # ダイアログをモーダル（閉じるまで他の操作不可）にする
        self.resize(300, 200)

        layout = Qw.QVBoxLayout(self)

        self.mass_input = Qw.QSpinBox(self)
        self.mass_input.setRange(0, 1000)
        self.mass_input.setPrefix("質量： ")

        self.p_x_input = Qw.QSpinBox(self)
        self.p_x_input.setRange(-1000, 1000)
        self.p_x_input.setPrefix("初期位置 X： ")

        self.p_y_input = Qw.QSpinBox(self)
        self.p_y_input.setRange(-1000, 1000)
        self.p_y_input.setPrefix("初期位置 Y： ")

        self.v_x_input = Qw.QSpinBox(self)
        self.v_x_input.setRange(-1000, 1000)
        self.v_x_input.setPrefix("初速度 X： ")

        self.v_y_input = Qw.QSpinBox(self)
        self.v_y_input.setRange(-1000, 1000)
        self.v_y_input.setPrefix("初速度 Y： ")

        self.r_input = Qw.QSpinBox(self)
        self.r_input.setRange(1, 100)
        self.r_input.setPrefix("半径： ")

        self.color_button = Qw.QPushButton("色を選択", self)
        self.color_button.clicked.connect(self.select_color)
        self.selected_color = Qg.QColor(255, 0, 0)  # 初期色は赤

        # ボタン（OK / キャンセル）
        self.ok_button = Qw.QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = Qw.QPushButton("キャンセル", self)
        self.cancel_button.clicked.connect(self.reject)

        # レイアウトに追加
        layout.addWidget(self.mass_input)
        layout.addWidget(self.r_input)
        layout.addWidget(self.p_x_input)
        layout.addWidget(self.p_y_input)
        layout.addWidget(self.v_x_input)
        layout.addWidget(self.v_y_input)
        layout.addWidget(self.color_button)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

    def select_color(self):
        """色を選択するダイアログを開く"""
        color = Qw.QColorDialog.getColor(self.selected_color, self, "色を選択")
        if color.isValid():
            self.selected_color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()};")

    def get_data(self):
        """ユーザーが入力した値を取得"""
        return {
            "mass":self.mass_input.value(),
            "r": self.r_input.value(),
            "p_x": self.p_x_input.value(),
            "p_y": self.p_y_input.value(),
            "v_x": self.v_x_input.value(),
            "v_y": self.v_y_input.value(),
            "color": self.selected_color
        }
    
# シミュレーション用スレッド
class SimulationThread(Qc.QThread):
    update_signal = Qc.Signal()  # 画面更新のシグナル

    def __init__(self,window):
        super().__init__()
        self.window = window
        self.world = window.world
        self.running = True  # スレッドの動作状態を管理

    def run(self):
        """シミュレーションの処理"""
        while self.running:
            self.world.update(self.window.fps)  # シミュレーションを更新
            self.window.update()
            time.sleep(1/self.window.fps)

    def stop(self):
        """スレッドを停止"""
        self.running = False
        self.wait()  # スレッド終了を待機

## main ##
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  main_window = MainWindow(app) # appを引数に与えてインスタンスを生成
  main_window.show()
  sys.exit(app.exec())