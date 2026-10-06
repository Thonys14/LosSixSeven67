"""Niveles de dificultad: tamaño y velocidad de la nave objetivo."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Dificultad:
    """Parámetros de un nivel de dificultad.

    Atributos:
        nombre: texto que se muestra en el menú.
        escala: multiplicador del tamaño de la nave (menor = más difícil).
        velocidad: píxeles por segundo con que se mueve la nave.
    """

    nombre: str
    escala: float
    velocidad: float


FACIL = Dificultad("FACIL", 1.0, 50.0)
MEDIO = Dificultad("MEDIO", 0.75, 140.0)
DIFICIL = Dificultad("DIFICIL", 0.5, 200.0)

DIFICULTADES = (FACIL, MEDIO, DIFICIL)