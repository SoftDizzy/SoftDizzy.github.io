from setting import *  
from sys import exit  
import threading  # 目前沒使用，但原本多人連線用
import json  

from game import Game  
from score import Score  
from preview import Preview  
from time import sleep  
from random import choice 
import pygame 
class Main:
    def __init__(self):
        
        pygame.init()
        self.Dispay_Surface = pygame.display.set_mode((Window_Width, Window_Height))  
        self.clock = pygame.time.Clock()  
        pygame.display.set_caption("Tetris")  

       
        self.next_shapes = [choice(list(Tetorminos.keys())) for shape in range(3)]

        
        self.game = Game(self.get_next_shape, self.update_score)  
        self.game.Start = True  # 強制單機模式直接開始遊戲 這邊是我當時著重改的點 因原本的版本是兩個人連線後才能進入遊戲
        self.score = Score() 
        self.preview = Preview()  

    def update_score(self, lines, score, level):
        
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(Tetorminos.keys())))
        return next_shape

    def main_run(self):
        
        self.Pause = False  
        self.Dispay_Surface.fill(Gray)  

        while True:
            # 等待玩家開始遊戲的階段（通常用於 multiplayer 現在已繞過）
            while not self.game.Start:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                self.Dispay_Surface.fill(Gray)
                self.game.GameStart()  
                pygame.display.update()
                self.clock.tick(60)

            
            while not self.Pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

               
                self.Dispay_Surface.fill(Gray)
                self.game.run()  
                self.game.draw_grid()  
                self.score.run()  
                self.preview.run(self.next_shapes)  
                self.game.level_up()  

                pygame.display.update()  
                self.clock.tick(60)  
                # 如果遊戲結束，進入暫停階段
                if self.game.gameover:
                    self.Pause = True
                    print("press 'Q' to exit the game")

                # 按 P 可暫停
                opkey = pygame.key.get_pressed()
                if opkey[pygame.K_p]:
                    self.Pause = True
                    print(self.Pause)

            # 遊戲暫停中，等待玩家恢復（按 O）
            while self.Pause and not self.game.gameover:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                opkey = pygame.key.get_pressed()
                if opkey[pygame.K_o]:
                    self.Pause = False
                    print(self.Pause)

            # 遊戲結束後等待玩家退出（按 Q）
            while self.game.gameover:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                opkey = pygame.key.get_pressed()
                if opkey[pygame.K_q]:
                    print("END!")
                    pygame.quit()
                    exit()
                self.Dispay_Surface.fill(Gray)
                self.game.GameStart()
                pygame.display.update()
                self.clock.tick(60)

if __name__ == "__main__":
    main = Main()
    main.main_run()  # 執行主程式
   