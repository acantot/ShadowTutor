import sys
from utiles.nlp import sub_a_texto, procesar, seleccionar_vocabulario
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)


class AbrirInterfaz(QWidget):

    def __init__(self, nombre_de_archivo_audio, nombre_de_archivo_sub, vocabulario_seleccionado, frases):
        from ui_ventana import Ui_Widget
        super().__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self, nombre_de_archivo_audio, nombre_de_archivo_sub)
        self.setWindowTitle("ShadowTutor")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.ui.caja_ejercicios.setTitle(nombre_de_archivo_audio)
        self.ui.palabras=vocabulario_seleccionado
        self.ui.frases=frases


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("ShadowTutor")
        self.setWindowIcon(QIcon("images/icon.png"))
        audio_imagen = QPixmap("images/audio_file.png")
        subtitulo_imagen = QPixmap("images/subs.png")
        self.texto=""
        self.layout = QVBoxLayout()
        self.button_audio = QPushButton()
        self.button_audio.setText("Upload audio/video")
        self.button_audio.setIcon(audio_imagen)
        self.button_audio.clicked.connect(lambda: self.abrir_archivo(self.button_audio, ("*.mp4 *.mp3", "Upload audio/video")))
        self.button_audio.setFont(QFont("Segoe UI", 10))
        self.layout.addWidget(self.button_audio)
        self.button_srt = QPushButton()
        self.button_srt.setText("Upload subtitles")
        self.button_srt.setIcon(subtitulo_imagen)
        self.button_srt.setFont(QFont("Segoe UI", 10))
        self.button_srt.clicked.connect(lambda: self.abrir_archivo(self.button_srt, ("*.srt", "Upload subtitles")))
        self.layout.addWidget(self.button_srt)
        button_listo = QPushButton("Go!")
        button_listo.setFont(QFont("Segoe UI", 10))
        button_listo.clicked.connect(self.listo)
        self.layout.addWidget(button_listo)
        w = QWidget()
        w.setLayout(self.layout)
        self.setCentralWidget(w)
        
    def listo(self):
        sub_a_texto(self)
        procesar(self.texto)
        vocabulario=procesar(self.texto)[0]
        vocabulario_seleccionado=seleccionar_vocabulario(vocabulario)
        frases=procesar(self.texto)[1]
        self.ventana_ejercicios = AbrirInterfaz(self.fileName_audio[0], self.fileName_srt[0], vocabulario_seleccionado, frases)
        self.ventana_ejercicios.show()
        window.close()

    def abrir_archivo(self, identificador_boton, formato):
        if self.button_audio==identificador_boton:
            self.fileName_audio = QFileDialog.getOpenFileName(self, formato[1], "material/", f"{formato[0]}")
            self.button_audio.setText(self.fileName_audio[0])
        else:
            self.fileName_srt = QFileDialog.getOpenFileName(self, formato[1], "material/", f"{formato[0]}")
            self.button_srt.setText(self.fileName_srt[0])


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()