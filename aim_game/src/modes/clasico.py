"""Modo Clásico: la diana de anillos de siempre, sobre el fondo del almacén."""

import math
import random

import pygame
from src.modes.base import ModoJuego
from src.targets.rings import Diana

# La escala de MEDIO (0.75) deja la diana con su radio original (40 px).
ESCALA_REFERENCIA = 0.75
LIMITE_SUPERIOR = 75    # espacio para el HUD
LIMITE_INFERIOR = 125   # espacio para el personaje


class ModoClasico(ModoJuego):
    """Una diana a la vez; la dificultad cambia su tamaño y su velocidad."""

    nombre = "CLASICO"
    duracion = 60
    fondo = "almacen"

    def iniciar(self):
        """Reinicia la partida sin diana en pantalla."""
        super().iniciar()
        self.diana = None
        self.pos = pygame.Vector2()
        self.velocidad = pygame.Vector2()
        self.se_mueve = True

    @staticmethod
    def _puntos_por_distancia(distancia, radio):
        """Puntos según el anillo: 100 centro, 75, 50 y 25 el borde."""
        if distancia > radio:
            return 0
        if distancia <= radio * 0.25:
            return 100
        if distancia <= radio * 0.50:
            return 75
        if distancia <= radio * 0.75:
            return 50
        return 25

    def _crear_diana(self):
        """Crea una diana ajustada a la dificultad y con su movimiento."""
        diana = Diana(self.ancho, self.alto)
        escala = self.dificultad.escala / ESCALA_REFERENCIA
        if abs(escala - 1.0) > 0.01:
            diametro = max(10, round((diana.radio * 2 + 2) * escala))
            diana.imagen = pygame.transform.smoothscale(
                diana.imagen, (diametro, diametro)
            )
            diana.radio = (diametro - 2) // 2

        self._x_min = diana.radio
        self._x_max = self.ancho - diana.radio
        self._y_min = LIMITE_SUPERIOR + diana.radio
        self._y_max = self.alto - LIMITE_INFERIOR - diana.radio
        self.pos = pygame.Vector2(diana.posicion)
        self.pos.x = min(max(self.pos.x, self._x_min), self._x_max)
        self.pos.y = min(max(self.pos.y, self._y_min), self._y_max)

        angulo = random.uniform(0, 2 * math.pi)
        self.velocidad = (
            pygame.Vector2(math.cos(angulo), math.sin(angulo))
            * self.dificultad.velocidad
        )
        self.se_mueve = True
        self._colocar(diana)
        return diana

    def _colocar(self, diana):
        """Copia la posición calculada a la diana (sin romper si no se puede)."""
        try:
            diana.posicion = (round(self.pos.x), round(self.pos.y))
        except AttributeError:
            self.se_mueve = False

    def actualizar(self, dt, teclas):
        """Crea la diana si hace falta, la anima y la mueve rebotando."""
        if self.diana is None:
            self.diana = self._crear_diana()
        self.diana.actualizar(dt)
        if not self.se_mueve or self.velocidad.length_squared() == 0:
            return
        self.pos += self.velocidad * dt
        if not self._x_min <= self.pos.x <= self._x_max:
            self.velocidad.x *= -1
            self.pos.x = min(max(self.pos.x, self._x_min), self._x_max)
        if not self._y_min <= self.pos.y <= self._y_max:
            self.velocidad.y *= -1
            self.pos.y = min(max(self.pos.y, self._y_min), self._y_max)
        self._colocar(self.diana)

    def procesar_clic(self, posicion, efectos):
        """Suma los puntos del anillo impactado y genera una diana nueva."""
        if self.diana is None or not self.diana.esta_visible:
            return 0
        distancia = pygame.Vector2(self.diana.posicion).distance_to(posicion)
        puntos = self._puntos_por_distancia(distancia, self.diana.radio)
        if puntos > 0:
            self.puntos += puntos
            efectos.registrar_acierto(self.diana, posicion, puntos)
            self.diana = self._crear_diana()
        return puntos

    def dibujar(self, pantalla):
        """Dibuja la diana actual."""
        if self.diana is not None:
            self.diana.dibujar(pantalla)
