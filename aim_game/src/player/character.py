"""Personaje decorativo fijo en la parte inferior de la pantalla."""

import pygame


class Personaje:
    """Carga un sprite una vez y ofrece el origen de sus proyectiles."""

    def __init__(self, ancho, alto, ruta_imagen, alto_sprite=135):
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        limites = imagen.get_bounding_rect(min_alpha=128)
        if limites.width == 0 or limites.height == 0:
            raise ValueError("La imagen del personaje está completamente vacía.")
        imagen = imagen.subsurface(limites).copy()
        ancho_sprite = max(
            1, round(imagen.get_width() * alto_sprite / imagen.get_height())
        )
        self.imagen = pygame.transform.scale(imagen, (ancho_sprite, alto_sprite))
        self.rect = self.imagen.get_rect(midbottom=(ancho // 2, alto - 10))
        self.tiempo_destello = 0.0

    @property
    def origen_disparo(self):
        """Punto fijo del lanzador, cerca del extremo superior del sprite."""
        return self.rect.centerx, self.rect.top + 4

    def disparar(self):
        self.tiempo_destello = 0.06

    def actualizar(self, dt):
        self.tiempo_destello = max(0.0, self.tiempo_destello - dt)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
        if self.tiempo_destello > 0:
            pygame.draw.circle(pantalla, (55, 220, 255), self.origen_disparo, 6)
            pygame.draw.circle(pantalla, (240, 255, 255), self.origen_disparo, 3)
