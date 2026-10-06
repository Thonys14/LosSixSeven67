import os
import pygame

class GestorConfiguracion:
    def __init__(self, directorio_base):
        # dimensiones globales
        self.ancho = 800
        self.alto = 600
        self.fps = 60
        self.tiempo_limite = 60

        # centralización de todas las rutas
        self.dir_base = directorio_base
        self.ruta_fuente = os.path.join(self.dir_base, "src", "ui", "Pix32.ttf")
        self.ruta_logo = os.path.join(self.dir_base, "assets", "gfx", "logo.png")
        self.ruta_icono = os.path.join(self.dir_base, "assets", "gfx", "icon.png")
        self.ruta_fondo = os.path.join(self.dir_base, "assets", "gfx", "background.jpg")
        self.ruta_personaje = os.path.join(self.dir_base, "assets", "gfx", "robot.png")
        
        # rutas de los cursores (juego y menús)
        self.ruta_crosshair_juego = os.path.join(self.dir_base, "assets", "gfx", "crosshair.png")
       
        self.ruta_cursor_menu = os.path.join(self.dir_base, "assets", "gfx", "crosshair_menu.png") 
        
        # rutas de Audio
        self.ruta_musica_juego = os.path.join(self.dir_base, "sounds", "training_song.mp3")
        self.ruta_musica_lobby = os.path.join(self.dir_base, "sounds", "lobby_song.mp3")
        self.ruta_sonido_fin = os.path.join(self.dir_base, "sounds", "finish_effect.wav")
        self.ruta_sonido_disparo = os.path.join(self.dir_base, "sounds", "shoot_effect.wav")
        self.ruta_sonido_acierto = os.path.join(self.dir_base, "sounds", "blanco_effect.wav")
        self.ruta_sonido_boton = os.path.join(self.dir_base, "sounds", "ui_effect.wav")

        # configuración inicial de audio
        self.vol_musica = 0.5
        self.vol_sfx = 1.0

        # cursor en menús
        self.cursor_menu = None

    def cargar_cursor(self):
        try:
            # Cargar imagen y escalarla a tamaño de cursor estándar (ej. 32x32)
            img_cursor = pygame.image.load(self.ruta_cursor_menu).convert_alpha()
            img_cursor = pygame.transform.scale(img_cursor, (32, 32))
            #  (el centro)
            self.cursor_menu = pygame.cursors.Cursor((12, 12), img_cursor)
        except Exception:
            # si no aparece una cualquiera en su lugar
            print(f"no aparecio el cursor nuevo ruta: {self.ruta_cursor_menu}" )
            self.cursor_menu = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    def actualizar_cursor(self, estado_actual):
        """Alterna entre el dibujado manual del juego y el cursor personalizado de UI."""
        if estado_actual == "JUEGO":
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
        else:
            # cursor nuevo
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
            if self.cursor_menu: 
                pygame.mouse.set_cursor(self.cursor_menu)

    def aplicar_volumen_musica(self, valor=None):
        if valor is not None:
            self.vol_musica = valor
        pygame.mixer.music.set_volume(self.vol_musica)

    def aplicar_volumen_sfx(self, lista_sonidos, valor=None):
        if valor is not None:
            self.vol_sfx = valor
        for sonido in lista_sonidos:
            if sonido:
                sonido.set_volume(self.vol_sfx)