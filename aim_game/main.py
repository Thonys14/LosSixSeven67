"""Módulo principal que inicializa el bucle del juego, renderiza entidades y controla la máquina de estados."""

import pygame
import sys
import os

from src.ui.menu import MenuPrincipal, MenuPausa, MenuResultados 
from src.player.shooter import Crosshair 
from src.targets.rings import Diana 
from src.player.character import Personaje
from src.effects.feedback import EfectosVisuales
from src.ui.window_controls import ControlesVentana
from src.ui.intro import IntroPartida
from src.game.settings import GestorConfiguracion

def main():
    # (evita errores de audio en windows -_-)
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.init()

    # Forzar el ícono personalizado en la barra de tareas de Windows
    try:
        import ctypes
        myappid = 'mi_estudio.aim_trainer.1_0' # Identificador único de tu aplicación
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except AttributeError:
        pass 

    directorio_base = os.path.dirname(__file__)
    config = GestorConfiguracion(directorio_base)

    try: 
        pygame.display.set_icon(pygame.image.load(config.ruta_icono))
    except FileNotFoundError: 
        pass

    try:
        sonido_fin = pygame.mixer.Sound(config.ruta_sonido_fin)
        sonido_disparo = pygame.mixer.Sound(config.ruta_sonido_disparo)
        sonido_acierto = pygame.mixer.Sound(config.ruta_sonido_acierto)
        config.aplicar_volumen_sfx([sonido_fin, sonido_disparo, sonido_acierto])
    except Exception:
        sonido_fin = sonido_disparo = sonido_acierto = None

    #display
    pantalla = pygame.display.set_mode((config.ancho, config.alto), pygame.NOFRAME)
    #cargar cursor
    config.cargar_cursor()
    #reloj
    reloj = pygame.time.Clock()

    #fuente_ui
    try:
        fuente_ui = pygame.font.Font(config.ruta_fuente, 20) 
        fuente_resultados = pygame.font.Font(config.ruta_fuente, 30)
    except FileNotFoundError:
        fuente_ui = pygame.font.Font(None, 30)
        fuente_resultados = pygame.font.Font(None, 42)

    personaje = Personaje(config.ancho, config.alto, config.ruta_personaje)
    area_textos = pygame.Rect(8, 70, config.ancho - 16, config.alto - 195)
    efectos = EfectosVisuales(fuente_resultados, area_textos)
    controles_ventana = ControlesVentana(config.ancho)
    intro = IntroPartida(
        (config.ancho, config.alto), personaje.imagen, fuente_resultados, fuente_ui
    )

    tiempo_limite = config.tiempo_limite
    tiempo_inicio = 0 
    tiempo_inicio_pausa = 0

    # instanciar menús
    menu_principal = MenuPrincipal(config.ancho, config.alto, directorio_base)
    menu_pausa = MenuPausa(config.ancho, config.alto, directorio_base) 
    menu_resultados = MenuResultados(config.ancho, config.alto, directorio_base) 
    estado_actual = "MENU"

    #crosshair
    try:
        imagen_crosshair = pygame.image.load(config.ruta_crosshair_juego).convert()
        imagen_crosshair.set_colorkey((0, 0, 0))
    except FileNotFoundError:
        print("No se encontró el sprite 'crosshair.png'")
        imagen_crosshair = None

    jugador = Crosshair(imagen_crosshair)
    diana_actual = None

    #bg in-game
    try:
        fondo = pygame.image.load(config.ruta_fondo).convert()
        fondo = pygame.transform.scale(fondo, (config.ancho, config.alto))
    except Exception:
        print(f"Error: No se encontró la imagen de fondo")
        fondo = pygame.Surface((config.ancho, config.alto))
        fondo.fill((20, 30, 40))

    # variables de partida
    puntuacion_temporal = 0
    disparos_totales = 0
    aciertos = 0 
    fallos = 0

    while True:
        dt = reloj.get_time() / 1000.0
        
        # gestión de cursor
        config.actualizar_cursor(estado_actual)
        
        efectos.actualizar(dt)
        personaje.actualizar(dt)

        if estado_actual == "CINEMATICA":
            intro.actualizar(dt)
            if intro.terminada:
                estado_actual = "JUEGO"
                tiempo_inicio = pygame.time.get_ticks()
                efectos.limpiar()
                try:
                    pygame.mixer.music.load(config.ruta_musica_juego)
                    pygame.mixer.music.play(-1)
                except Exception as e:
                    print(f"Error reproduciendo música: {e}")

        if estado_actual == "JUEGO":
            transcurrido = pygame.time.get_ticks() - tiempo_inicio
            if transcurrido >= tiempo_limite * 1000:
                estado_actual = "RESULTADOS"
                efectos.limpiar()
                pygame.mixer.music.stop()
                if sonido_fin:
                    sonido_fin.play()

        #gestión de entradas de usuario
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            accion_ventana = controles_ventana.manejar_evento(evento)
            if accion_ventana == "SALIR":
                pygame.quit()
                sys.exit()
            if accion_ventana == "MINIMIZAR":
                pygame.display.iconify()
                continue

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if estado_actual == "JUEGO":
                        estado_actual = "PAUSA"
                        tiempo_inicio_pausa = pygame.time.get_ticks()
                    elif estado_actual == "PAUSA":
                        estado_actual = "JUEGO"
                        tiempo_inicio += pygame.time.get_ticks() - tiempo_inicio_pausa
                    elif estado_actual == "RESULTADOS":
                        estado_actual = "MENU"
                        puntuacion_temporal = disparos_totales = aciertos = fallos = 0
                        diana_actual = None
                        efectos.limpiar()
                        pygame.mixer.music.stop()
                        try:
                            pygame.mixer.music.load(config.ruta_musica_lobby)
                            pygame.mixer.music.play(-1)
                        except Exception:
                            pass

                elif evento.key == pygame.K_SPACE and estado_actual == "CINEMATICA":
                    estado_actual = "JUEGO"
                    tiempo_inicio = pygame.time.get_ticks() 
                    efectos.limpiar()
                    try:
                        pygame.mixer.music.load(config.ruta_musica_juego)
                        pygame.mixer.music.play(-1)
                    except Exception:
                        pass
        
            #evento de clic in-game
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if (
                    estado_actual == "JUEGO"
                    and diana_actual is not None
                    and pygame.time.get_ticks() - tiempo_inicio < tiempo_limite * 1000
                ):
                    if sonido_disparo:
                        sonido_disparo.play()
                        
                    personaje.disparar()
                    efectos.disparar(personaje.origen_disparo, evento.pos)
                    disparos_totales += 1 
                    puntos = 0

                    if diana_actual.esta_visible:
                        puntos = jugador.disparar(
                            diana_actual.posicion, diana_actual.radio, evento.pos
                        )
                    if puntos > 0:
                        aciertos += 1 
                        puntuacion_temporal += puntos
                        efectos.registrar_acierto(diana_actual, evento.pos, puntos)
                        
                        if sonido_acierto:
                            sonido_acierto.play()

                        diana_actual = Diana(config.ancho, config.alto)
                    else:
                        fallos += 1 
        
            # lógica menús
            if estado_actual == "MENU":
                accion = menu_principal.manejar_evento(evento)
                if accion == "JUGAR":
                    intro.reiniciar()
                    estado_actual = "CINEMATICA"
                elif accion == "SALIR":
                    pygame.quit()
                    sys.exit()

            if estado_actual == "PAUSA":
                accion_pausa = menu_pausa.manejar_evento(evento)
                if accion_pausa == "CONTINUAR":
                    estado_actual = "JUEGO"
                    tiempo_inicio += pygame.time.get_ticks() - tiempo_inicio_pausa
                elif accion_pausa == "SALIR_MENU":
                    estado_actual = "MENU"
                    puntuacion_temporal = disparos_totales = aciertos = fallos = 0
                    diana_actual = None
                    efectos.limpiar()
                    pygame.mixer.music.stop()
                    try:
                        pygame.mixer.music.load(config.ruta_musica_lobby)
                        pygame.mixer.music.play(-1)
                    except Exception:
                        pass

            if estado_actual == "RESULTADOS":
                accion_resultados = menu_resultados.manejar_evento(evento)
                if accion_resultados == "REINICIAR":
                    estado_actual = "JUEGO"
                    puntuacion_temporal = disparos_totales = aciertos = fallos = 0
                    tiempo_inicio = pygame.time.get_ticks()
                    diana_actual = None
                    efectos.limpiar()
                    pygame.mixer.music.stop()
                    try:
                        pygame.mixer.music.load(config.ruta_musica_juego)
                        pygame.mixer.music.play(-1)
                    except Exception:
                        pass
                        
                elif accion_resultados == "SALIR":
                    estado_actual = "MENU"
                    puntuacion_temporal = disparos_totales = aciertos = fallos = 0
                    diana_actual = None
                    efectos.limpiar()
                    pygame.mixer.music.stop()
                    try:
                        pygame.mixer.music.load(config.ruta_musica_lobby)
                        pygame.mixer.music.play(-1)
                    except Exception:
                        pass

        # renderizado en pantalla
        if estado_actual == "MENU":
            menu_principal.dibujar(pantalla)
        
        elif estado_actual == "CINEMATICA":
            intro.dibujar(pantalla)
        
        elif estado_actual == "JUEGO":
            if fondo is None:
                pantalla.fill((20, 30, 40))
            else:
                pantalla.blit(fondo, (0, 0))

            tiempo_actual = pygame.time.get_ticks()
            segundos_transcurridos = (tiempo_actual - tiempo_inicio) // 1000
            tiempo_restante = max(0, tiempo_limite - segundos_transcurridos)

            if tiempo_restante == 0 and estado_actual != "RESULTADOS":
                estado_actual = "RESULTADOS"
                efectos.limpiar()
                pygame.mixer.music.stop()
                if sonido_fin: sonido_fin.play()

            if diana_actual is None:
                diana_actual = Diana(config.ancho, config.alto)
            
            efectos.dibujar_dianas_salientes(pantalla)
            diana_actual.actualizar(dt)
            diana_actual.dibujar(pantalla)
            personaje.dibujar(pantalla)
            efectos.dibujar(pantalla)

            texto_puntos_sombra = fuente_ui.render(f"Puntos: {puntuacion_temporal}", True, (0, 0, 0))
            texto_puntos = fuente_ui.render (f"Puntos: {puntuacion_temporal}", True, (255,255,255))
            pantalla.blit(texto_puntos_sombra, (22, 22)) 
            pantalla.blit(texto_puntos, (20, 20))

            color_tiempo = (255, 100, 100) if tiempo_restante <= 10 else (255, 255, 255)
            texto_tiempo_sombra = fuente_ui.render(f"Tiempo: {tiempo_restante}s", True, (0, 0, 0))
            texto_tiempo = fuente_ui.render(f"Tiempo: {tiempo_restante}s", True, color_tiempo)

            rect_tiempo = texto_tiempo.get_rect(topright=(config.ancho - 96, 20))
            rect_sombra = texto_tiempo_sombra.get_rect(topright=(config.ancho - 94, 22))

            pantalla.blit(texto_tiempo_sombra, rect_sombra)
            pantalla.blit(texto_tiempo, rect_tiempo)

            jugador.actualizar()
            jugador.dibujar(pantalla)

        elif estado_actual == "RESULTADOS":
            precision = int((aciertos / disparos_totales) * 100) if disparos_totales > 0 else 0
            minutos = tiempo_limite // 60
            segundos = tiempo_limite % 60
            tiempo_formateado = f"{minutos:02d}:{segundos:02d}"

            stats_partida = {
                'puntuacion': puntuacion_temporal,
                'tiempo': tiempo_formateado,
                'aciertos': aciertos,
                'fallos': fallos,
                'precision': precision
            }
            menu_resultados.dibujar(pantalla, stats_partida)

        elif estado_actual == "PAUSA":
            if fondo is None: pantalla.fill((20, 30, 40))
            else: pantalla.blit(fondo, (0, 0))
            
            efectos.dibujar_dianas_salientes(pantalla)
            if diana_actual: diana_actual.dibujar(pantalla)
            personaje.dibujar(pantalla)
            efectos.dibujar(pantalla)

            velo = pygame.Surface((config.ancho, config.alto), pygame.SRCALPHA)
            velo.fill((0, 0, 0, 180))
            pantalla.blit(velo, (0, 0))

            menu_pausa.dibujar(pantalla)

        # actualizar la pantalla
        controles_ventana.dibujar(pantalla)
        pygame.display.flip()
        reloj.tick(config.fps)

if __name__ == "__main__":
    main()