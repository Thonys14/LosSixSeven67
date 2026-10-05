"""Dianas con cuatro zonas y transiciones de aparición y salida."""

import random

import pygame


class Diana:
    """Mantiene el radio de colisión fijo mientras cambia su transparencia."""

    DURACION_ENTRADA = 0.14
    DURACION_SALIDA = 0.18

    def __init__(self, ancho_pantalla, alto_pantalla):
        self.radio = 40
        # Espacio para el HUD superior y el personaje inferior.
        x = random.randint(self.radio, ancho_pantalla - self.radio)
        y = random.randint(75 + self.radio, alto_pantalla - 125 - self.radio)
        self.posicion = (x, y)
        self.edad = 0.0
        self.tiempo_salida = None
        self.opacidad_salida = 255

        diametro = self.radio * 2 + 2
        self.imagen = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
        centro = (self.radio + 1, self.radio + 1)
        for proporcion, color in (
            (1.00, (255, 255, 255)),
            (0.75, (50, 150, 255)),
            (0.50, (255, 150, 0)),
            (0.25, (200, 40, 40)),
        ):
            pygame.draw.circle(
                self.imagen, color, centro, int(self.radio * proporcion)
            )

    @property
    def esta_visible(self):
        """Una diana recién creada debe dibujarse antes de aceptar impactos."""
        return self.edad > 0 and self.tiempo_salida is None

    @property
    def terminado(self):
        return (
            self.tiempo_salida is not None
            and self.tiempo_salida >= self.DURACION_SALIDA
        )

    @property
    def opacidad(self):
        if self.tiempo_salida is not None:
            avance = min(1.0, self.tiempo_salida / self.DURACION_SALIDA)
            return round(self.opacidad_salida * (1 - avance))
        avance = min(1.0, self.edad / self.DURACION_ENTRADA)
        return round(255 * avance)

    def iniciar_salida(self):
        """Conserva su opacidad actual para que el desvanecimiento sea continuo."""
        self.opacidad_salida = self.opacidad
        self.tiempo_salida = 0.0

    def actualizar(self, dt):
        if self.tiempo_salida is None:
            self.edad += dt
        else:
            self.tiempo_salida += dt

    def dibujar(self, pantalla):
        self.imagen.set_alpha(self.opacidad)
        pantalla.blit(self.imagen, self.imagen.get_rect(center=self.posicion))
