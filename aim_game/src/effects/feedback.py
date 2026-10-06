"""[VISUAL]Proyectiles decorativos, impactos y puntos flotantes."""

import pygame

COLORES_PUNTOS = {
    100: (255, 225, 80),
    75: (255, 170, 65),
    50: (255, 80, 80),
    25: (95, 195, 255),
    10: (120, 255, 140),
    5: (255, 170, 65),
}


class Proyectil:
    """Viaja hasta el punto del clic sin intervenir en las colisiones."""

    DURACION = 0.14

    def __init__(self, origen, destino):
        self.origen = pygame.Vector2(origen)
        self.destino = pygame.Vector2(destino)
        self.edad = 0.0
        diferencia = self.destino - self.origen
        self.direccion = (
            diferencia.normalize()
            if diferencia.length_squared() > 0
            else pygame.Vector2(0, -1)
        )

    @property
    def terminado(self):
        return self.edad >= self.DURACION

    @property
    def posicion(self):
        avance = min(1.0, self.edad / self.DURACION)
        return self.origen.lerp(self.destino, avance)

    def actualizar(self, dt):
        """Avanza según segundos transcurridos, independientemente de los FPS."""
        self.edad += dt

    def dibujar(self, pantalla):
        punta = self.posicion
        cola = punta - self.direccion * 12
        pygame.draw.line(pantalla, (40, 210, 255), cola, punta, 4)
        pygame.draw.line(pantalla, (220, 255, 255), cola, punta, 2)


class Impacto:
    """Destello breve en la posición exacta del acierto."""

    DURACION = 0.22

    def __init__(self, posicion, color):
        self.posicion = pygame.Vector2(posicion)
        self.color = color
        self.edad = 0.0
        self.imagen = pygame.Surface((56, 56), pygame.SRCALPHA)

    @property
    def terminado(self):
        return self.edad >= self.DURACION

    def actualizar(self, dt):
        self.edad += dt

    def dibujar(self, pantalla):
        avance = min(1.0, self.edad / self.DURACION)
        radio = 4 + round(16 * avance)
        self.imagen.fill((0, 0, 0, 0))
        pygame.draw.circle(self.imagen, self.color, (28, 28), radio, 2)
        if avance < 0.4:
            pygame.draw.circle(self.imagen, (255, 255, 255), (28, 28), 3)
        for direccion in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            vector = pygame.Vector2(direccion)
            inicio = pygame.Vector2(28, 28) + vector * (radio + 2)
            final = pygame.Vector2(28, 28) + vector * (radio + 6)
            pygame.draw.line(self.imagen, self.color, inicio, final, 2)
        self.imagen.set_alpha(round(255 * (1 - avance)))
        rect = self.imagen.get_rect(center=self.posicion)
        pantalla.blit(self.imagen, rect)


class TextoFlotante:
    """Muestra los puntos de un acierto, asciende y se desvanece."""

    DURACION = 0.90

    def __init__(self, posicion, puntos, fuente):
        self.posicion = pygame.Vector2(posicion) + (0, -52)
        self.edad = 0.0
        color = COLORES_PUNTOS.get(puntos, (255, 255, 255))
        self.imagen = fuente.render(f"+{puntos}", True, color)
        self.sombra = fuente.render(f"+{puntos}", True, (0, 0, 0))

    @property
    def terminado(self):
        return self.edad >= self.DURACION

    def actualizar(self, dt):
        self.edad += dt
        self.posicion.y -= 42 * dt

    def dibujar(self, pantalla, area):
        # Mantenerlo legible antes de empezar el desvanecimiento.
        restante = max(0.0, self.DURACION - self.edad)
        opacidad = round(255 * min(1.0, restante / 0.30))
        self.imagen.set_alpha(opacidad)
        self.sombra.set_alpha(opacidad)
        rect = self.imagen.get_rect(center=self.posicion)
        rect.clamp_ip(area)
        pantalla.blit(self.sombra, rect.move(2, 2))
        pantalla.blit(self.imagen, rect)


class EfectosVisuales:
    """Conserva varios efectos simultáneos y retira los que terminaron."""

    def __init__(self, fuente, area_textos):
        self.fuente = fuente
        self.area_textos = area_textos.copy()
        self.proyectiles = []
        self.impactos = []
        self.textos = []
        self.dianas_salientes = []

    def disparar(self, origen, destino):
        """El disparo puede mostrarse tanto para aciertos como para fallos."""
        self.proyectiles.append(Proyectil(origen, destino))

    def registrar_acierto(self, diana, posicion_clic, puntos):
        """Guarda la diana anterior y muestra el resultado inmediatamente."""
        diana.iniciar_salida()
        self.dianas_salientes.append(diana)
        color = COLORES_PUNTOS.get(puntos, (255, 255, 255))
        self.impactos.append(Impacto(posicion_clic, color))
        self.textos.append(TextoFlotante(posicion_clic, puntos, self.fuente))

    def actualizar(self, dt):
        """Actualiza y elimina efectos, sin esperas que bloqueen el juego."""
        for efectos in (
            self.proyectiles,
            self.impactos,
            self.textos,
            self.dianas_salientes,
        ):
            for efecto in efectos:
                efecto.actualizar(dt)
            efectos[:] = [efecto for efecto in efectos if not efecto.terminado]

    def dibujar_dianas_salientes(self, pantalla):
        """Las dianas acertadas son decorativas y ya no reciben clics."""
        for diana in self.dianas_salientes:
            diana.dibujar(pantalla)

    def dibujar(self, pantalla):
        for proyectil in self.proyectiles:
            proyectil.dibujar(pantalla)
        for impacto in self.impactos:
            impacto.dibujar(pantalla)
        for texto in self.textos:
            texto.dibujar(pantalla, self.area_textos)

    def limpiar(self):
        """Evita arrastrar efectos a la siguiente partida."""
        self.proyectiles.clear()
        self.impactos.clear()
        self.textos.clear()
        self.dianas_salientes.clear()
