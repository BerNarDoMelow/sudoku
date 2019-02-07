
###METER ESTADO __INIT__ LOGO COM AS CLASSES THINGS
from things import *


class Estado:
    def __init__(self,size,block_x,block_y,positions=[]):
        ##
        self.block_x = block_x
        self.block_y = block_y
        self.size = [x for x in range(1,size + 1)]
        self.positions = positions


    def percept(self,position=(1,1,1)):
        """

        :param position: ponto de coordenadas, e numero do grupo (x,y,grupo)
        :return: dicionario com os pontos com mesmo x ou y,ou dentro de um grupo,
         correspondente á percecao no ponto position.
        """
        things = {
            "esq":list(map(lambda x:x[2],filter(lambda x: x[0] < position[0] and x[1] == position[1],self.positions))),
            "dir":list(map(lambda x:x[2],filter(lambda x: x[0] > position[0] and x[1] == position[1],self.positions))),
            "cima":list(map(lambda x:x[2],filter(lambda x: x[1] < position[1] and x[0] == position[0],self.positions))),
            "baixo":list(map(lambda x:x[2],filter(lambda x: x[1] > position[1] and x[0] == position[0],self.positions))),
            #"group":list(map(lambda x:x[2],filter(lambda x: x[3] == position[2],self.positions))),
        }
        return things


    def filter_perception(self,position):
        perception = self.percept(position)
        result = []
        for each in perception.values():
            result += map(lambda x:int(x),list(filter(lambda x:x != "#",each)))
        return result
        #return list(set(map(lambda x:int(x[2]),filter(lambda x:x[2]!= "#",perception.values()))))

    def filter_map(self,position):
        lista = list(filter(lambda x:x[2] == "#" and x[3] == position[3],self.positions))
        lista.remove(position)
        return lista

    def positions_left_in_group(self,position):
        return len(list(map(lambda x: x[2],filter(lambda x: x[3]==position[3],list(filter(lambda x: x[2] == "#",self.positions))))))


    def group(self,position):
        return list(set(map(lambda x: int(x[2]),filter(lambda x: x[3]==position[3],list(filter(lambda x: x[2] != "#",self.positions))))))

    def __lt__(self,estado):
        pass
        #return self.arrumador < estado.arrumador and self.local_caixas < estado.local_caixas
    
    def __eq__(self,estado):
        pass
        #return self.local_caixas == estado.local_caixas and self.arrumador == estado.arrumador
    
    def __hash__(self):
        return hash(str(self.positions))
        
    def __str__(self):
        string = ""
        for each in self.positions:
            if each[0] < len(self.size):
                string+= " " + str(each[2])
            else:
                string+= " "+ str(each[2]) +"\n"
        return string

    def from_file(self,file_name):
        with open(file_name) as fich:
            result = []
            y = 1
            for each_line in fich:
                l = each_line.strip("\n").split(" ")
                x = 1
                for each in l:
                    if x / self.block_x <= 1 and y / self.block_y <= 1:
                        result.append([x,y,each,1])
                    elif 1 < x / self.block_x <= 2 and y / self.block_y <= 1:
                        result.append([x,y,each,2])
                    elif x / self.block_x > 2 and y / self.block_y <= 1:
                        result.append([x,y,each,3])
                    elif x / self.block_x <= 1 and 1 < y / self.block_y <= 2:
                        result.append([x,y,each,4])
                    elif 1 < x / self.block_x <= 2 and 1 < y / self.block_y <= 2:
                        result.append([x,y,each,5])
                    elif x / self.block_x > 2 and 1 < y / self.block_y <= 2:
                        result.append([x,y,each,6])
                    elif x / self.block_x <= 1 and y / self.block_y > 2:
                        result.append([x,y,each,7])
                    elif 1 < x / self.block_x <= 2 and y / self.block_y > 2:
                        result.append([x,y,each,8])
                    elif x / self.block_x > 2 and y / self.block_y > 2:
                        result.append([x,y,each,9])
                    x+=1
                y+=1
            self.positions = result

