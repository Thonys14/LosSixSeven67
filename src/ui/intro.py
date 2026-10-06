"""Intro animada provisional, reemplazable por la cinemática del equipo."""

import math

import pygame


class IntroPartida:
    """Presenta al robot y una cuenta atrás antes de empezar el temporizador."""

    DURACION = 10.2

    def __init__(self, tamano, imagen_personaje, fuente_titulo, fuente_texto):
        self.ancho, self.alto = tamano
        self.fuente_titulo = fuente_titulo
        self.fuente_texto = fuente_texto
        self.edad = 0.0
        self.lienzo = pygame.Surface(tamano).convert()
        alto_sprite = 160
        ancho_sprite = round(
            imagen_personaje.get_width() * alto_sprite / imagen_personaje.get_height()
        )
        self.personaje = pygame.transform.scale(
            imagen_personaje, (ancho_sprite, alto_sprite)
        )

    @property
    def terminada(self):
        return self.edad >= self.DURACION

    def reiniciar(self):
        """Reproduce la introducción desde el comienzo en cada nueva partida."""
        self.edad = 0.0

    def actualizar(self, dt):
        self.edad += dt

    def dibujar(self, pantalla):
        fondo = (10, 18, 32)
        self.lienzo.fill(fondo)
        panel = pygame.Rect(40, 60, self.ancho - 80, self.alto - 120)
        pygame.draw.rect(self.lienzo, (50, 100, 150), panel, width=2)
        titulo = self.fuente_titulo.render(
            "SISTEMA DE ENTRENAMIENTO", True, (220, 240, 255)
        )
        self.lienzo.blit(
            titulo, titulo.get_rect(center=(self.ancho // 2, 110))
        )

        movimiento = round(math.sin(self.edad * 4) * 3)
        rect_robot = self.personaje.get_rect(
            center=(self.ancho // 2, self.alto // 2 - 45 + movimiento)
        )
        self.lienzo.blit(self.personaje, rect_robot)

        texto = self.fuente_texto.render(
            "Preparando objetivos...", True, (120, 200, 235)
        )
        self.lienzo.blit(texto, texto.get_rect(center=(self.ancho // 2, 355)))
        numero = max(1, 10 - int(self.edad))
        cuenta = self.fuente_titulo.render(str(numero), True, (55, 220, 255))
        cuenta = pygame.transform.scale(
            cuenta, (cuenta.get_width() * 2, cuenta.get_height() * 2)
        )
        self.lienzo.blit(cuenta, cuenta.get_rect(center=(self.ancho // 2, 420)))
        ayuda = self.fuente_texto.render(
            "ESPACIO: omitir introducción", True, (150, 175, 195)
        )
        self.lienzo.blit(ayuda, ayuda.get_rect(center=(self.ancho // 2, 505)))

        entrada = min(1.0, self.edad / 0.25)
        salida = min(1.0, max(0.0, (self.DURACION - self.edad) / 0.25))
        self.lienzo.set_alpha(round(255 * min(entrada, salida)))
        pantalla.fill(fondo)
        pantalla.blit(self.lienzo, (0, 0))
