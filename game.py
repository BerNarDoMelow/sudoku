from estado import Estado
from search import *
import math, random
import time
from copy import deepcopy
import random

class Game(Problem):
    def __init__(self,inicial,goal = None):
        super().__init__(inicial)
        self.goal = goal
        self.nos_expandidos = 0


    def actions3(self,estado):
        actions = []
        total_positions = len(list(filter(lambda x: x[2] == "#",estado.positions)))
        print("total positions: " + str(total_positions))
        for position in list(filter(lambda x: x[2] == "#",estado.positions)):
            print("position: " + str(position[:2]))
            values = {}
            info = []
            percept = estado.percept((position[0],position[1],position[3]))
            #print(percept)
            for some in list(percept.values()):
                for l in some:
                    try:
                        info.append(int(l))
                    except ValueError:
                        pass
            #print("meu perception: ")
            #print(info)
            values_in_group = list(map(lambda x: int(x[2]),filter(lambda x: x[3]==position[3],list(filter(lambda x: x[2] != "#",estado.positions)))))
            ##POR CADA POSICAO DO MESMO GRUPO
            print(list(filter(lambda x: x[2] == "#",estado.positions)))
            grupo_n = list(filter(lambda x: x[3]==position[3],list(filter(lambda x: x[2] == "#",estado.positions))))
            grupo_s = list(filter(lambda x: x[3]==position[3],list(filter(lambda x: x[2] != "#",estado.positions))))
            print("grupo_n")
            print(grupo_n)
            if len(grupo_n) == 1:
                print("numero que falta é: ")
                print(int(sum(estado.size))-int(sum(list(map(lambda x:int(x[2]),grupo_s)))))
                actions.append([position[0],position[1],int(sum(estado.size))-int(sum(list(map(lambda x:int(x[2]),grupo_s)))),position[3]])
            n_options = len(list(filter(lambda x: x[3]==position[3],list(filter(lambda x: x[2] == "#",estado.positions)))))
            for other_position in grupo_n:
                other_percept = estado.percept((other_position[0],other_position[1],other_position[3]))
                other_values = []
                ##POR TODOS OS VALORES DO PERCEPT DUMA POSICAO (DO GRUPO)
                ##E apenas um filtro
                for other_some in list(other_percept.values()):
                    for other_l in other_some:
                        try:
                            other_values.append(int(other_l))
                        except ValueError:
                           pass

                for each in list(set(other_values)):
                    try:
                        values[each] += 1
                    except KeyError:
                        values[each] = 1
            #print(values)
            for each_value in values:
                if values[each_value] == n_options - 1 and each_value not in info:
                    actions.append([position[0],position[1],each_value,position[3]])
        return actions
    
    
    def actions(self,estado):
        actions = []
        total_positions = len(list(filter(lambda x: x[2] == "#",estado.positions)))
        print("total positions: " + str(total_positions))
        for position in list(filter(lambda x: x[2] == "#",estado.positions)):
            perception = estado.filter_perception((position[0],position[1],position[3]))
            group = estado.group(position)
            options = deepcopy(estado.size)
            actions_local = self.actions_on_location(perception,group,options)
            if actions_local is not None:
                actions.append([position[0],position[1],str(actions_local),position[3]])
            #print("actions no grupo: " + str(position[3]))
            actions_grupo = list(filter(lambda x:x not in group+perception,self.actions_on_group(estado,position)))
            #print(actions_grupo)
            if len(actions_grupo) == 1:
                actions.append([position[0],position[1],actions_grupo[0],position[3]])
        return actions



    def actions_on_location(self,perception,group,options):
        actions = []
        for each in options:
            if each not in list(set(perception+group)):
                actions.append(each)
        if len(actions) == 1:
            return actions[0]
        return None


    def actions_on_group(self,estado,position):
        values = {}
        positions_left = estado.positions_left_in_group(position)
        #print("position: ")
        #print(position[:2])
        for each_position in estado.filter_map(position):
            perception = estado.percept(each_position)
            other_values = []
            for other_some in list(perception.values()):
                for other_l in other_some:
                    try:
                        other_values.append(int(other_l))
                    except ValueError:
                        pass
            #print(other_values)
            for each in list(set(other_values)):
                try:
                    values[each] += 1
                except KeyError:
                    values[each] = 1
        #print(values)
        #print("posicoes que faltam: " + str(positions_left))
        options=[]
        for some in values:
            if values[some] == positions_left - 1:
                options.append(some)
        return options


    def result(self,state,action):
        state_n = deepcopy(state)
        index_position = [action[0],action[1],'#',action[3]]
        state_n.positions[state.positions.index(index_position)] = action
        estado = Estado(len(state_n.size),state_n.block_x,state_n.block_y,state_n.positions)
        return Estado(len(state_n.size),state_n.block_x,state_n.block_y,state_n.positions)



    def goal_test(self,estado):
        """

        :param estado:
        :return:
        """
        for x in estado.positions:
            if x[2] == "#":
                return False
        return True

    def equals(self,caixa,alvo):
        pass
        #return caixa.width == alvo.width and caixa.height == alvo.height

    def path_cost(self,c,state1,action,state2):
        pass
        #return 1 if "empurra" in action else 2

    def h1(self,no):
        pass
        #valor_h = 0
        #for each_caixa in no.state.local_caixas:
        #    lista = []
        #    dist_alvo = 0
        #    for each_alvo in no.state.local_alvos:
        #        nova_dist_alvo = math.sqrt((each_caixa.width-each_alvo.width)**2 + (each_caixa.height-each_alvo.height)**2)
        #        lista.append(nova_dist_alvo)
        #    valor_h += min(lista)
        #return valor_h
            


    def h2(self,no):
        """
        Esta heuristica desvaloriza por cada caixa que esta no canto
        """
        pass
        #valor_h = 0
        #for each in no.state.local_caixas:
        #    if no.state.in_corner(each):
        #        valor_h+=1
        #return valor_h


    def h3(self,no):
        """
        Valoriza o que tiver menor distancia entre o arrumador e a primeira caixa que esta state.local_caixas
        """
        pass
        #caixas = no.state.local_caixas
        #lista = []
        #arrumador = no.state.arrumador
        #for caixa in caixas:
        #    lista.append(math.sqrt((caixa.width-arrumador.width)**2 + (caixa.height-arrumador.height)**2))
        #return min(lista)


#############################



#######A ir buscar ao ficheiro
estado = Estado(9,3,3)
estado.from_file("examples/example5.txt")
print(estado.positions)
print(estado)

game = Game(estado)
#game.actions3(estado)
#print(game.actions(estado))
#estado2 = game.result(estado,[3,8,'3',7])
#print(estado2)
#print(estado2.positions)
#print(list(filter(lambda x: x[2] == "#",estado2.positions)))
#print("actions: ")
#print(game.actions(estado2))
#estado3 = game.result(estado2,[6,1,1,2])
#print(estado3)
##1 / 4
#print("Comecei")
print(depth_first_tree_search(game))
#res = depth_first_tree_search(game)
#print(res)
#res = depth_first_graph_search(game)
#res = uniform_cost_search(game)
#res = iterative_deepening_search(game)
#res = depth_limited_search(game,10)
#res = best_first_graph_search(game,game.h2)
#res = best_first_graph_search(game,game.h3)
#res = astar_search(game,game.h3)
#Para correr tem descomentar o algoritmo que quer



##NOTAS:
##O PERCEPT SECALHAR N DEVIA SER COM DICIONARIO
##USAR RANDOM.CHOICES
