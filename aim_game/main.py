import pygame
import sys
import os

# config base / es más fácil de argumentar
ANCHO, ALTO = 800, 600
FPS = 60

def main():
    pygame.init()

    #icono    
    directorio_base = os.path.dirname(__file__)
    ruta_icono = os.path.join(directorio_base,"assets","icon","icon.png")
    try:
        icono = pygame.image.load(ruta_icono)
        pygame.display.set_icon(icono)
    except FileNotFoundError:
        print(f"NO ESTA EL ICONO")


    #display
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("aim game")

    #fps
    reloj = pygame.time.Clock()


    # Estados disponibles contemplados: "CINEMATICA", "JUEGO", "RESULTADOS"
    estado_actual = "CINEMATICA"



    while True:
        # 1. primera parte: gestión de entradas de usuario
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # solo para ciclar más rápido los eventos durante el desarrollo
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_ESCAPE:
                    if estado_actual == "CINEMATICA":
                        estado_actual = "JUEGO"
                    elif estado_actual == "RESULTADOS":
                        estado_actual = "CINEMATICA" # Reiniciar ciclo

        
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

        # 3. actualizar la pantalla en base al framerate
        pygame.display.flip()
        reloj.tick(FPS)

        

if __name__ == "__main__":
    main()