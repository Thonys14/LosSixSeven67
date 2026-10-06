"""Nave objetivo con sprite y zonas de puntuación (núcleo, cabina, alas, propulsores)."""

import math
import os
import random

import pygame

RUTA_SPRITE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "assets", "gfx", "nave.png",
)

# Tamaño del sprite original (nave.png) y ancho base en pantalla.
ANCHO_SPRITE = 657
ALTO_SPRITE = 512
ANCHO_BASE = 170

# Zonas en coordenadas del sprite original, de menor a mayor valor:
# (puntos, color_de_respaldo, forma, datos). Lo último queda encima.
ZONAS = (
    (5, (255, 150, 0), "rect", (178, 335, 70, 165)),
    (5, (255, 150, 0), "rect", (408, 335, 70, 165)),
    (10, (60, 200, 90), "poly",
     ((0, 330), (172, 198), (172, 372), (40, 372))),
    (10, (60, 200, 90), "poly",
     ((657, 330), (485, 198), (485, 372), (617, 372))),
    (25, (60, 150, 255), "ellipse", (289, 40, 76, 104)),
    (50, (220, 40, 40), "circle", ((325, 278), 42)),
)

_sprite_cache = None


def _cargar_sprite():
    """Carga nave.png una sola vez; si falta, crea un sprite de respaldo.

    Returns:
        Superficie con transparencia de ANCHO_SPRITE x ALTO_SPRITE.
    """
    global _sprite_cache
    if _sprite_cache is not None:
        return _sprite_cache
    try:
        sprite = pygame.image.load(RUTA_SPRITE).convert_alpha()
    except (FileNotFoundError, pygame.error):
        print("Advertencia: no se encontró assets/gfx/nave.png, "
              "se usa una nave de respaldo.")
        sprite = pygame.Surface((ANCHO_SPRITE, ALTO_SPRITE), pygame.SRCALPHA)
        pygame.draw.rect(sprite, (150, 160, 175), (240, 120, 177, 330))
        for _, color, forma, datos in ZONAS:
            _dibujar_zona(sprite, color, forma, datos, 1.0)
    _sprite_cache = sprite
    return sprite


def _dibujar_zona(superficie, color, forma, datos, escala):
    """Dibuja una zona sobre una superficie aplicando la escala dada."""
    if forma in ("rect", "ellipse"):
        x, y, ancho, alto = (round(valor * escala) for valor in datos)
        rect = (x, y, max(1, ancho), max(1, alto))
        if forma == "rect":
            pygame.draw.rect(superficie, color, rect)
        else:
            pygame.draw.ellipse(superficie, color, rect)
    elif forma == "poly":
        puntos = [(round(x * escala), round(y * escala)) for x, y in datos]
        pygame.draw.polygon(superficie, color, puntos)
    else:
        (cx, cy), radio = datos
        pygame.draw.circle(
            superficie,
            color,
            (round(cx * escala), round(cy * escala)),
            max(1, round(radio * escala)),
        )


class Nave:
    """Objetivo que se mueve y da puntos según la zona donde se impacte.

    Es compatible con la interfaz de ``Diana`` (posicion, radio,
    esta_visible, terminado, iniciar_salida, actualizar y dibujar).
    """

    DURACION_ENTRADA = 0.14
    DURACION_SALIDA = 0.18
    LIMITE_SUPERIOR = 75   # espacio para el HUD
    LIMITE_INFERIOR = 125  # espacio para el personaje

    def __init__(self, ancho_pantalla, alto_pantalla, dificultad):
        """Crea una nave en posición aleatoria.

        Args:
            ancho_pantalla: ancho de la ventana en píxeles.
            alto_pantalla: alto de la ventana en píxeles.
            dificultad: objeto ``Dificultad`` con escala y velocidad.
        """
        ancho = max(8, round(ANCHO_BASE * dificultad.escala))
        factor = ancho / ANCHO_SPRITE
        alto = max(8, round(ALTO_SPRITE * factor))
        self.radio = ancho // 2
        self.edad = 0.0
        self.tiempo_salida = None
        self.opacidad_salida = 255

        self.imagen = pygame.transform.smoothscale(
            _cargar_sprite(), (ancho, alto)
        )
        # El canal rojo de cada píxel guarda los puntos de esa zona.
        self.mapa_zonas = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        for puntos, _, forma, datos in ZONAS:
            _dibujar_zona(
                self.mapa_zonas, (puntos, 0, 0, 255), forma, datos, factor
            )

        self._x_min = ancho / 2
        self._x_max = ancho_pantalla - ancho / 2
        self._y_min = self.LIMITE_SUPERIOR + alto / 2
        self._y_max = alto_pantalla - self.LIMITE_INFERIOR - alto / 2
        self.pos = pygame.Vector2(
            random.uniform(self._x_min, self._x_max),
            random.uniform(self._y_min, self._y_max),
        )
        angulo = random.uniform(0, 2 * math.pi)
        self.velocidad = (
            pygame.Vector2(math.cos(angulo), math.sin(angulo))
            * dificultad.velocidad
        )

    @property
    def posicion(self):
        """Centro de la nave como tupla de enteros."""
        return (round(self.pos.x), round(self.pos.y))

    @property
    def esta_visible(self):
        """Una nave recién creada se dibuja antes de aceptar impactos."""
        return self.edad > 0 and self.tiempo_salida is None

    @property
    def terminado(self):
        """True cuando terminó la animación de salida."""
        return (
            self.tiempo_salida is not None
            and self.tiempo_salida >= self.DURACION_SALIDA
        )

    @property
    def opacidad(self):
        """Opacidad actual (0-255) según entrada o salida."""
        if self.tiempo_salida is not None:
            avance = min(1.0, self.tiempo_salida / self.DURACION_SALIDA)
            return round(self.opacidad_salida * (1 - avance))
        avance = min(1.0, self.edad / self.DURACION_ENTRADA)
        return round(255 * avance)

    def iniciar_salida(self):
        """Inicia el desvanecimiento conservando la opacidad actual."""
        self.opacidad_salida = self.opacidad
        self.tiempo_salida = 0.0

    def puntuar(self, posicion_clic):
        """Devuelve los puntos de un clic: 50, 25, 10, 5 o 0.

        El cuerpo gris de la nave y los clics fuera de ella dan 0 puntos.
        """
        if not self.esta_visible:
            return 0
        rect = self.imagen.get_rect(center=self.posicion)
        if not rect.collidepoint(posicion_clic):
            return 0
        x = posicion_clic[0] - rect.x
        y = posicion_clic[1] - rect.y
        if self.imagen.get_at((x, y)).a < 40:
            return 0  # píxel transparente: fuera de la silueta
        return self.mapa_zonas.get_at((x, y)).r

    def actualizar(self, dt):
        """Avanza el tiempo y mueve la nave, rebotando en los bordes."""
        if self.tiempo_salida is not None:
            self.tiempo_salida += dt
            return
        self.edad += dt
        self.pos += self.velocidad * dt
        if not self._x_min <= self.pos.x <= self._x_max:
            self.velocidad.x *= -1
            self.pos.x = min(max(self.pos.x, self._x_min), self._x_max)
        if not self._y_min <= self.pos.y <= self._y_max:
            self.velocidad.y *= -1
            self.pos.y = min(max(self.pos.y, self._y_min), self._y_max)

    def dibujar(self, pantalla):
        """Dibuja la nave con su opacidad actual."""
        self.imagen.set_alpha(self.opacidad)  
        pantalla.blit(self.imagen, self.imagen.get_rect(center=self.posicion))