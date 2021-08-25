import random
from re import S
import time
import numpy as np
import cv2
import keyboard

class StockMarket:
    def __init__(self):
        self.current_price = 100
        self.high = 100
        self.low = 100
        self.history = []
        self.history_graph = []
        self.x = 1200
        self.y = 700
        self.graph_level = int(self.y/2)

    def update(self):
        self.high = self.current_price
        self.low = self.current_price
        self.open = self.current_price
        graph_lever = 20
        for i in range(100):
            if random.randint(0,1) == 0:
                self.current_price += 0.05
            else:
                self.current_price -= 0.05
            if self.high < self.current_price:
                self.high = self.current_price
            elif self.low > self.current_price:
                self.low = self.current_price
        self.history.append([self.open,self.current_price,self.high,self.low])
        self.history_graph.append([(self.open-100)*graph_lever,(self.current_price-100)*graph_lever,(self.high-100)*graph_lever,(self.low-100)*graph_lever])
        if len(self.history) > self.x*3/16:
            self.history.pop(0)
            self.history_graph.pop(0)
        if (self.current_price-100)*graph_lever +self.y/2 < self.graph_level +100:
            self.graph_level -= 150
        if (self.current_price-100)*graph_lever +self.y/2  > self.graph_level - 100:
            self.graph_level += 150
    def update_graph(self):
        graph = np.zeros((self.y,self.x,3))
        candle_wdith = 4
        for i in range(1,len(self.history)):
            if self.history[i][0] < self.history[i][1]:
                for l in range(int(self.history_graph[i][3]),int(self.history_graph[i][2])):
                    if self.graph_level -l > 1:
                        graph[self.graph_level-l][i*candle_wdith] = [0.2,1,0.2]
                for l in range(int(self.history_graph[i][0]),int(self.history_graph[i][1])):
                    for w in range(1,candle_wdith):
                        if self.graph_level -l > 1:
                            graph[self.graph_level-l][i*candle_wdith-2+w] = [0.2,1,0.2]
            elif self.history[i][0] > self.history[i][1]:
                for l in range(int(self.history_graph[i][3]),int(self.history_graph[i][2])):
                    if self.graph_level -l > 1:
                        graph[self.graph_level-l][i*candle_wdith] = [0.2,0.2,1]
                for l in range(int(self.history_graph[i][1]),int(self.history_graph[i][0])):
                    for w in range(1,candle_wdith):
                        if self.graph_level -l > 1:
                            graph[self.graph_level-l][i*candle_wdith-2+w] = [0.2,0.2,1]
            else:
                for l in range(int(self.history_graph[i][3]),int(self.history_graph[i][2])):
                    if self.graph_level -l > 1:
                        graph[self.graph_level-l][i*candle_wdith] = [0.2,0.2,1]
                for w in range(1,candle_wdith):
                    if self.graph_level -l > 1:
                        graph[self.graph_level-int(self.history_graph[i][1])][i*candle_wdith-2+w] = [0.2,0.2,1]
        return graph
    def update_text(self,screen):
        #open
        cv2.putText(screen,"Open : "+str(round(self.history[len(self.history)-1][0],2)),(20,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(1,1,1))
        #current
        cv2.putText(screen,"Current : "+str(round(self.history[len(self.history)-1][1],2)),(150,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(1,1,1))
        #high
        cv2.putText(screen,"High : "+str(round(self.history[len(self.history)-1][2],2)),(300,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0.2,1,0.2))
        #low
        cv2.putText(screen,"Low : "+str(round(self.history[len(self.history)-1][3],2)),(420,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0.2,0.2,1))
        return screen

def main():
    slow = 0
    market = StockMarket()
    while True:
        time.sleep(slow)
        market.update()
        graph = market.update_graph()
        graph = market.update_text(graph)
        cv2.imshow("graph",graph)
        if keyboard.is_pressed("d"):
            if slow < 2:
                slow += 0.01
        if keyboard.is_pressed("a"):
            if slow > 0.01:
                slow -= 0.01
        if cv2.waitKey(1) and keyboard.is_pressed("q"):
            break

if __name__ == "__main__":
    main()