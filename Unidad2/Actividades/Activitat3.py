from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys
import argparse


class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()
        #Dar valor a las variables
        title, text, fixed, size_x, size_y = "La meua aplicació", "Aceptar", False, 300, 200
        
        #Si damos parametros, cambia el valor de la variable
        if args.title:
            title = args.title
        if args.button_text:
            text = args.button_text
        if args.fixed_size:
            fixed = args.fixed_size
        if args.size:
            size_x, size_y = args.size
        #Titulo    
        self.setWindowTitle(title)
        self.setGeometry(300, 150, size_x, size_y)
        if fixed:
            self.setFixedSize(size_x, size_y)

        #Creamos el boton
        self.button = QPushButton(text)
        self.setCentralWidget(self.button)
        self.button.clicked.connect(QApplication.instance().quit)

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--title", help="Title of application")
    parser.add_argument("-b", "--button-text", help="Button text")
    parser.add_argument("-f", "--fixed-size", action="store_true",
                        help="Window fixed size")
    parser.add_argument("-s", "--size", nargs=2, metavar=("SIZE_X", "SIZE_Y"), type=int,
                        help="Size of windows")
    arguments = parser.parse_args()

    app = QApplication(sys.argv)
    window = MainWindow(arguments)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()