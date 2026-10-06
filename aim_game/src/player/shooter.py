"""Módulo encargado de gestionar el puntero del jugador y calcular la precisión de impacto."""

import pygame
import pygame.math as math

class Crosshair:

    """
    Representa la mira del usuario en pantalla y procesa las matemáticas de colisión.
    
    Parameters:
        sprite_imagen (Surface, opcional): Imagen personalizada para la mira.
    """

    def __init__(self, sprite_imagen = None):
        self.color = (0, 255, 0) #verde fosforescente
        self.posicion = (0, 0)
        self.sprite = sprite_imagen


    def actualizar(self):
        """Sincroniza las coordenadas lógicas de la mira con la posición del ratón."""
        #mismas coordenadas del mouse de windows
        self.posicion = pygame.mouse.get_pos()

    def dibujar(self, pantalla): #render del mouse en pantalla
        """Renderiza la mira en la superficie principal de la ventana."""
        if self.sprite:
            #centro
            self.sprite = pygame.transform.scale(self.sprite,(64,64))
            rect_sprite = self.sprite.get_rect(center=self.posicion)
            pantalla.blit(self.sprite, rect_sprite)
        else:
            x, y = self.posicion
            pygame.draw.line(pantalla, (0, 255, 0), (x -15, y), (x + 15, y), 2)
            pygame.draw.line(pantalla, (0, 255, 0), (x, y - 15), (x, y + 15), 2)
            pygame.draw.circle(pantalla, self.color, self.posicion, 10, 2)

    def disparar(self, blanco_centro, radio_maximo, posicion_clic=None):

        """
        Calcula los puntos obtenidos basándose en la distancia euclidiana al centro del objetivo.
        
        Parameters:
            blanco_centro (tuple): Coordenadas (x, y) del centro de la diana.
            radio_maximo (int): Radio total de colisión de la diana.
            posicion_clic (tuple, opcional): Coordenadas exactas donde se registró el clic.
            
        Returns:
            int: Puntos obtenidos (100, 75, 50, 25) o 0 si el disparo falló.
        """

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
