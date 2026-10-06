"""Dianas con cuatro zonas y transiciones de aparición y salida."""

import random

import pygame


class Diana:
    """Mantiene el radio de colisión fijo mientras cambia su transparencia."""

    DURACION_ENTRADA = 0.14
    DURACION_SALIDA = 0.18

    def __init__(self, ancho_pantalla, alto_pantalla, sprite_centro=None):
        self.radio = 40
        self.ancho = ancho_pantalla

        #area exclusivamente para aparición de dianas
        self.limite_techo = 180 # justo debajo de las luces del bg
        self.limite_suelo = 450 # por encima de la linea de peligro
        self.limite_izquierdo = 100 # guardado para los rebotes
        self.limite_derecho = ancho_pantalla - 100 # desde el extremo de la pantalla 800 - 100

        #que las dianas aparezcan en la nueva posición
        self.x = random.randint(self.limite_izquierdo + self.radio, self.limite_derecho - self.radio)
        self.y = random.randint(self.limite_techo + self.radio, self.limite_suelo - self.radio)

        #asignar posicion
        self.posicion = (self.x, self.y)

        self.sprite = sprite_centro
        if self.sprite:
            radio_centro = int(self.radio * 0.84)
            self.sprite = pygame.transform.scale(self.sprite, (radio_centro * 2, radio_centro * 2))

        #velocidades iniciales
        self.vel_x = random.choice([-5, -4, 4, 5])
        self.vel_y = random.choice([-5, -4, 4, 5])

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

        self.x += self.vel_x
        self.y += self.vel_y

        #rebote horizontal con reubicación forzada
        if self.x - self.radio <= 0:
            self.x = self.radio #reposicionar al ras de la pared izquierda
            self.vel_x *= -1
        elif self.x + self.radio >= self.ancho:
            self.x = self.ancho - self.radio # reposicionar al ras de la pared derecha
            self.vel_x *= -1

        #rebote vertical
        if self.y - self.radio <= self.limite_techo:
            self.y = self.limite_techo + self.radio #reposicionar justo en el techo
            self.vel_y *= -1
        elif self.y + self.radio >= self.limite_suelo:
            self.y = self.limite_suelo - self.radio #reposicionar justo en el suelo
            self.vel_y *= -1

        #sincronizar posicion nueva
        self.posicion = (self.x, self.y)

    def dibujar(self, pantalla):
        self.imagen.set_alpha(self.opacidad)
        pantalla.blit(self.imagen, self.imagen.get_rect(center=self.posicion))
