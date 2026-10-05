import pygame
import pygame.math as math

class Crosshair:
    def __init__(self):
        self.color = (0, 255, 0) #verde fosforescente
        self.posicion = (0, 0)

    def actualizar(self):
        #mismas coordenadas del mouse de windows
        self.posicion = pygame.mouse.get_pos()

    def dibujar(self, pantalla): #render del mouse en pantalla
        pygame.draw.circle(pantalla, self.color, self.posicion, 10, 2)
        pygame.draw.line(pantalla, self.color, (self.posicion[0] - 15, self.posicion[1]), (self.posicion[0] + 15, self.posicion[1]), 2)
        pygame.draw.line(pantalla, self.color, (self.posicion[0], self.posicion[1]- 15), (self.posicion[0], self.posicion[1] + 15), 2)

    def disparar(self, blanco_centro, radio_maximo, posicion_clic=None):

        posicion = self.posicion if posicion_clic is None else posicion_clic
        vector_clic = math.Vector2(posicion)  # Coordenadas reales del evento de clic.
        vector_blanco = math.Vector2(blanco_centro)     #ubicar la posicion del blanco

        distancia = vector_clic.distance_to(vector_blanco) #calcular la distancia entre ambos usando cálculo euclidiano

        if distancia <= radio_maximo:
            if distancia <= radio_maximo * 0.25:
                return 100 #al rojo!
            elif distancia <= radio_maximo * 0.50:
                return 75 #zona intermedia
            elif distancia <= radio_maximo * 0.75:
                return 50 # zona azul :3
            else:
                return 25
        return 0 #fallaste
