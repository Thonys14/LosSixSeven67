import pygame
import os

class MenuPrincipal:
    def __init__(self,ancho,alto,directorio_base):
        self.ancho = ancho      #espacio de la clase en pantalla
        self.ancho= alto

        #Cargar la fuente dde /ui/boldMenuFont.tff
        ruta_fuente = os.path.join(directorio_base, "src", "ui","Pix32.ttf")
        try:
            self.fuente_titulo = pygame.font.Font(ruta_fuente,72)
            self.fuente_botones = pygame.font.Font(ruta_fuente,36)  
            print("Éxito: La fuente personalizada se cargó correctamente.")   #fuente de titulo y botones
        except FileNotFoundError:
            print(f"Advertencia: No se encontró la fuente en la ruta -> {ruta_fuente}")
            self.fuente_titulo = pygame.font.Font(None,72)
            self.fuente_botones = pygame.font.Font(None,36)

        self.rect_play = pygame.Rect(self.ancho//2 - 100, 380, 200, 60)
        self.rect_quit = pygame.Rect(self.ancho//2 - 100, 460, 200, 60)

        # [NUEVO AUDIO] Rutas de los sonidos usando la carpeta assets
        ruta_musica_lobby = os.path.join(directorio_base, "sounds", "lobby_song.mp3")
        ruta_sonido_boton = os.path.join(directorio_base, "sounds", "ui_effect.wav")

        # [NUEVO AUDIO] Cargar y reproducir la música de fondo del menú
        try:
            pygame.mixer.music.load(ruta_musica_lobby)
            pygame.mixer.music.play(-1) # El -1 la reproduce en bucle infinito
            pygame.mixer.music.set_volume(0.6) # Ajusta el volumen si la música es muy fuerte
        except Exception as e:
            print(f"Error cargando música del menú: {e}")

        # [NUEVO AUDIO] Cargar el efecto de sonido para los botones
        try:
            self.sonido_boton = pygame.mixer.Sound(ruta_sonido_boton)
            self.sonido_boton.set_volume(1.0)
        except Exception as e:
            print(f"Error cargando sonido de botón: {e}")
            self.sonido_boton = None

    def reproducir_musica_fondo(self):
        # [NUEVO AUDIO] Método de apoyo por si necesitas reiniciar la música del menú luego de jugar
        try:
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def dibujar(self,pantalla):
        #Fondo oscuro porque no hay presupuesto (se agregará un fondito, calma, primero lo esencial).
        pantalla.fill((15,20,30))

        #obtener el rectangulo exacto de la pantalla actual
        rect_pantalla = pantalla.get_rect()

        #1. lienzo digital (esto corrige los elementos hacia un costado).
        superficie_imagen = pygame.Surface((500,250))
        superficie_imagen.fill((40,50,70))

        #2. obtener el placeholder del lienzo
        rect_imagen = superficie_imagen.get_rect(midtop=(rect_pantalla.centerx, 50))

        #3. render del lienzo
        pantalla.blit(superficie_imagen, rect_imagen)

        texto_placeholder = self.fuente_botones.render("[ESPACIO PARA IMAGEN 500x250]", True, (150,150,150))
        pantalla.blit(texto_placeholder,texto_placeholder.get_rect(center=rect_imagen.center))

        #este titulo solo por si el logo no tiene letras; ciertamente no es posible.
        texto_titulo = self.fuente_titulo.render("Aim Trainer 2D", True, (255,255,255))
        pantalla.blit(texto_titulo, texto_titulo.get_rect(center=(rect_pantalla.centerx,350)))

        #botones

        #matemáticamente centrados
        self.rect_play.center = (rect_pantalla.centerx, 450)
        self.rect_quit.center = (rect_pantalla.centerx, 530)

        
        #boton JUGAR
        pygame.draw.rect(pantalla,(200,50,50),self.rect_play)
        texto_play = self.fuente_botones.render("JUGAR", True, (255,255,255))
        pantalla.blit(texto_play, texto_play.get_rect(center=self.rect_play.center))

        #boton salir
        pygame.draw.rect(pantalla,(200,50,50),self.rect_quit)
        texto_quit = self.fuente_botones.render("SALIR", True,(255,255,255))
        pantalla.blit(texto_quit,texto_quit.get_rect(center=self.rect_quit.center))

    def manejar_evento(self,evento):
        """Revisa si el usuario hizo clic en algún botón y retorna la acción"""
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_play.collidepoint(evento.pos):
                # [NUEVO AUDIO] Reproducir sonido de interfaz
                if self.sonido_boton:
                    self.sonido_boton.play()
                return "JUGAR"
            elif self.rect_quit.collidepoint(evento.pos):
                # [NUEVO AUDIO] Reproducir sonido de interfaz
                if self.sonido_boton:
                    self.sonido_boton.play()
                return "SALIR"
        return None