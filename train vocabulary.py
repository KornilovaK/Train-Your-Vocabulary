from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QApplication, QAction,  QLineEdit
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
from PyQt5.Qt import Qt

import sys
from random import randint


class App(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Train vocabulary')
        self.setFixedSize(640, 480)
        self.setInit()
        self.setStyleSheet('background: #faf1e8;')

    def setInit(self):
        self.add_word = QPushButton('Add new word', self)
        self.add_word.setGeometry(QRect(100, 200, 200, 80))
        self.add_word.setStyleSheet('background: white;')
        self.add_word.clicked.connect(self.new_word)
        self.add_word.show()

        self.training = QPushButton('Start training', self)
        self.training.setGeometry(QRect(340, 200, 200, 80))
        self.training.setStyleSheet('background: white;')
        self.training.clicked.connect(self.start_train)
        self.training.show()

    def new_word(self):
        self._window()
        try:
            self.line_add.show()
            self.line_add.setText('Enter new word')
            self.line_translation.show()
            self.line_translation.setText('Enter translation')
            self.button_add.show()
        except:
            self.line_add = QLineEdit('Enter new word', self)
            self.line_add.setGeometry(220, 120, 200, 50)
            self.line_add.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.line_add.show()

            self.line_translation = QLineEdit('Enter translation', self)
            self.line_translation.setGeometry(220, 190, 200, 50)
            self.line_translation.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.line_translation.show()

            self.button_add = QPushButton("Add", self)
            self.button_add.setStyleSheet('background: white;')
            self.button_add.setGeometry(220, 280, 200, 80)
            self.button_add.clicked.connect(self.add_to_dictionary)
            self.button_add.show()

    def add_to_dictionary(self):
        text = self.line_add.text()
        translation = self.line_translation.text()

        self.line_add.clear()
        self.line_translation.clear()

        file = open('dictionary.txt', 'a')
        file.write(f'{text}-{translation}\n')
        file.close()

    def start_train(self):
        self._window()
        self.count = 0
        self.numbers = []
        self.init_train()

        with open('dictionary.txt', 'r') as f:
            self.words = f.read().splitlines()
            f.close()

        try:
            self.random_number = randint(0, len(self.words) - 1)
            self.numbers.append(self.random_number)
            self.label_train.setText(self.words[self.random_number].split('-')[1])
            self.label_train.setStyleSheet("background-color: #faf1e8")
            self.line_train.clear()
        except:
            self.label_train.setText('Nothing is here!')
            self.line_train.hide()
            self.button_train.hide()

    def init_train(self):
        try:
            self.label_train.show()
            self.line_train.show()
            self.button_train.show()
        except:
            self.label_train = QLabel(self)
            self.label_train.move(220, 120)
            self.label_train.setFixedWidth(200)
            self.label_train.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.label_train.show()

            self.line_train = QLineEdit(self)
            self.line_train.setGeometry(220, 160, 200, 50)
            self.line_train.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.line_train.show()

            self.button_train = QPushButton('Check', self)
            self.button_train.setGeometry(220, 220, 200, 60)
            self.button_train.setStyleSheet('background: white;')
            self.button_train.clicked.connect(self.check_word)
            self.button_train.show()

    def check_word(self):
        self.button_train.hide()

        if self.count+1 == len(self.words):
            self.finish_button = QPushButton('Finish', self)
            self.finish_button.setStyleSheet('background: white;')
            self.finish_button.clicked.connect(self.finish)
            self.finish_button.setGeometry(220, 220, 200, 60)
            self.finish_button.show()
        else:
            self.next_button = QPushButton('Next', self)
            self.next_button.clicked.connect(self.next_word)
            self.next_button.setStyleSheet('background: white;')
            self.next_button.setGeometry(220, 220, 200, 60)
            self.next_button.show()

        text = self.line_train.text()
        word = self.words[self.random_number]

        if text.lower() != word.split('-')[0].lower():
            self.label_train.setStyleSheet("background-color: red")
            self.line_train.setText(word.split('-')[0].lower())
        else:
            self.label_train.setStyleSheet("background-color: lightgreen")

    def finish(self):
        self.line_train.hide()
        self.label_train.hide()
        self.finish_button.hide()
        self.button_train.hide()
        self.setInit()
        self.menuBar().hide()

    def next_word(self):
        self.button_train.show()
        self.count += 1
        self.next_button.hide()
        self.line_train.clear()
        self.random_number = randint(0, len(self.words) - 1)

        if self.random_number not in self.numbers:
            pass
        else:
            while self.random_number in self.numbers:
                self.random_number = randint(0, len(self.words) - 1)

        self.numbers.append(self.random_number)
        print(self.numbers)

        self.label_train.setText(self.words[self.random_number].split('-')[1])
        self.label_train.setStyleSheet("background-color: #faf1e8")

    def _window(self):
        self.add_word.hide()
        self.training.hide()
        self._menuBar()

    def _menuBar(self):
        self.backAction = QAction(QIcon("back.svg"), "Back")
        self.backAction.triggered.connect(self._backAction)

        menuBar = self.menuBar()
        menuBar.addAction(self.backAction)
        menuBar.setStyleSheet("background: white")
        menuBar.show()

    def _backAction(self):
        self.menuBar().hide()
        try:
            self.label_train.hide()
        except:
            pass
        try:
            self.button_add.hide()
            self.line_add.hide()
            self.line_translation.hide()
        except:
            self.button_train.hide()
            self.line_train.hide()
            self.label_train.hide()
        try:
            self.finish_button.hide()
        except:
            pass
        try:
            self.next_button.hide()
        except:
            pass

        self.setInit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    ex = App()
    ex.show()
    sys.exit(app.exec_())