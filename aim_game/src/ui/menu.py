import os

import pygame


class MenuPrincipal:
    """Gestiona la renderización y los eventos del menú de inicio del juego."""

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

        #ubicar la ruta del logo
        ruta_logo = os.path.join(directorio_base,"assets","gfx","logo.png")
        try:
            self.logo = pygame.image.load(ruta_logo).convert_alpha()
            self.logo = pygame.transform.scale(self.logo, (500,250))
        except FileNotFoundError:
            print("No se ha encontrado el logo.png")
            self.logo = None

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
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error cargando música del menú: {e}")

        # [NUEVO AUDIO] Cargar el efecto de sonido para los botones
        try:
            self.sonido_boton = pygame.mixer.Sound(ruta_sonido_boton)
            self.sonido_boton.set_volume(1.0)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error cargando sonido de botón: {e}")
            self.sonido_boton = None

    def reproducir_musica_fondo(self):
        # [NUEVO AUDIO] Método de apoyo por si necesitas reiniciar la música del menú luego de jugar
        try:
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error: {e}")

    def dibujar(self,pantalla):
        #Fondo oscuro porque no hay presupuesto (se agregará un fondito, calma, primero lo esencial).
        pantalla.fill((10,18,32))

        #obtener el rectangulo exacto de la pantalla actual
        rect_pantalla = pantalla.get_rect()

        if self.logo:
            rect_logo = self.logo.get_rect(center=(self.ancho * 0.68, 210))
            pantalla.blit(self.logo, rect_logo)

        #matemáticamente centrados
        self.rect_play.center = (rect_pantalla.centerx, 420)
        self.rect_quit.center = (rect_pantalla.centerx, 495)

        mouse_pos = pygame.mouse.get_pos()

        botones = [
            (self.rect_play, "JUGAR"),
            (self.rect_quit, "SALIR")
        ]

        for rect, texto in botones:
            if rect.collidepoint(mouse_pos):
                color_fondo = (45, 65, 90)
                color_borde = (150, 200, 255)
            else:
                color_fondo = (25, 35, 50)
                color_borde = (150, 200, 255)

            pygame.draw.rect(pantalla, color_fondo, rect, border_radius=8)
            pygame.draw.rect(pantalla, color_borde, rect, width=2, border_radius=8)

            txt_render = self.fuente_botones.render(texto, True, (255, 255, 255))
            pantalla.blit(txt_render, txt_render.get_rect(center=rect.center))

    def manejar_evento(self,evento):
        """Revisa si el usuario hizo clic en algún botón y retorna la acción"""
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_play.collidepoint(evento.pos):
                # [AUDIO] Reproducir sonido de interfaz
                if self.sonido_boton:
                    self.sonido_boton.play()
                return "JUGAR"
            elif self.rect_quit.collidepoint(evento.pos):
                # [AUDIO] Reproducir sonido de interfaz
                if self.sonido_boton:
                    self.sonido_boton.play()
                return "SALIR"
        return None

class MenuPausa:
    def __init__(self, ancho, alto, directorio_base):
        self.ancho = ancho
        self.alto = alto
        
        ruta_fuente = os.path.join(directorio_base, "src", "ui", "Pix32.ttf")
        try:
            self.fuente_titulo = pygame.font.Font(ruta_fuente, 48)
            self.fuente_botones = pygame.font.Font(ruta_fuente, 24)
        except FileNotFoundError:
            self.fuente_titulo = pygame.font.Font(None, 48)
            self.fuente_botones = pygame.font.Font(None, 24)

        # Dimensiones y posiciones de los botones
        w_boton, h_boton = 280, 50
        x_centro = self.ancho // 2
        
        self.rect_continuar = pygame.Rect(0, 0, w_boton, h_boton)
        self.rect_continuar.center = (x_centro, self.alto // 2 - 10)
        
        self.rect_salir = pygame.Rect(0, 0, w_boton, h_boton)
        self.rect_salir.center = (x_centro, self.alto // 2 + 70)

        # Cargar sonido de clic
        ruta_sonido_boton = os.path.join(directorio_base, "sounds", "ui_effect.wav")
        try:
            self.sonido_boton = pygame.mixer.Sound(ruta_sonido_boton)
        except (pygame.error, FileNotFoundError):
            self.sonido_boton = None

    def dibujar(self, pantalla):
        # Título
        texto_titulo = self.fuente_titulo.render("PAUSA", True, (255, 255, 255))
        pantalla.blit(texto_titulo, texto_titulo.get_rect(center=(self.ancho // 2, self.alto // 2 - 100)))

        # Lógica de Hover (detectar posición del ratón)
        mouse_pos = pygame.mouse.get_pos()

        botones = [
            (self.rect_continuar, "CONTINUAR"),
            (self.rect_salir, "SALIR AL MENU")
        ]

        for rect, texto in botones:
            # Si el ratón choca con el rectángulo, iluminamos el fondo y el borde
            if rect.collidepoint(mouse_pos):
                color_fondo = (45, 65, 90)  # Azul claro (Hover)
                color_borde = (150, 200, 255)
            else:
                color_fondo = (25, 35, 50)  # Azul oscuro (Normal)
                color_borde = (100, 150, 255)

            # Dibujar caja y borde
            pygame.draw.rect(pantalla, color_fondo, rect, border_radius=8)
            pygame.draw.rect(pantalla, color_borde, rect, width=2, border_radius=8)
            
            # Dibujar texto
            txt_render = self.fuente_botones.render(texto, True, (255, 255, 255))
            pantalla.blit(txt_render, txt_render.get_rect(center=rect.center))

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_continuar.collidepoint(evento.pos):
                if self.sonido_boton: self.sonido_boton.play()
                return "CONTINUAR"
            else: 
                self.rect_salir.collidepoint(evento.pos)
                if self.sonido_boton: self.sonido_boton.play()
                return "SALIR_MENU"
        return None

class MenuResultados:

    """Desglosa las estadísticas de rendimiento (aciertos, fallos, precisión) al finalizar el temporizador."""
    def __init__(self, ancho, alto, directorio_base):
        self.ancho = ancho
        self.alto = alto
        ruta_fuente = os.path.join(directorio_base, "src", "ui", "Pix32.ttf")
        try:
            self.fuente_titulo = pygame.font.Font(ruta_fuente, 28)
            self.fuente_puntos = pygame.font.Font(ruta_fuente, 56)
            self.fuente_texto = pygame.font.Font(ruta_fuente, 18)
        except FileNotFoundError:
            self.fuente_titulo = pygame.font.Font(None, 36)
            self.fuente_puntos = pygame.font.Font(None, 64)
            self.fuente_texto = pygame.font.Font(None, 24)

        # Dimensiones del panel central
        self.rect_panel = pygame.Rect(0, 0, 420, 480)
        self.rect_panel.center = (self.ancho // 2, self.alto // 2)
        
        # Dimensiones y posición de los botones
        w_boton, h_boton = 160, 45
        self.rect_reiniciar = pygame.Rect(self.rect_panel.left + 30, self.rect_panel.bottom - 75, w_boton, h_boton)
        self.rect_salir = pygame.Rect(self.rect_panel.right - 190, self.rect_panel.bottom - 75, w_boton, h_boton)

        ruta_sonido_boton = os.path.join(directorio_base, "sounds", "ui_effect.wav")
        try:
            self.sonido_boton = pygame.mixer.Sound(ruta_sonido_boton)
        except (pygame.error, FileNotFoundError):
            self.sonido_boton = None

    def dibujar(self, pantalla, stats):
        # Fondo oscuro
        pantalla.fill((10, 18, 32))

        # Panel principal y borde azul
        pygame.draw.rect(pantalla, (15, 25, 40), self.rect_panel, border_radius=8)
        pygame.draw.rect(pantalla, (45, 85, 140), self.rect_panel, width=2, border_radius=8)

        # Textos superiores
        txt_titulo = self.fuente_titulo.render("PARTIDA TERMINADA", True, (255, 255, 255))
        pantalla.blit(txt_titulo, txt_titulo.get_rect(center=(self.ancho // 2, self.rect_panel.top + 40)))

        txt_sub = self.fuente_texto.render("PUNTUACIÓN FINAL", True, (150, 200, 255))
        pantalla.blit(txt_sub, txt_sub.get_rect(center=(self.ancho // 2, self.rect_panel.top + 90)))

        # Puntuación grande en amarillo
        txt_pts = self.fuente_puntos.render(str(stats['puntuacion']), True, (255, 215, 0))
        pantalla.blit(txt_pts, txt_pts.get_rect(center=(self.ancho // 2, self.rect_panel.top + 145)))

        # Línea divisoria
        pygame.draw.line(pantalla, (45, 85, 140), (self.rect_panel.left + 30, self.rect_panel.top + 200), (self.rect_panel.right - 30, self.rect_panel.top + 200), 2)

        # Listado de Estadísticas
        y_offset = self.rect_panel.top + 230
        espaciado = 35
        etiquetas = ["TIEMPO DE JUEGO", "ACIERTOS", "FALLADOS", "PRECISIÓN"]
        valores = [stats['tiempo'], str(stats['aciertos']), str(stats['fallos']), f"{stats['precision']}%"]

        for i in range(4):
            txt_eti = self.fuente_texto.render(etiquetas[i], True, (200, 200, 200))
            txt_val = self.fuente_texto.render(valores[i], True, (100, 200, 255))
            pantalla.blit(txt_eti, (self.rect_panel.left + 40, y_offset + (i * espaciado)))
            pantalla.blit(txt_val, txt_val.get_rect(topright=(self.rect_panel.right - 40, y_offset + (i * espaciado))))

        # Renderizar botones con efecto Hover
        mouse_pos = pygame.mouse.get_pos()
        for rect, texto in [(self.rect_reiniciar, "REINICIAR"), (self.rect_salir, "SALIR")]:
            if rect.collidepoint(mouse_pos):
                color_fondo = (35, 75, 165) # Botón iluminado
                color_borde = (150, 200, 255)
            else:
                color_fondo = (20, 35, 60)  # Botón normal
                color_borde = (45, 85, 140)
            
            pygame.draw.rect(pantalla, color_fondo, rect, border_radius=6)
            pygame.draw.rect(pantalla, color_borde, rect, width=1, border_radius=6)
            txt_btn = self.fuente_texto.render(texto, True, (255, 255, 255))
            pantalla.blit(txt_btn, txt_btn.get_rect(center=rect.center))

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_reiniciar.collidepoint(evento.pos):
                if self.sonido_boton: self.sonido_boton.play()
                return "REINICIAR"
            elif self.rect_salir.collidepoint(evento.pos):
                if self.sonido_boton: self.sonido_boton.play()
                return "SALIR"
        return None