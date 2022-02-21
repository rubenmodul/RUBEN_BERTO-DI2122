import sys
import os
import mysql.connector

from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarCategoryAxis, QStackedBarSeries
from PySide6.QtGui import QAction, QIcon, QPainter, QPixmap
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QDialog,
    QDialogButtonBox,
    QComboBox,
    QHBoxLayout,
    QSpinBox
)

ruta_base = os.path.dirname(__file__)

# Dialeg per a exir
class DialogExit(QDialog):
    # Indiquem que no te pare per a que aparegua damunt de la finstra
    def __init__(self, parent=None):
        super().__init__(parent)

        # Dialogos
        self.setWindowTitle("Dialeg eixir")
        self.setStyleSheet("background-color: #d3dbda;")

        self.buttons_dialog = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.buttons_dialog = QDialogButtonBox(self.buttons_dialog)
        self.buttons_dialog.accepted.connect(self.accept)
        self.buttons_dialog.rejected.connect(self.reject)

        self.layout_dialeg = QVBoxLayout()
        mensatgeEixir = QLabel("Estas seguro que quieres salir?")
        self.layout_dialeg.addWidget(mensatgeEixir)
        self.layout_dialeg.addWidget(self.buttons_dialog)
        self.setLayout(self.layout_dialeg)

    # Tornar a la pantalla de login
    def tornarLogin(self):
        self.hide()
        if (__name__ == '__main__'):
            self = MainWindow()
            if (__name__ == '__main__'):
                w.show()

    # Eixir
    def exit(self):
        dlg = DialogExit()
        if dlg.exec_():
            app.closeAllWindows()
        else:
            pass
    
    def checkInAbout(self):
        self.hide()
        miConexion = mysql.connector.connect(host='localhost',
                                            user= 'root',
                                            passwd='1234',
                                            db='estadistiques')
        sql_insert = "INSERT INTO usuario (nomUser, passwd) VALUES (%s, %s);"
        records = [(self.lineUsuario.text(), self.linePasswd.text())]
        with miConexion.cursor() as cursor:
            cursor.executemany(sql_insert, records)
            miConexion.commit()
        w.show()

# Pantalla User
class User(QMainWindow):
    def __init__(self):
        super().__init__()

        self.estadistica = Estadistica()
        self.aboutFinestra = About()

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.setWindowTitle("Usuario")

        # Creamos e importamos los png para los QAction
        icon_path = os.path.join(ruta_base, "PNGs/door-open-out.png")
        LogOut = QAction(QIcon(icon_path), "&Log out", self)
        LogOut.setStatusTip("Log out")
        LogOut.triggered.connect(self.tornarLogin)

        icon_path = os.path.join(ruta_base, "PNGs/cross-button.png")
        salir = QAction(QIcon(icon_path), "&Salir", self)
        salir.setStatusTip("Salir")
        salir.triggered.connect(self.exit)

        icon_path = os.path.join(ruta_base, "PNGs/smiley-medium.png")
        about = QAction(QIcon(icon_path), "&About", self)
        about.setStatusTip("About")
        about.triggered.connect(self.finestraAbout)

        # Creamos el menu
        menu = self.menuBar()
        
        # Añadimos los QAction al menu
        menu_action = menu.addMenu("&Options")
        menu_action.addAction(LogOut)
        menu_action.addAction(about)
        menu_action.addAction(salir)

        # Layouts
        self.layoutUser = QVBoxLayout()
        layoutTopSide = QHBoxLayout()
        layoutEquips = QVBoxLayout()
        self.layoutJugadors = QVBoxLayout()
        layoutBoto = QVBoxLayout()
        self.layoutEstadistica = QVBoxLayout()

        # Layout Equipos
        labelEquips = QLabel()
        labelEquips.setText("Mis Equipos")

        self.boxEquips = QComboBox()
        self.boxEquips.addItem("")
        self.boxEquips.addItem("Prebenjamin A")
        self.boxEquips.addItem("Alevin B")

        layoutEquips.addWidget(labelEquips)
        layoutEquips.addWidget(self.boxEquips)

        # Layout Jugadors
        self.labelJugadors = QLabel()
        self.labelJugadors.setText("Jugadores")

        self.boxJuagdors = QComboBox()
        self.llistaJugadorsPrebenjamin = ["Antonio Garcia", "Jose Martinez", "Francisco Lopez",
        "Juan Sanchez", "Pedro Gomez", "Jesus Fernandez"
        ]
        self.llistaJugadorsAlevin = ["Andres Cano", "Ramon Garrido", "Enrique Gil", "Alvaro Ortiz",
        "Emilio Valero", "Diego Rodenas"
        ]
        self.layoutJugadors.addWidget(self.labelJugadors)
        self.boxEquips.currentTextChanged.connect(self.comprovarEquip)

        self.layoutJugadors.addWidget(self.boxJuagdors)

        #Boto
        labelEstadistica = QLabel("Estadistica de jugadores")
        botoEstadistica = QPushButton("Estadistica")
        layoutBoto.addWidget(labelEstadistica)
        layoutBoto.addWidget(botoEstadistica)
        botoEstadistica.clicked.connect(self.checkInEstadistica)

        #Boto Mostrar Estadistiques
        self.botoMostrar = QPushButton("Mostrar Grafica")
        self.botoMostrar.clicked.connect(self.add_estadisticas)

        #Layout Estadistica
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.layoutEstadistica.addWidget(self.chart_view)

        # Añadim layouts al principal
        self.layoutUser.addWidget(centralWidget)
        self.setStyleSheet("background-color: #d3dbda;")
        self.layoutUser.addLayout(layoutTopSide)
        layoutTopSide.addLayout(layoutEquips)
        layoutTopSide.addLayout(self.layoutJugadors)
        layoutTopSide.addLayout(layoutBoto)
        self.layoutUser.addLayout(self.layoutEstadistica)
        self.layoutUser.addWidget(self.botoMostrar)

        widget = QWidget()
        widget.setLayout(self.layoutUser)
        self.setCentralWidget(widget)

        self.setFixedSize(QSize(500, 350))


    # Añadir estadistiques a la grafica
    def add_estadisticas(self):

        self.chart.removeAllSeries()

        # Lista donde guardamos la sentencia del select
        llistaEstadistica = []
        miConexion = mysql.connector.connect(host='localhost',
                                             user='root',
                                             passwd='1234',
                                             db='estadistiques')
        mycursor = miConexion.cursor()

        sql = f"SELECT * FROM jornadaJugador WHERE nomJugador = %s && jornada = %s;"
        adr = (self.boxJuagdors.currentText(), self.estadistica.boxJornadas.currentIndex()+1)

        mycursor.execute(sql, adr)

        myresult = mycursor.fetchall()

        # Añadimos los resultados a la lista
        for i in myresult:
            llistaEstadistica.append(i)

        # Variables que necesitamos
        self.goles = llistaEstadistica[0][2]
        self.minutos = llistaEstadistica[0][3]
        self.actitud = llistaEstadistica[0][4]

        self.setgoles = QBarSet("Goles")
        self.setminutos = QBarSet("Minutos")
        self.setactitud = QBarSet("Actitut")

        self.setgoles.append([self.goles, 0, 0])
        self.setminutos.append([0, self.minutos, 0])
        self.setactitud.append([0, 0, self.actitud])

        estadisticas = QStackedBarSeries()
        estadisticas.append(self.setgoles)
        estadisticas.append(self.setminutos)
        estadisticas.append(self.setactitud)

        self.chart.addSeries(estadisticas)
        self.chart.setTitle(self.boxJuagdors.currentText())
        self.chart.setAnimationOptions(QChart.AllAnimations)

        self.chart.createDefaultAxes()

        self.chart.removeAxis(self.chart.axisX())

        axisX = QBarCategoryAxis()
        axisX.append(self.jornades)

    # Tornar a la pantalla de Login
    def tornarLogin(self):
        self.hide()
        if (__name__ == '__main__'):
            self = MainWindow()
            if (__name__ == '__main__'):
                w.show()

    #  Eixir
    def exit(self):
        dlg = DialogExit()
        if dlg.exec_():
            app.closeAllWindows()
        else:
            pass

    def checkInEstadistica(self):
        self.estadistica.jugador = self.boxJuagdors.currentText()
        self.estadistica.show()
    
    def finestraAbout(self):
        self.aboutFinestra.show()

    # Funcion para comprovar que cambien los jugadores segun el equipo seleccionado
    def comprovarEquip(self, t):
        if t == "Prebenjamin A":
            self.boxJuagdors.clear()
            for i in self.llistaJugadorsPrebenjamin:
                self.boxJuagdors.addItem(i)

        elif t == "Alevin B":
            self.boxJuagdors.clear()
            for i in self.llistaJugadorsAlevin:
                self.boxJuagdors.addItem(i)

# Pantalla Estadística
class Estadistica(QMainWindow):
    def __init__(self):
        super().__init__()

        self.jugador=""

        self.setWindowTitle("Estadísticas")

        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #d3dbda;")

        # Jornadas
        labelJornades = QLabel()
        labelJornades.setText("Jornadas")

        self.boxJornadas = QComboBox()
        listaJornadas = ["1", "2", "3", "4", "5"]

        for i in listaJornadas:
            self.boxJornadas.addItem("Jornada " + i)

        layout.addWidget(labelJornades)
        layout.addWidget(self.boxJornadas)

        # Goles
        labelGoles = QLabel("Goles:")
        self.spinGoles = QSpinBox()
        self.spinGoles.setMaximum(15)
        self.spinGoles.setMinimum(0)

        layout.addWidget(labelGoles)
        layout.addWidget(self.spinGoles)

        # Minutos
        labelMinutos = QLabel("Minutos jugados:")
        self.spinMinutos = QSpinBox()
        self.spinMinutos.setMaximum(50)
        self.spinMinutos.setMinimum(0)

        layout.addWidget(labelMinutos)
        layout.addWidget(self.spinMinutos)

        # Actitud
        labelActitud = QLabel("Actitud:")
        self.actitud = QSpinBox()
        self.actitud.setMaximum(5)
        self.actitud.setMinimum(1)

        layout.addWidget(labelActitud)
        layout.addWidget(self.actitud)

        # Creem el botó de guardar
        self.buttonGuardar = QPushButton("Guardar")
        layout.addWidget(self.buttonGuardar)
        self.buttonGuardar.clicked.connect(self.guardar)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # Hacemos el insert para guardar los datos que ponemos en estadistica
    def guardar(self):
        self.hide()
        miConexion = mysql.connector.connect(host='localhost',
                                            user= 'root',
                                            passwd='1234',
                                            db='estadistiques')
        sql_insert = "INSERT INTO jornadaJugador (jornada, nomJugador, goles, minutos, actitud) VALUES (%s, %s, %s, %s, %s);"
        records = [(self.boxJornadas.currentIndex()+1, self.jugador, int(self.spinGoles.text()), int(self.spinMinutos.text()), int(self.actitud.text()))]
        with miConexion.cursor() as cursor:
            cursor.executemany(sql_insert, records)
            miConexion.commit()

# Pantalla About
class About(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        layoutAbout = QVBoxLayout()
        self.setStyleSheet("background-color: #d3dbda;")

        labelAbout = QLabel("Esta aplicación ha sido creada por:")
        layoutAbout.addWidget(labelAbout)

        # Layout de los nombres arriba de las imagenes
        layoutNoms = QHBoxLayout()

        labelCarles = QLabel("Carles")
        layoutNoms.addWidget(labelCarles)
        layoutAbout.addLayout(layoutNoms)

        labelRuben = QLabel("Ruben")
        layoutNoms.addWidget(labelRuben)
        layoutNoms.addLayout(layoutNoms)
        
        # Layout de las imagenes
        layoutImagenes = QHBoxLayout()
        labelImgCarles = QLabel()
        icon_path = os.path.join(ruta_base, "img/Carles.jpg")
        pixmapCarles = QPixmap(icon_path)
        self.resize(pixmapCarles.width(), pixmapCarles.height())
        labelImgCarles.setPixmap(pixmapCarles)
        layoutImagenes.addWidget(labelImgCarles)
        layoutAbout.addLayout(layoutImagenes)

        labelImgRuben = QLabel()
        icon_path = os.path.join(ruta_base, "img/Ruben.jpg")
        pixmapRuben = QPixmap(icon_path)
        self.resize(pixmapRuben.width(), pixmapRuben.height())
        labelImgRuben.setPixmap(pixmapRuben)
        layoutImagenes.addWidget(labelImgRuben)
        layoutAbout.addLayout(layoutImagenes)

        # Label para los links de contacto
        labelContactar = QLabel("Contacta con nosotros a traves de:")
        layoutAbout.addWidget(labelContactar)

        labelLinkCarles = QLabel()
        urlLink = "<a href=\"https://carles.cdi@gmail.com\">Correo de Carles</a>"
        labelLinkCarles.setText(urlLink)
        layoutAbout.addWidget(labelLinkCarles)

        labelLinkRuebn = QLabel()
        urlLink = "<a href=\"https://rubenmodul@gmail.com\">Correo de Ruben</a>"
        labelLinkRuebn.setText(urlLink)
        layoutAbout.addWidget(labelLinkRuebn)

        # Action de volver al usuario
        icon_path = os.path.join(ruta_base, "PNGs/navigation-180.png")
        actionAbout = QAction(QIcon(icon_path),"&Tornar al usuari", self)
        actionAbout.triggered.connect(self.tornarUser)

        menu = self.menuBar()

        menuAbout = menu.addMenu("&Opcions")
        menuAbout.addAction(actionAbout)

        widget = QWidget()
        widget.setLayout(layoutAbout)
        self.setCentralWidget(widget)

    def tornarUser(self):
        self.hide()

# Pantalla Login
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("App Futbol")

        self.user = User()

        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #d3dbda;")

        # Label del error de nombre o contraseña incorrecto
        self.label = QLabel("", self)

        # Creem el LineEdit per a l'usuari
        self.usuari = QLineEdit("")
        self.usuari.setPlaceholderText("Usuario")
        layout.addWidget(self.usuari)

        # Creem el LineEdit per a la contrasenya
        self.passwd = QLineEdit("")
        self.passwd.setEchoMode(QLineEdit.Password)
        self.passwd.setPlaceholderText("Contraseña")
        layout.addWidget(self.passwd)

        # Creem el botó de Login
        button = QPushButton("Login")
        button.clicked.connect(self.checkIn)
        layout.addWidget(button)

        icon_path = os.path.join(ruta_base, "PNGs/cross-button.png")
        salir = QAction(QIcon(icon_path), "&Salir", self)
        salir.setStatusTip("Salir")
        salir.triggered.connect(self.exit)

        menu = self.menuBar()

        menu_principal = menu.addMenu("&Options")
        menu_principal.addAction(salir)

        layout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # Sacamos los datos de la base de datos para entrar en el usuario seleccionado
    def checkIn(self):
        listaUsuarios = []
        miConexion = mysql.connector.connect(host='localhost',
                                             user='root',
                                             passwd='1234',
                                             db='estadistiques')
        mycursor = miConexion.cursor()

        mycursor.execute("SELECT * FROM usuario")

        myresult = mycursor.fetchall()

        for i in myresult:
            listaUsuarios.append(i)
        
        if (self.usuari.text() == listaUsuarios[0][0] and self.passwd.text() == listaUsuarios[0][1]) or (self.usuari.text() == listaUsuarios[1][0] and self.passwd.text() == listaUsuarios[1][1]):
            self.hide()
            self.user.show()
        else:
            self.label.setText("Usuario o Contraseña incorrectos")

    # Salir
    def exit(self):
        dlg = DialogExit()
        if dlg.exec_():
            app.closeAllWindows()
        else:
            pass

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()