""" Nom: REN
    prénom: Yi
    marticule: 000468901
    Date: 06/02/2019
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from interface import Ui_MainWindow
from main_partie3 import *
from PyQt5.QtGui import QPainter, QColor, QFont,QPen,QBrush
from PyQt5.QtCore import Qt
import sys
from humain import *

lst_walls_h = [] # liste des murs horizontals
lst_walls_v = [] # liste des murs verticals

class myDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(myDialog, self).__init__(parent)
        self.Ui = Ui_MainWindow()
        self.Ui.setupUi(self)
        self.setWindowTitle('jeu quoridor')

        self.jeu = Main()
        self.Ui.direction_label.setVisible(False)
        self.joueurSuiv = "blanc"
        self.draw = False

        self.Ui.loadFileButton.clicked.connect(self.loadFile)
        self.Ui.saveFileButton.clicked.connect(self.saveFile)
        self.Ui.newIAButton.clicked.connect(self.create_IA)
        self.Ui.trainIAButton.clicked.connect(self.trainIA)
        """self.Ui.ia_humainButton.clicked.connect(self.iavsHumain()) ne fonctionne pas :("""
        self.Ui.comparepushButton.clicked.connect(self.compareIA)
        self.Ui.humainButton.clicked.connect(self.humainVShuamin)
        self.Ui.upButton.clicked.connect(self.up)
        self.Ui.downButton.clicked.connect(self.down)
        self.Ui.leftButton.clicked.connect(self.left)
        self.Ui.rightButton.clicked.connect(self.right)
        self.Ui.murpushButton.clicked.connect(self.putWall_button)

        self.setEnabled_button(False)


    def updateView(self):
        self.Ui.msg_Label.setText(self.jeu.get_msg())
        self.Ui.train_comp_progressBar.reset()
        self.Ui.joueurSuivlabel.setText(self.joueurSuiv)
        self.update()

    def loadFile(self):
        self.jeu.load_file(self.Ui.fichier_charg_lineEdit.text())
        self.updateView()

    def saveFile(self):
        self.jeu.save_file(self.Ui.fichier_sav_lineEdit.text())
        self.updateView()

    def create_IA(self):
        neurones_interne = self.Ui.neurone_inter_spinBox.value()
        taille_plateau = self.Ui.taille_plateau_spinBox.value()
        nbr_murs = self.Ui.nbr_mur_spinBox.value()

        self.jeu.create(neurones_interne,taille_plateau,nbr_murs)
        self.updateView()

    def trainIA(self):

        eps = self.Ui.eps_doubleSpinBox.value()
        alpha = self.Ui.learning_rate_doubleSpinBox.value()
        lamb = self.Ui.lambda_doubleSpinBox.value()
        ls = self.Ui.strategy_comboBox.currentText()
        try:
            player1,player2 = self.jeu.train_IA(eps,alpha,lamb,ls)
            nbr_parties = self.Ui.nbr_entrainm_spinBox.value()
            self.Ui.msg_Label.setText("Entrainement en cours !")

            print('\nEntraînement (' + str(nbr_parties) + ' parties)')
            QtWidgets.QApplication.processEvents()

            for j in range(nbr_parties):
                self.progress(j,nbr_parties)
                playGame(player1, player2)
            self.jeu.set_msg("Entrainement est fini. ")
        except:
            self.jeu.set_msg("Il faut d'abord créer un IA")
        self.updateView()

    def compareIA(self):
        filename = self.Ui.fichier_charg_lineEdit.text()
        nbr_parties = self.Ui.nbr_comp_spinBox.value()
        eps = self.Ui.eps_doubleSpinBox.value()
        try:
            players = self.jeu.compare(filename,eps)
            i = 0
            self.Ui.msg_Label.setText('Tournoi IA vs ' + filename + ' (' + str(nbr_parties) + ' parties, eps=' + str(eps) + ')')
            QtWidgets.QApplication.processEvents()
            for j in range(nbr_parties):
                self.progress(j,nbr_parties)
                playGame(players[i], players[(i + 1) % 2])
                i = (i + 1) % 2
            perf = (players[0].score / nbr_parties)*100
            self.jeu.set_msg("Parties gagnées par l'IA :"+  str(perf) +'%')
        except:
            self.jeu.set_msg("Il faut d'abord charger un dossier !")
        self.updateView()


    def progress(self,j,nbr_parties):
        if int(100*j/nbr_parties)>int(100*(j-1)/nbr_parties):
            pourcent = 100*j/nbr_parties
            self.Ui.train_comp_progressBar.setValue(pourcent)

    def iavsHumain(self):
        self.jeu.play_humain_vs_IA()
        self.updateView()

    def humainVShuamin(self):
        global lst_walls_h
        global lst_walls_v
        nbr_murs = self.Ui.nbr_mur_spinBox.value()
        self.setEnabled_button(True)
        self.draw = True
        taille = self.Ui.taille_plateau_spinBox.value()
        nbr_murs = self.Ui.nbr_mur_spinBox.value()
        middle_x = (taille - 1) // 2
        self.noir = Humain(middle_x, 0, "noir",nbr_murs)
        self.blanc = Humain(middle_x, taille - 1, "blanc",nbr_murs)
        self.Ui.murs_blanc_label.setText(str(nbr_murs))
        self.Ui.murs_noir_label.setText(str(nbr_murs))
        self.Ui.affichage_label_21.setVisible(False)
        lst_walls_h = []
        lst_walls_v = []

        self.updateView()

    def updateMoveMsg(self,color,move):
        if(move):
            self.jeu.set_msg("déplacement validé !")
        else:
            self.jeu.set_msg("mur est placée !")
        if(color == "blanc"):
            self.joueurSuiv = "noir"
        else:
            self.joueurSuiv = "blanc"

    def win(self,color):
        taille = self.Ui.taille_plateau_spinBox.value()
        if (color == "blanc"):
            if (self.blanc.win(0)):
                self.setEnabled_button(False)
                self.jeu.set_msg("joueur blanc a gagné !")
        elif(color == "noir"):
            if (self.noir.win(taille - 1)):
                self.setEnabled_button(False)
                self.jeu.set_msg("joueur noir a gagné !")

    def put_wall(self,type_wall,row_w,col_w,color):
        taille = self.Ui.taille_plateau_spinBox.value()
        if(type_wall == "horizontale"):
            lst_walls_h.append((row_w,col_w))
            if(col_w == taille-1 and (row_w,col_w-1) not in lst_walls_h):
                lst_walls_h.append((row_w,col_w-1))
            else:
                lst_walls_h.append((row_w, col_w +1))

        elif(type_wall == "verticale"):
            lst_walls_v.append((row_w,col_w))
            if(row_w == taille-1 and (row_w-1,col_w) not in lst_walls_v ):
                lst_walls_v.append((row_w-1,col_w))
            else:
                lst_walls_v.append((row_w+1,col_w))
        if (color == "blanc"):
            self.blanc.dec_nbr_murs()
            self.Ui.murs_blanc_label.setText(str(self.blanc.getMurs()))
        elif (color == "noir"):
            self.noir.dec_nbr_murs()
            self.Ui.murs_noir_label.setText(str(self.noir.getMurs()))

    def move_pion(self): # effectue les mouvements des pions
        bouton = self.Ui.direction_label.text()
        taille = self.Ui.taille_plateau_spinBox.value()
        type_wall = self.Ui.type_wallcomboBox.currentText()
        row_wall = self.Ui.row_WspinBox.value()
        col_wall = self.Ui.col_WspinBox.value()
        if (self.joueurSuiv == "blanc"):
            if (bouton == "up" and self.blanc.can_jump(self.noir, taille - 1, taille - 1, "up", lst_walls_h, lst_walls_v)):
                self.updateMoveMsg("blanc", True)
                self.blanc.move(self.blanc.getCol(), self.blanc.getRow() - 2)

            elif (bouton == "up" and self.blanc.canMove(self.noir, taille - 1, taille - 1, "up",lst_walls_h,lst_walls_v)):
                self.updateMoveMsg("blanc",True)
                self.blanc.move(self.blanc.getCol(), self.blanc.getRow() - 1)

            elif (bouton == "down" and self.blanc.can_jump(self.noir, taille - 1, taille - 1, "down", lst_walls_h, lst_walls_v)):
                self.updateMoveMsg("blanc", True)
                self.blanc.move(self.blanc.getCol(), self.blanc.getRow() + 2)

            elif(bouton == "down" and self.blanc.canMove(self.noir, taille - 1, taille - 1, "down",lst_walls_h,lst_walls_v)):
                self.updateMoveMsg("blanc",True)
                self.blanc.move(self.blanc.getCol(), self.blanc.getRow() + 1)

            elif (bouton == "left" and self.blanc.can_jump(self.noir, taille - 1, taille - 1, "left", lst_walls_h, lst_walls_v)):
                self.updateMoveMsg("blanc", True)
                self.blanc.move(self.blanc.getCol() - 2, self.blanc.getRow())

            elif (bouton == "left" and self.blanc.canMove(self.noir, taille - 1, taille - 1, "left",lst_walls_h,lst_walls_v)):
                self.updateMoveMsg("blanc",True)
                self.blanc.move(self.blanc.getCol()-1, self.blanc.getRow())

            elif (bouton == "right" and self.blanc.can_jump(self.noir, taille - 1, taille - 1, "right", lst_walls_h, lst_walls_v)):
                self.updateMoveMsg("blanc", True)
                self.blanc.move(self.blanc.getCol() + 2, self.blanc.getRow())

            elif (bouton == "right" and self.blanc.canMove(self.noir, taille - 1, taille - 1, "right",lst_walls_h,lst_walls_v)):
                self.updateMoveMsg("blanc",True)
                self.blanc.move(self.blanc.getCol()+1, self.blanc.getRow())

            elif(bouton == "mur" and self.blanc.can_put_wall(lst_walls_h,lst_walls_v,type_wall,row_wall,col_wall,taille)):
                self.updateMoveMsg("blanc",False)
                self.put_wall(type_wall,row_wall,col_wall,"blanc")

            else:
                if(bouton == "mur" and self.blanc.getMurs() == 0):
                    self.jeu.set_msg("Pas de mur disponible !")
                else:
                    self.jeu.set_msg("déplacement invalide")

        elif (self.joueurSuiv == "noir"):

            if (bouton == "up" and self.noir.can_jump(self.blanc, taille - 1, taille - 1, "up", lst_walls_h, lst_walls_v)):
                self.updateMoveMsg("noir", True)
                self.noir.move(self.noir.getCol(), self.noir.getRow() - 2)

            elif (bouton == "up" and self.noir.canMove(self.blanc, taille - 1, taille - 1, "up",lst_walls_h,lst_walls_v)):
                self.updateMoveMsg("noir",True)
                self.noir.move(self.noir.getCol(), self.noir.getRow() - 1)

            elif (bouton == "down" and self.noir.can_jump(self.blanc, taille - 1, taille - 1, "down", lst_walls_h, lst_walls_v)):
                self.updateMoveMsg("noir", True)
                self.noir.move(self.noir.getCol(), self.noir.getRow() + 2)

            elif(bouton == "down" and self.noir.canMove(self.blanc, taille - 1, taille - 1, "down",lst_walls_h,lst_walls_v)):
                self.updateMoveMsg("noir",True)
                self.noir.move(self.noir.getCol(), self.noir.getRow() + 1)

            elif (bouton == "left" and self.noir.can_jump(self.blanc, taille - 1, taille - 1, "left", lst_walls_h, lst_walls_v)):
                self.updateMoveMsg("noir", True)
                self.noir.move(self.noir.getCol() - 2, self.noir.getRow())

            elif (bouton == "left" and self.noir.canMove(self.blanc, taille - 1, taille - 1, "left",lst_walls_h,lst_walls_v)):
                self.updateMoveMsg("noir",True)
                self.noir.move(self.noir.getCol()-1, self.noir.getRow())

            elif (bouton == "right" and self.noir.can_jump(self.blanc, taille - 1, taille - 1, "right", lst_walls_h, lst_walls_v)):
                self.updateMoveMsg("noir", True)
                self.noir.move(self.noir.getCol() + 2, self.noir.getRow())

            elif (bouton == "right" and self.noir.canMove(self.blanc, taille - 1, taille - 1, "right",lst_walls_h,lst_walls_v)):
                self.updateMoveMsg("noir",True)
                self.noir.move(self.noir.getCol()+1, self.noir.getRow())

            elif (bouton == "mur" and self.noir.can_put_wall(lst_walls_h,lst_walls_v, type_wall, row_wall,col_wall,taille)):
                self.updateMoveMsg("noir", False)
                self.put_wall(type_wall, row_wall, col_wall, "noir")
            else:
                if(bouton == "mur" and self.noir.getMurs() == 0):
                    self.jeu.set_msg("Pas de mur disponible !")
                else:
                    self.jeu.set_msg("déplacement invalidé")
        self.win("blanc")
        self.win("noir")
        self.updateView()

    def putWall_button(self):
        self.Ui.direction_label.setText("mur")
        self.move_pion()

    def up(self):
        self.Ui.direction_label.setText("up")
        self.move_pion()


    def down(self):
        self.Ui.direction_label.setText("down")
        self.move_pion()

    def left(self):
        self.Ui.direction_label.setText("left")
        self.move_pion()


    def right(self):
        self.Ui.direction_label.setText("right")
        self.move_pion()

    def draw_pion(self,pq,x0,y0,col,row):
        taille = self.Ui.taille_plateau_spinBox.value()
        cellSize = int(self.Ui.plateau_label.width()) // taille
        offset = 5

        x = offset + x0 + cellSize * col
        y = offset + y0 + cellSize * row
        pq.drawEllipse(x, y, cellSize - offset * 2, cellSize - offset * 2)

    def draw_wall(self,pq, x0, y0):
        taille = self.Ui.taille_plateau_spinBox.value()
        cellSize = int(self.Ui.plateau_label.width()) // taille
        pq.setPen(QPen(Qt.yellow, 6, Qt.SolidLine))

        for pos in lst_walls_h: # dessine les murs horizontals
            row = pos[0]
            col = pos[1]
            x1 = cellSize * col + x0
            x2 = x1 + cellSize
            y = cellSize + row * cellSize + y0
            pq.drawLine(x1, y, x2, y)

        for pos in lst_walls_v: # dessine les murs verticals
            row = pos[0]
            col = pos[1]
            x = cellSize * col + cellSize + x0
            y1 = cellSize * row + y0
            y2 = y1 + cellSize
            pq.drawLine(x, y1, x, y2)

    def setEnabled_button(self,bol): # desactiver les boutons des mouvements des pions
        self.Ui.upButton.setEnabled(bol)
        self.Ui.downButton.setEnabled(bol)
        self.Ui.leftButton.setEnabled(bol)
        self.Ui.rightButton.setEnabled(bol)
        self.Ui.murpushButton.setEnabled(bol)

    def paintEvent(self,e):

        if (self.draw is False):
            return

        painter = QPainter(self)
        taille = self.Ui.taille_plateau_spinBox.value()
        painter.begin(self)

        cellSize = int(self.Ui.plateau_label.width()) // taille  # la taille de plateau_lab est fixé, width = height
        x0 = self.Ui.plateau_label.x()
        y0 = self.Ui.plateau_label.y()

        painter.setBrush(Qt.red)
        painter.drawRect(x0, y0, cellSize * taille, cellSize * taille)

        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

        for i in range(taille): # dessine les cases du plateau
            for j in range(taille):
                painter.drawRect(x0 + j * cellSize, y0 + i * cellSize, cellSize, cellSize)

        painter.setBrush(Qt.black)
        self.draw_pion(painter,x0,y0,self.noir.getCol(),self.noir.getRow())

        painter.setBrush(Qt.white)
        self.draw_pion(painter, x0, y0, self.blanc.getCol(), self.blanc.getRow())

        self.draw_wall(painter,x0,y0)
        painter.end()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    u = myDialog()
    u.show()
    sys.exit(app.exec_())


