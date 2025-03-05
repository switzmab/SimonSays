import sys
import random as rand
import os
from time import sleep
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class mainGame:
    round = 1
    seq = []
    l = False
    out = "default"
    
    def __init__(self, name):
        self.simon = name

    def getInput(self, color):
        return color

    def setOutput(self):
        num = rand.randint(1, 4)
        if num == 1: 
            self.out = "b"
        elif num == 2: 
            self.out = "r"
        elif num == 3: 
            self.out = "y"
        elif num == 4: 
            self.out = "g"
        else: 
            self.out = "b"
    
    def getOrder(self, i):
        return self.seq[i]
    def seqOrder(self, out):
        self.seq.append(out)

    def sequence(self, main_window):
        self.setOutput()
        self.seqOrder(self.out)
        for output in self.seq:
            print(f"Generated: {self.out}")
            if output == 'b':
                sleep(1)
                main_window.b_select()
            elif output == 'r':
                sleep(1)
                main_window.r_select()
            elif output == 'g':
                sleep(1)
                main_window.g_select()
            elif output == 'y':
                sleep(1)
                main_window.y_select()
            os.system('cls')
        print(f"Full sequence for round {self.round}: {self.seq}")

    def playerSequence(self, guess):
        if len(guess) != len(self.seq):
            print(f"Error: Guess length {len(guess)} does not match sequence length {len(self.seq)}")
            return 0
        
        for i in range(len(guess)):
            print(f"Comparing: {guess[i]} with {self.seq[i]}")
            if guess[i] != self.seq[i]:
                self.setLose()
                return 0
        self.round = self.round + 1
        print("SEQUENCE CORRECT, MOVING TO ROUND: ", self.round)
        return self.round

    def setLose(self):
        print("YOU LOSE!!")
        print("FINAL SCORE: ", self.round)
        self.l = True

    def getLose(self):
        return self.l


class MainWindow(QWidget):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.resize(500, 400)
        self.setWindowTitle("Simon Says Game")
        self.label = QLabel(self)
        self.label.setText("Welcome to Benji's game of Simon Says")
        self.label.move(125, 20)
        self.score = QLabel(self)
        self.score.setText(f"Score: {game.round}")
        
        # Set up the buttons
        self.r = QPushButton('RED')
        self.r.setStyleSheet('background-color: red; color: white')
        self.r.setFixedSize(250,120)
        self.r.clicked.connect(lambda: self.button_clicked('r'))
        
        self.b = QPushButton('BLUE')
        self.b.setStyleSheet('background-color: blue; color: white')
        self.b.setFixedSize(250,120)
        self.b.clicked.connect(lambda: self.button_clicked('b'))
        
        self.g = QPushButton('GREEN')
        self.g.setStyleSheet('background-color: green; color: white')
        self.g.setFixedSize(250,120)
        self.g.clicked.connect(lambda: self.button_clicked('g'))
        
        self.y = QPushButton('YELLOW')
        self.y.setStyleSheet('background-color: yellow; color: black')
        self.y.setFixedSize(250,120)
        self.y.clicked.connect(lambda: self.button_clicked('y'))
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.label)
        layout.addWidget(self.score)

        button_layout = QGridLayout()
        button_layout.addWidget(self.r, 0, 0)
        button_layout.addWidget(self.b, 0, 1)
        button_layout.addWidget(self.g, 1, 0)
        button_layout.addWidget(self.y, 1, 1)
        
        layout.addLayout(button_layout)
        
        self.user_sequence = []

        # Show the window
        self.show()

    def button_clicked(self, color):
        self.user_sequence.append(color)
        if len(self.user_sequence) == self.game.round:
            self.check_sequence()
    
    def check_sequence(self):
        if self.game.playerSequence(self.user_sequence):
            self.user_sequence = []
            self.game.sequence(self)
        else:
            self.label.setText("YOU LOSE!! Final score: {}".format(self.game.round))
    
    def r_select(self):
        self.flash_button(self.r, 'red', 'black', 'red')

    def b_select(self):
        self.flash_button(self.b, 'blue', 'black', 'blue')

    def g_select(self):
        self.flash_button(self.g, 'green', 'black', 'green')

    def y_select(self):
        self.flash_button(self.y, 'yellow', 'black', 'yellow')

    def flash_button(self, button, original_color, flash_color, text_color):
        button.setStyleSheet(f'background-color: {flash_color}; color: {original_color}')
        QTimer.singleShot(1000, lambda: button.setStyleSheet(f'background-color: {original_color}; color: {text_color}'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = mainGame('Simon')
    window = MainWindow(game)
    game.sequence(window)  # Generate the initial sequence

    # Start the event loop
    sys.exit(app.exec())
