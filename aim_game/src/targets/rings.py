import pygame
import random

class Diana:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.radio = 40 #tamaño meh

        #centro generado con random
        x = random.randint(self.radio, ancho_pantalla - self.radio)
        y = random.randint(self.radio, alto_pantalla - self.radio)
        self.posicion = (x,y)

    def dibujar(self, pantalla):
        #render de los placeholders de las dianas y de prueba
        pygame.draw.circle(pantalla, (255, 255, 255), self.posicion, self.radio) #25 pts
        pygame.draw.circle(pantalla, (50, 150, 255), self.posicion, int(self.radio * 0.75)) #50 pts
        pygame.draw.circle(pantalla, (255, 150, 0), self.posicion, int(self.radio * 0.50)) #75 pts
        pygame.draw.circle(pantalla, (200, 40, 40), self.posicion, int(self.radio * 0.25)) #al rojo!