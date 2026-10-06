"""Modo Destrucción de Núcleo (Ataque Final): jefe que dispara al jugador."""

import math

import pygame
from src.effects.feedback import COLORES_PUNTOS, Impacto, TextoFlotante
from src.modes.base import ModoJuego

# Parámetros por dificultad:
#   vida_jefe: impactos al núcleo para destruirlo
#   radio_nucleo: tamaño del punto débil
#   intervalo: segundos entre ráfagas del jefe
#   vel_bala: velocidad de los disparos (px/s)
#   abanico: balas por ráfaga
#   abierto / cerrado: segundos con el escudo abierto / cerrado
#   vida_jugador: golpes que aguanta el jugador
#   omega: rapidez del movimiento lateral del jefe
CONFIG = {
    "FACIL": {"vida_jefe":12, "radio_nucleo":24, "intervalo":1.5,
                  "vel_bala":190.0, "abanico":1, "abierto":2.0, "cerrado":1.2,
                  "vida_jugador":5, "omega":0.6},
    "MEDIO": {"vida_jefe":18, "radio_nucleo":18, "intervalo":1.1,
                  "vel_bala":250.0, "abanico":1, "abierto":1.5, "cerrado":1.6,
                  "vida_jugador":4, "omega":0.9},
    "DIFICIL": {"vida_jefe":25, "radio_nucleo":14, "intervalo":0.8,
                    "vel_bala":310.0, "abanico":3, "abierto":1.1, "cerrado":2.0,
                    "vida_jugador":3, "omega":1.2},
}


class ModoNucleo(ModoJuego):
    """Esquiva con A/D (y W/S) y destruye el núcleo cuando el escudo abre."""

    nombre = "NUCLEO"
    duracion = 90
    dibuja_personaje = False

    VELOCIDAD_JUGADOR = 320.0
    PUNTOS_NUCLEO = 50
    BONO_JEFE = 200
    RADIO_JEFE = 118
    CENTRO_Y = 195
    AMPLITUD = 190
    TOLERANCIA = 6

    def iniciar(self):
        """Reinicia al jefe, al jugador y las balas."""
        super().iniciar()
        self.cfg = CONFIG.get(self.dificultad.nombre, CONFIG["MEDIO"])
        self.vida_jefe_max = self.cfg["vida_jefe"]
        self.vida_jefe = self.vida_jefe_max
        self.vida_jugador = self.cfg["vida_jugador"]
        self.tiempo = 0.0
        self.espera_disparo = 1.2
        self.invulnerable = 0.0
        self.destello_escudo = 0.0
        self.balas = []  # cada bala: [posicion, velocidad]
        self.jugador = pygame.Vector2(self.ancho / 2, self.alto - 60)
        self.sprite = self._preparar_sprite()

    def _preparar_sprite(self):
        """Escala la imagen del jugador; devuelve None si no se puede."""
        if self.imagen_jugador is None:
            return None
        try:
            alto = 84
            ancho = max(
                1,
                round(
                    self.imagen_jugador.get_width() * alto
                    / self.imagen_jugador.get_height()
                ),
            )
            return pygame.transform.smoothscale(
                self.imagen_jugador, (ancho, alto)
            )
        except (pygame.error, ValueError, ZeroDivisionError):
            return None

    @property
    def centro_jefe(self):
        """Posición actual del núcleo (el jefe se mueve de lado a lado)."""
        x = self.ancho / 2 + self.AMPLITUD * math.sin(
            self.tiempo * self.cfg["omega"]
        )
        return (x, self.CENTRO_Y)

    @property
    def escudo_abierto(self):
        """True durante la ventana en que el núcleo recibe daño."""
        ciclo = self.cfg["abierto"] + self.cfg["cerrado"]
        return (self.tiempo % ciclo) >= self.cfg["cerrado"]

    @property
    def hitbox(self):
        """Zona del jugador que puede ser golpeada por las balas."""
        caja = pygame.Rect(0, 0, 34, 52)
        caja.center = (round(self.jugador.x), round(self.jugador.y))
        return caja

    def origen_disparo(self, personaje):
        """Los disparos salen de la parte superior del jugador."""
        return (self.jugador.x, self.jugador.y - 40)

    def actualizar(self, dt, teclas):
        """Mueve al jugador, al jefe y las balas."""
        if self.terminado:
            return
        self.tiempo += dt
        self.invulnerable = max(0.0, self.invulnerable - dt)
        self.destello_escudo = max(0.0, self.destello_escudo - dt)
        self._mover_jugador(dt, teclas)
        self._disparar_jefe(dt)
        self._mover_balas(dt)

    def _mover_jugador(self, dt, teclas):
        """Mueve al jugador con WASD o las flechas dentro de su zona."""
        direccion = pygame.Vector2(
            (teclas[pygame.K_d] or teclas[pygame.K_RIGHT])
            - (teclas[pygame.K_a] or teclas[pygame.K_LEFT]),
            (teclas[pygame.K_s] or teclas[pygame.K_DOWN])
            - (teclas[pygame.K_w] or teclas[pygame.K_UP]),
        )
        if direccion.length_squared() > 0:
            self.jugador += direccion.normalize() * self.VELOCIDAD_JUGADOR * dt
        self.jugador.x = min(max(self.jugador.x, 30), self.ancho - 30)
        self.jugador.y = min(max(self.jugador.y, self.alto - 210), self.alto - 45)

    def _disparar_jefe(self, dt):
        """El jefe lanza una ráfaga apuntada al jugador cada cierto tiempo."""
        self.espera_disparo -= dt
        if self.espera_disparo > 0:
            return
        self.espera_disparo = self.cfg["intervalo"]
        origen = pygame.Vector2(self.centro_jefe)
        hacia_jugador = self.jugador - origen
        angulo_base = math.atan2(hacia_jugador.y, hacia_jugador.x)
        cantidad = self.cfg["abanico"]
        for i in range(cantidad):
            desvio = (i - (cantidad - 1) / 2) * math.radians(16)
            angulo = angulo_base + desvio
            velocidad = pygame.Vector2(math.cos(angulo), math.sin(angulo))
            self.balas.append([origen.copy(), velocidad * self.cfg["vel_bala"]])

    def _mover_balas(self, dt):
        """Avanza las balas, retira las que salen y aplica el daño."""
        vivas = []
        caja = self.hitbox.inflate(10, 10)
        for bala in self.balas:
            bala[0] += bala[1] * dt
            x, y = bala[0]
            if not (-20 <= x <= self.ancho + 20 and -20 <= y <= self.alto + 20):
                continue
            if self.invulnerable <= 0 and caja.collidepoint(x, y):
                self.vida_jugador -= 1
                self.invulnerable = 1.0
                if self.vida_jugador <= 0:
                    self.terminado = True
                    self.mensaje_final = "Tu nave fue destruida"
                continue
            vivas.append(bala)
        self.balas = vivas

    def _mostrar_acierto(self, efectos, posicion, puntos):
        """Muestra destello y texto flotante sin necesitar una ``Nave``."""
        color = COLORES_PUNTOS.get(puntos, (255, 255, 255))
        efectos.impactos.append(Impacto(posicion, color))
        efectos.textos.append(TextoFlotante(posicion, puntos, efectos.fuente))

    def procesar_clic(self, posicion, efectos):
        """Daña al jefe solo si se acierta al núcleo con el escudo abierto."""
        if self.terminado:
            return 0
        centro = pygame.Vector2(self.centro_jefe)
        if centro.distance_to(posicion) > self.cfg["radio_nucleo"] + self.TOLERANCIA:
            return 0
        if not self.escudo_abierto:
            self.destello_escudo = 0.25  # el escudo bloqueó el disparo
            return 0
        self.vida_jefe -= 1
        self.puntos += self.PUNTOS_NUCLEO
        self._mostrar_acierto(efectos, posicion, self.PUNTOS_NUCLEO)
        if self.vida_jefe <= 0:
            self.puntos += self.BONO_JEFE
            self.terminado = True
            self.mensaje_final = "¡Núcleo destruido!"
        return self.PUNTOS_NUCLEO

    def _dibujar_jefe(self, pantalla):
        """Dibuja la estación: casco, placas giratorias y núcleo."""
        cx, cy = (round(valor) for valor in self.centro_jefe)
        radio = self.cfg["radio_nucleo"]
        pygame.draw.circle(pantalla, (45, 55, 75), (cx, cy), self.RADIO_JEFE)
        pygame.draw.circle(pantalla, (95, 110, 135), (cx, cy), self.RADIO_JEFE, 4)
        for i in range(8):
            angulo = self.tiempo * 0.8 + i * math.tau / 8
            interior = (cx + math.cos(angulo) * 62, cy + math.sin(angulo) * 62)
            exterior = (cx + math.cos(angulo) * 108, cy + math.sin(angulo) * 108)
            pygame.draw.line(pantalla, (120, 135, 160), interior, exterior, 10)
        pygame.draw.circle(pantalla, (28, 35, 52), (cx, cy), radio + 14)
        pygame.draw.circle(pantalla, (90, 105, 130), (cx, cy), radio + 14, 3)
        if self.escudo_abierto:
            pulso = 3 + round(2 * math.sin(self.tiempo * 10))
            pygame.draw.circle(pantalla, (255, 60, 60), (cx, cy), radio)
            pygame.draw.circle(pantalla, (255, 200, 200), (cx, cy), max(2, pulso))
        else:
            pygame.draw.circle(pantalla, (110, 40, 50), (cx, cy), radio)
            grosor = 5 if self.destello_escudo > 0 else 3
            pygame.draw.circle(
                pantalla, (80, 200, 255), (cx, cy), radio + 8, grosor
            )

    def _dibujar_jugador(self, pantalla):
        """Dibuja al jugador; parpadea mientras es invulnerable."""
        if self.invulnerable > 0 and int(self.invulnerable * 10) % 2 == 0:
            return
        x, y = round(self.jugador.x), round(self.jugador.y)
        if self.sprite is not None:
            pantalla.blit(self.sprite, self.sprite.get_rect(center=(x, y)))
        else:
            puntos = [(x, y - 30), (x - 22, y + 26), (x + 22, y + 26)]
            pygame.draw.polygon(pantalla, (120, 200, 255), puntos)

    def dibujar(self, pantalla):
        """Dibuja jefe, balas, jugador y barras de vida."""
        self._dibujar_jefe(pantalla)
        for posicion, _ in self.balas:
            centro = (round(posicion.x), round(posicion.y))
            pygame.draw.circle(pantalla, (255, 140, 40), centro, 7)
            pygame.draw.circle(pantalla, (255, 245, 200), centro, 3)
        self._dibujar_jugador(pantalla)

        # barra de vida del jefe
        ancho_barra = 320
        barra = pygame.Rect(self.ancho // 2 - ancho_barra // 2, 56, ancho_barra, 10)
        relleno = barra.copy()
        relleno.width = round(ancho_barra * max(0, self.vida_jefe) / self.vida_jefe_max)
        pygame.draw.rect(pantalla, (60, 20, 25), barra)
        pygame.draw.rect(pantalla, (230, 60, 60), relleno)
        pygame.draw.rect(pantalla, (255, 255, 255), barra, 2)

        # vidas del jugador
        self.dibujar_texto(pantalla, "Vida:", (20, 48))
        for i in range(self.vida_jugador):
            pygame.draw.rect(pantalla, (80, 220, 120), (90 + i * 22, 50, 18, 18))
