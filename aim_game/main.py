import pygame
import sys
import os

from src.ui.menu import MenuPrincipal #clase menu
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
    pygame.init()

    #icono    
    directorio_base = os.path.dirname(__file__)
    ruta_icono = os.path.join(directorio_base,"assets","gfx","icon.png") #ruta del ícono
    try:
        icono = pygame.image.load(ruta_icono) #ícono cargado
        pygame.display.set_icon(icono) #ícono se muestra
    except FileNotFoundError:
        print(f"NO ESTA EL ICONO")

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

    #instancia de menú
    menu_principal = MenuPrincipal(ANCHO,ALTO,directorio_base)

    estado_actual = "MENU"



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
        if estado_actual == "JUEGO":
            transcurrido = pygame.time.get_ticks() - tiempo_inicio
            if transcurrido >= tiempo_limite * 1000:
                estado_actual = "RESULTADOS"
                efectos.limpiar()
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
                if evento.key == pygame.K_ESCAPE and estado_actual == "RESULTADOS":
                    estado_actual = "MENU"
                    puntuacion_temporal = 0
                    diana_actual = None
                    efectos.limpiar()

                elif evento.key == pygame.K_SPACE and estado_actual == "CINEMATICA":    #cuando cambia de CINEMATICA a JUEGO
                    estado_actual = "JUEGO"
                    tiempo_inicio = pygame.time.get_ticks() #se reinicia el tiempo del contador
                    efectos.limpiar()
        
            #evento de clic in-game
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if (
                    estado_actual == "JUEGO"
                    and diana_actual is not None
                    and pygame.time.get_ticks() - tiempo_inicio < tiempo_limite * 1000
                ):
                    personaje.disparar()
                    efectos.disparar(personaje.origen_disparo, evento.pos)
                    puntos = 0
                    if diana_actual.esta_visible:
                        puntos = jugador.disparar(
                            diana_actual.posicion, diana_actual.radio, evento.pos
                        )
                    if puntos > 0:
                        puntuacion_temporal += puntos
                        efectos.registrar_acierto(diana_actual, evento.pos, puntos)
                        print(f"¡PIU! ¡PIU! +{puntos} | Total: {puntuacion_temporal}")

                        #nueva diana al acertar
                        diana_actual = Diana(ANCHO,ALTO)
                    else:
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

        #control de renderizado de estado MENU
        if estado_actual == "MENU":
            menu_principal.dibujar(pantalla)
        elif estado_actual == "CINEMATICA":
            intro.dibujar(pantalla)
            #imagenes xd
        # control de renderizado de estado JUEGO
        elif estado_actual == "JUEGO":
            pygame.mouse.set_visible(False) #aquí se oculta el mouse, después crosshair
            pantalla.fill((20, 30, 40))

            #logica del temporizador
            tiempo_actual = pygame.time.get_ticks()
            segundos_transcurridos = (tiempo_actual - tiempo_inicio) // 1000
            tiempo_restante = max(0, tiempo_limite - segundos_transcurridos)

            #entonces si el reloj llega a cero hay que forzar el estado 'resultado'
            if tiempo_restante == 0:
                estado_actual = "RESULTADOS"
                efectos.limpiar()

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

        #renderizado de RESULTADOS
        elif estado_actual == "RESULTADOS":
            pygame.mouse.set_visible(True) #devuelvo el cursor de windows
            pantalla.fill((15, 20, 30)) #fondo temporal

            #declaración de renders de texto
            texto_fin = fuente_resultados.render("Se terminó el tiempo. Veamos tu puntuación.", True, (255, 100, 100))
            texto_final_puntos = fuente_resultados.render (f"Puntuación Final: {puntuacion_temporal}", True, (100, 255, 100))
            texto_salir = fuente_resultados.render("Presiona ESC para salir", True, (150, 150, 150))
            #mostrar los textos
            pantalla.blit(texto_fin, texto_fin.get_rect(center=(ANCHO//2,ALTO//2 - 60)))
            pantalla.blit(texto_final_puntos, texto_final_puntos.get_rect(center=(ANCHO//2,ALTO//2)))
            pantalla.blit(texto_salir, texto_salir.get_rect(center=(ANCHO//2,ALTO//2 + 80)))

                
            """      
            # 2. por temas de desarrollo cambio de cinematicas
            if estado_actual == "CINEMATICA":
            # fondo para saber que es cinematica time
            pantalla.fill((20, 20, 20)) 
            # TODO: Añadir lógica para rotar las imágenes de IbisPaint
            
            elif estado_actual == "JUEGO":
            # fondo para saber que es el juego
            pantalla.fill((200, 220, 240)) 
            # TODO: Actualizar entidades, generar blancos, calcular vectores
            
            elif estado_actual == "RESULTADOS":
            # fondo para distinguir el game over
            pantalla.fill((100, 50, 50)) 
            # TODO: Mostrar puntuación final 
            
            """
        # 3. actualizar la pantalla en base al framerate
        controles_ventana.dibujar(pantalla)
        pygame.display.flip()
        reloj.tick(FPS)

        

if __name__ == "__main__":
    main()
