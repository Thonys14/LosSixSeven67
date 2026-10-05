import pygame
import sys
import os

from src.ui.menu import MenuPrincipal, MenuPausa, MenuResultados #clase menu
from src.player.shooter import Crosshair #puntero
from src.targets.rings import Diana #las dianas xd
from src.player.character import Personaje
from src.effects.feedback import EfectosVisuales
from src.ui.window_controls import ControlesVentana
from src.ui.intro import IntroPartida

# config base / es más fácil de argumentar
ANCHO, ALTO = 800, 600
FPS = 60

def main():
    # [AUDIO] Forzar inicialización limpia para evitar errores en Windows
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.init() 

    #icono    
    directorio_base = os.path.dirname(__file__)
    ruta_icono = os.path.join(directorio_base,"assets","gfx","icon.png") #ruta del ícono
    try:
        icono = pygame.image.load(ruta_icono) #ícono cargado
        pygame.display.set_icon(icono) #ícono se muestra
    except FileNotFoundError:
        print(f"NO ESTA EL ICONO")

    # [AUDIO] Cargar rutas de audio correctamente desde la carpeta assets
    ruta_musica_juego = os.path.join(directorio_base,  "sounds", "training_song.mp3")
    ruta_musica_lobby = os.path.join(directorio_base,  "sounds", "lobby_song.mp3")
    ruta_sonido_fin = os.path.join(directorio_base, "sounds", "finish_effect.wav")
    ruta_sonido_disparo = os.path.join(directorio_base, "sounds", "shoot_effect.wav")
    ruta_sonido_acierto = os.path.join(directorio_base, "sounds", "blanco_effect.wav")

    # [AUDIO] Instanciar los efectos de sonido y ajustar volumen
    try:
        sonido_fin = pygame.mixer.Sound(ruta_sonido_fin)
        sonido_disparo = pygame.mixer.Sound(ruta_sonido_disparo)
        sonido_acierto = pygame.mixer.Sound(ruta_sonido_acierto)
        
        sonido_fin.set_volume(1.0)
        sonido_disparo.set_volume(1.0)
        sonido_acierto.set_volume(1.0)
    except Exception as e:
        print(f"Advertencia: Faltan archivos de sonido o hubo un error -> {e}")
        sonido_fin = sonido_disparo = sonido_acierto = None

    #display
    pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.NOFRAME)
    pygame.display.set_caption("aim-trainer-game")

    #fps
    reloj = pygame.time.Clock()

    #jugador
    jugador = Crosshair()
    diana_actual = None
    puntuacion_temporal = 0

    #variables v3

    #fuente_ui
    ruta_fuente = os.path.join(directorio_base, "src", "ui","Pix32.ttf")
    try:
        fuente_ui = pygame.font.Font(ruta_fuente, 20) #fuente del ui
        fuente_resultados = pygame.font.Font(ruta_fuente, 30)
    except FileNotFoundError:
        fuente_ui = pygame.font.Font(None, 30)
        fuente_resultados = pygame.font.Font(None, 42)

    ruta_personaje = os.path.join(directorio_base, "assets", "gfx", "robot.png")
    personaje = Personaje(ANCHO, ALTO, ruta_personaje)
    area_textos = pygame.Rect(8, 70, ANCHO - 16, ALTO - 195)
    efectos = EfectosVisuales(fuente_resultados, area_textos)
    controles_ventana = ControlesVentana(ANCHO)
    intro = IntroPartida(
        (ANCHO, ALTO), personaje.imagen, fuente_resultados, fuente_ui
    )

    tiempo_limite = 60 #dura la partida
    tiempo_inicio = 0 #inicia la partida justo cuando se da en el botón JUGAR
    tiempo_inicio_pausa = 0

    #instancia de menú
    menu_principal = MenuPrincipal(ANCHO,ALTO,directorio_base)
    menu_principal = MenuPrincipal(ANCHO, ALTO, directorio_base)
    menu_pausa = MenuPausa(ANCHO, ALTO, directorio_base) # <-- NUEVO
    estado_actual = "MENU"

    #variables v4

    #crosshair
    ruta_sprite_crosshair = os.path.join(directorio_base,"assets","gfx","crosshair.png")
    try:
        imagen_crosshair = pygame.image.load(ruta_sprite_crosshair).convert()
        imagen_crosshair.set_colorkey((0, 0, 0))
    except FileNotFoundError:
        print(f"No se encontró el sprite 'crosshair.png'")
        imagen_crosshair = None

    jugador = Crosshair(imagen_crosshair)

    #bg in-game
    ruta_fondo = os.path.join(os.path.dirname(__file__),"assets","gfx", "background.jpg")
    try:
        fondo = pygame.image.load(ruta_fondo).convert()
        fondo = pygame.transform.scale(fondo,(ANCHO,ALTO))
    except:
        print(f"Error: No se encontró la imagen en {ruta_fondo}")
        fondo = pygame.Surface((ANCHO,ALTO))
        fondo.fill((20,30,40))

    #nuevas variables para la pantalla de resultados
    disparos_totales = 0
    aciertos = 0 
    fallos = 0

    menu_principal = MenuPrincipal(ANCHO, ALTO, directorio_base)
    menu_pausa = MenuPausa(ANCHO, ALTO, directorio_base) 
    menu_resultados = MenuResultados(ANCHO, ALTO, directorio_base) #

    ###############variables_v4###################3

    while True:
        dt = reloj.get_time() / 1000.0
        efectos.actualizar(dt)
        personaje.actualizar(dt)
        if estado_actual == "CINEMATICA":
            intro.actualizar(dt)
            if intro.terminada:
                estado_actual = "JUEGO"
                tiempo_inicio = pygame.time.get_ticks()
                efectos.limpiar()
                # [NUEVO AUDIO] Iniciar música de entrenamiento
                try:
                    pygame.mixer.music.load(ruta_musica_juego)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.5) # Baja el volumen un poco para oír disparos
                except Exception as e:
                    print(f"Error reproduciendo música: {e}")

        if estado_actual == "JUEGO":
            transcurrido = pygame.time.get_ticks() - tiempo_inicio
            if transcurrido >= tiempo_limite * 1000:
                estado_actual = "RESULTADOS"
                efectos.limpiar()
                # [NUEVO AUDIO] Detener música y reproducir sonido de fin
                pygame.mixer.music.stop()
                if sonido_fin:
                    sonido_fin.play()

        #gestión de entradas de usuario

        #evento de menu
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

            #al dar ESC, regresa al menu y limpia la puntuacion anterior
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if estado_actual == "JUEGO":
                        estado_actual = "PAUSA"
                        tiempo_inicio_pausa = pygame.time.get_ticks()
                    elif estado_actual == "PAUSA":
                        estado_actual = "JUEGO"
                        tiempo_en_pausa = pygame.time.get_ticks() - tiempo_inicio_pausa #quitar pausa
                        tiempo_inicio += tiempo_en_pausa
                    elif estado_actual == "RESULTADOS":
                        estado_actual = "MENU"
                        puntuacion_temporal = 0
                        diana_actual = None
                        efectos.limpiar()
                    
                    # [AUDIO] Detener sonido residual y volver a la música del lobby
                    pygame.mixer.music.stop()
                    try:
                        pygame.mixer.music.load(ruta_musica_lobby)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.6)
                    except Exception as e:
                        pass

                elif evento.key == pygame.K_SPACE and estado_actual == "CINEMATICA":    #cuando cambia de CINEMATICA a JUEGO
                    estado_actual = "JUEGO"
                    tiempo_inicio = pygame.time.get_ticks() #se reinicia el tiempo del contador
                    efectos.limpiar()
                    # [AUDIO] Iniciar música de entrenamiento si se salta la cinemática
                    try:
                        pygame.mixer.music.load(ruta_musica_juego)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.5)
                    except Exception as e:
                        print(f"Error reproduciendo música: {e}")
        
            #evento de clic in-game
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if (
                    estado_actual == "JUEGO"
                    and diana_actual is not None
                    and pygame.time.get_ticks() - tiempo_inicio < tiempo_limite * 1000
                ):
                    # [AUDIO] sonido de disparo
                    if sonido_disparo:
                        sonido_disparo.play()
                        
                    personaje.disparar()
                    efectos.disparar(personaje.origen_disparo, evento.pos)

                    disparos_totales +=1 #contar el disparo
                    puntos = 0

                    if diana_actual.esta_visible:
                        puntos = jugador.disparar(
                            diana_actual.posicion, diana_actual.radio, evento.pos
                        )
                    if puntos > 0:
                        aciertos += 1 # contar el acierto
                        puntuacion_temporal += puntos
                        efectos.registrar_acierto(diana_actual, evento.pos, puntos)
                        print(f"¡PIU! ¡PIU! +{puntos} | Total: {puntuacion_temporal}")
                        
                        # [NUEVO AUDIO] Reproducir sonido de impacto al acertar
                        if sonido_acierto:
                            sonido_acierto.play()

                        #nueva diana al acertar
                        diana_actual = Diana(ANCHO,ALTO)
                    else:
                        fallos += 1 # contar el fallo
                        print("¡FALLASTE, JAJA")
        
                # logica de control de acciones MENU
            if estado_actual == "MENU":
                #mostrar cursor normal de Windows
                pygame.mouse.set_visible(True)

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
                    menu_principal.reproducir_musica_fondo()
            # Lógica de control de acciones RESULTADOS
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
                        pygame.mixer.music.load(ruta_musica_juego)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.5)
                    except Exception:
                        pass
                        
                elif accion_resultados == "SALIR":
                    estado_actual = "MENU"
                    puntuacion_temporal = disparos_totales = aciertos = fallos = 0
                    diana_actual = None
                    efectos.limpiar()
                    
                    pygame.mixer.music.stop()
                    menu_principal.reproducir_musica_fondo()

        #control de renderizado de estado MENU
        if estado_actual == "MENU":
            menu_principal.dibujar(pantalla)
        elif estado_actual == "CINEMATICA":
            intro.dibujar(pantalla)
            #imagenes xd
        # control de renderizado de estado JUEGO
        elif estado_actual == "JUEGO":
            pygame.mouse.set_visible(False) #aquí se oculta el mouse, después crosshair

            if fondo is None:
                pantalla.fill((20, 30, 40))
            else:
                pantalla.blit(fondo,(0, 0))

            #logica del temporizador
            tiempo_actual = pygame.time.get_ticks()
            segundos_transcurridos = (tiempo_actual - tiempo_inicio) // 1000
            tiempo_restante = max(0, tiempo_limite - segundos_transcurridos)

            #entonces si el reloj llega a cero hay que forzar el estado 'resultado'
            if tiempo_restante == 0 and estado_actual != "RESULTADOS":
                estado_actual = "RESULTADOS"
                efectos.limpiar()
                # [AUDIO] respaldo: Detener música y reproducir sonido de fin
                pygame.mixer.music.stop()
                if sonido_fin:
                    sonido_fin.play()

            #Si no hay diana, creamos la primera
            if diana_actual is None:
                diana_actual = Diana(ANCHO, ALTO)
            #render de entidades
            efectos.dibujar_dianas_salientes(pantalla)
            diana_actual.actualizar(dt)
            diana_actual.dibujar(pantalla)
            personaje.dibujar(pantalla)
            efectos.dibujar(pantalla)

            #renderizado de interfaz in-game
            #render del texto: Puntos
            texto_puntos_sombra = fuente_ui.render(f"Puntos: {puntuacion_temporal}", True, (0, 0, 0))
            texto_puntos = fuente_ui.render (f"Puntos: {puntuacion_temporal}", True, (255,255,255))
            pantalla.blit(texto_puntos_sombra, (22, 22)) #posicion donde se muestra
            pantalla.blit(texto_puntos, (20, 20))

            #tiempo a la derecha para saber cuánto queda
            color_tiempo = (255, 100, 100) if tiempo_restante <= 10 else (255, 255, 255)
            texto_tiempo_sombra = fuente_ui.render(f"Tiempo: {tiempo_restante}s", True, (0, 0, 0))
            texto_tiempo = fuente_ui.render(f"Tiempo: {tiempo_restante}s", True, color_tiempo)

            rect_tiempo = texto_tiempo.get_rect(topright=(ANCHO - 96, 20))
            rect_sombra = texto_tiempo_sombra.get_rect(topright=(ANCHO - 94, 22))

            pantalla.blit(texto_tiempo_sombra, rect_sombra)
            pantalla.blit(texto_tiempo, rect_tiempo)

            jugador.actualizar()
            jugador.dibujar(pantalla)

        # renderizado de RESULTADOS
        elif estado_actual == "RESULTADOS":
            pygame.mouse.set_visible(True) 
            
            precision = int((aciertos / disparos_totales) * 100) if disparos_totales > 0 else 0
            # Formato de tiempo (ej. "01:00")
            minutos = tiempo_limite // 60
            segundos = tiempo_limite % 60
            tiempo_formateado = f"{minutos:02d}:{segundos:02d}"

            # Empaquetamos los datos para enviarlos a la clase visual
            stats_partida = {
                'puntuacion': puntuacion_temporal,
                'tiempo': tiempo_formateado,
                'aciertos': aciertos,
                'fallos': fallos,
                'precision': precision
            }
            
            menu_resultados.dibujar(pantalla, stats_partida)

        #renderizado de PAUSA
        elif estado_actual == "PAUSA":
            pygame.mouse.set_visible(True)

            #dibujar pantalla de juego exactamente igual pero no actualizamos
            if fondo is None: pantalla.fill ((20, 30, 40))
            else: pantalla.blit(fondo,(0, 0))
            efectos.dibujar_dianas_salientes(pantalla)
            if diana_actual: diana_actual.dibujar(pantalla)
            personaje.dibujar(pantalla)
            efectos.dibujar(pantalla)

            #superposición color negro con opacidad reducida
            velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            velo.fill((0, 0, 0, 180))
            pantalla.blit(velo, (0, 0))

            menu_pausa.dibujar(pantalla)

            #menu uww

        # 3. actualizar la pantalla en base al framerate
        controles_ventana.dibujar(pantalla)
        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    main()