"""Botones propios para una ventana sin controles nativos."""

import pygame


class ControlesVentana:
    """Mantiene minimizar y cerrar disponibles en todos los estados."""

    def __init__(self, ancho):
        self.rect_minimizar = pygame.Rect(ancho - 76, 8, 28, 24)
        self.rect_cerrar = pygame.Rect(ancho - 40, 8, 28, 24)

    def manejar_evento(self, evento):
        """Devuelve una acción para que el controlador del juego la ejecute."""
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return None
        if self.rect_cerrar.collidepoint(evento.pos):
            return "SALIR"
        if self.rect_minimizar.collidepoint(evento.pos):
            return "MINIMIZAR"
        return None

    def dibujar(self, pantalla):
        mouse = pygame.mouse.get_pos()
        for rect in (self.rect_minimizar, self.rect_cerrar):
            color = (20, 45, 65)
            if rect.collidepoint(mouse):
                color = (
                    (130, 45, 55) if rect == self.rect_cerrar else (35, 80, 110)
                )
            pygame.draw.rect(pantalla, color, rect, border_radius=3)
            pygame.draw.rect(
                pantalla, (70, 150, 200), rect, width=1, border_radius=3
            )

        x, y = self.rect_minimizar.center
        pygame.draw.line(pantalla, (220, 245, 255), (x - 6, y + 3), (x + 6, y + 3), 2)
        x, y = self.rect_cerrar.center
        pygame.draw.line(pantalla, (240, 245, 255), (x - 5, y - 5), (x + 5, y + 5), 2)
        pygame.draw.line(pantalla, (240, 245, 255), (x + 5, y - 5), (x - 5, y + 5), 2)
