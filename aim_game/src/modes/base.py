"""Clase base con la interfaz común de todos los modos de juego."""



class ModoJuego:
    """Interfaz que usa ``main.py`` para cualquier modo.

    Atributos de clase:
        nombre: texto que se muestra en el menú.
        duracion: segundos máximos de la partida.
        dibuja_personaje: False si el modo dibuja su propio jugador.
        fondo: "espacial" o "almacen", el fondo que usa main.py en la partida.

    Atributos de instancia:
        puntos: puntaje acumulado de la partida.
        terminado: True cuando el modo decide que la partida acabó.
        mensaje_final: texto para la pantalla de resultados.
    """

    nombre = "BASE"
    duracion = 60
    dibuja_personaje = True
    fondo = "espacial"

    def __init__(self, ancho, alto, dificultad, fuente, imagen_jugador=None):
        """Prepara el modo y lo deja listo para jugar.

        Args:
            ancho: ancho de la ventana en píxeles.
            alto: alto de la ventana en píxeles.
            dificultad: objeto ``Dificultad`` elegido en el menú.
            fuente: fuente de pygame para los textos del modo.
            imagen_jugador: superficie del jugador (solo la usa Núcleo).
        """
        self.ancho = ancho
        self.alto = alto
        self.dificultad = dificultad
        self.fuente = fuente
        self.imagen_jugador = imagen_jugador
        self.iniciar()

    def iniciar(self):
        """Reinicia puntos y estado de la partida."""
        self.puntos = 0
        self.terminado = False
        self.mensaje_final = ""

    def actualizar(self, dt, teclas):
        """Avanza la lógica del modo.

        Args:
            dt: segundos transcurridos desde el cuadro anterior.
            teclas: estado del teclado (``pygame.key.get_pressed()``).
        """

    def procesar_clic(self, posicion, efectos):
        """Procesa un disparo del jugador.

        Args:
            posicion: coordenadas (x, y) del clic.
            efectos: instancia de ``EfectosVisuales`` para mostrar aciertos.

        Returns:
            Puntos ganados (>0), 0 si falló o negativo si hubo penalización.
        """
        return 0

    def dibujar(self, pantalla):
        """Dibuja las entidades y el HUD propio del modo."""

    def origen_disparo(self, personaje):
        """Punto desde donde sale el proyectil visual."""
        return personaje.origen_disparo

    def dibujar_texto(self, pantalla, texto, posicion, color=(255, 255, 255)):
        """Dibuja un texto con sombra, con la esquina superior izquierda dada."""
        sombra = self.fuente.render(texto, True, (0, 0, 0))
        imagen = self.fuente.render(texto, True, color)
        pantalla.blit(sombra, (posicion[0] + 2, posicion[1] + 2))
        pantalla.blit(imagen, posicion)
