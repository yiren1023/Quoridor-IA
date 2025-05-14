""" Nom: REN
    prénom: Yi
    marticule: 000468901
    Date: 06/02/2019
"""

class Humain:
    def __init__(self, col, row,color,nbr_murs):
        self.col = col
        self.row = row
        self.color = color
        self.nbr_murs = nbr_murs

    def move(self, pCol, pRow):
        "permet un mouvement du pion"
        self.col = pCol
        self.row = pRow

    def getCol(self):
        "retourne la colonne du pion"
        return self.col

    def getRow(self):
        "retourne la ligne du pion"
        return self.row

    def getColor(self):
        "retourne la couleur du pion"
        return self.color

    def getMurs(self):
        "retourne le nombre de murs que possède le pion"
        return self.nbr_murs

    def dec_nbr_murs(self):
        "décrémente le nombre de murs"
        self.nbr_murs -=1

    def canMove(self,other,bordX,bordY,direction,lst_walls_h,lst_walls_v):
        "renvoie True si un mouvement peut etre effectue,sinon False"
        res = True
        if(direction == "right" and (self.getCol() == bordX or self.getCol()+1 == other.getCol() and self.getRow() == other.getRow() or self.wall_v_in_front(lst_walls_v,"right"))):
            res = False
        elif(direction == "left" and (self.getCol() == 0 or self.getCol()-1 == other.getCol() and self.getRow() == other.getRow() or self.wall_v_in_front(lst_walls_v,"left"))):
            res = False
        elif(direction == "up" and (self.getRow() == 0 or self.getRow()-1 == other.getRow() and self.getCol() == other.getCol() or self.wall_h_in_front(lst_walls_h,"up"))):
            res = False
        elif(direction == "down" and (self.getRow() == bordY or self.getRow()+1 == other.getRow()and self.getCol() == other.getCol() or self.wall_h_in_front(lst_walls_h,"down"))):
            res = False
        return res

    def win(self,destination):
        "renvoie True si le pion est gagné en fonction de la position dans le plateau,sinon False"
        res = False
        if(self.getRow() == destination):
            res = True
        return res

    def can_put_wall(self,lst_walls_h,lst_walls_v,type_walls,w_row,w_col,size):
        "renvoie True si le plion a le droit de poser un mur sur le plateau, sinon False"
        res = True
        if(type_walls == "horizontale" and (w_row,w_col) in lst_walls_h):
            res = False
        elif(type_walls == "verticale" and (w_row,w_col)in lst_walls_v):
            res = False
        elif(w_row > size-1 or w_col >size-1):
            res = False
        elif(self.getMurs() == 0):
            res = False
        return res

    def wall_h_in_front(self,lst_walls_h,direction):
        "renvoie True s'il y a un mur horizontal qui empeche le mouvement du pion sinon False"
        res = False
        pos = None
        if(direction == "up"):
            pos = (self.getRow()-1,self.getCol())
        elif(direction == "down"):
            pos = (self.getRow(),self.getCol())
        if(pos in lst_walls_h):
            res = True
        return res

    def wall_v_in_front(self,lst_walls_v,direction):
        "renvoie True s'il y a un mur vertical qui empeche le mouvement du pion sinon False"
        res = False
        pos = None
        if(direction == "right"):
            pos = (self.getRow(),self.getCol())
        elif(direction == "left"):
            pos = (self.getRow(),self.getCol()-1)
        if(pos in lst_walls_v):
            res = True
        return res

    def can_jump(self,other,bordX,bordY,direction,lst_walls_h,lst_walls_v):
        "renvoie True si le pion peut effectuer un saut"
        res = False
        up_wall = (self.getRow()-1,self.getCol())
        down_wall = (self.getRow(),self.getCol())
        left_wall = (self.getRow(),self.getCol()-1)
        right_wall =(self.getRow(),self.getCol())
        if(direction == "up" and self.getCol() == other.getCol() and self.getRow()-1 == other.getRow() and up_wall not in lst_walls_h and self.getRow()-2 >= 0):
            res = True
        elif(direction == "down" and self.getCol() == other.getCol() and self.getRow()+1 == other.getRow() and down_wall not in lst_walls_h and self.getRow()+2 <=bordY):
            res = True
        elif (direction == "right" and self.getCol()+1 == other.getCol() and self.getRow()== other.getRow() and right_wall not in lst_walls_v and self.getCol() + 2 <= bordX):
            res = True
        elif (direction == "left" and self.getCol()-1 == other.getCol() and self.getRow()== other.getRow() and left_wall not in lst_walls_v and self.getCol() -2 >=0):
            res = True
        return res









