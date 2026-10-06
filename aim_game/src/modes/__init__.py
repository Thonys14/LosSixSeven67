"""Modos de juego disponibles en el Aim Trainer."""

from src.modes.clasico import ModoClasico
from src.modes.nucleo import ModoNucleo

# El menú recorre esta tupla; el primero es el modo por defecto.
MODOS = (ModoClasico,  ModoNucleo)
