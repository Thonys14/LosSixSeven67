Sugerimos varias ideas. Inicialmente tenemos pensado, la idea general es un videojuego en 2D con Python. De este juego hay varias temáticas: Peleas, Plataformas 
de disparos, Mundo abierto, Aim trainer.

La idea más fácil de ejecutar es el plataformero; sin embargo el más dinámico es el aimbot trainer.

Nos decidimos a hacer un Aim trainer.

Este pequeño desarrollo aparte de ser un medio de entretenimiento puede ayudar a mejorar nuestra capacidad de reflejos no solo limitado a videojuegos sino que abre un sin fin de posibilidades, hasta incluso en un contexto educativo pero, con temática distinta por obvias razones.

El Juego se basará en una mira que debe de pegarle a cada  objetivo que se muestra en pantalla, por cada objetivo, se conseguirán punto,, si por ejemplo le damos a una zona alejada del centro nos daría  un punto, pero  si le damos en el  centro del objetivo, nos  dará  3 o  5, por ejemplo,  el juego  consta con diferentes modos determinados un cronómetro de por ejemplo modo hardcore definido por un menor tiempo o la velocidad y/o tiempo en desaparecer los objetivos mediante el cual  el jugador debe de  conseguir todos  los puntos posibles, al final existirá la opción de  reiniciar  la partida o de salir, y marcará el puntaje final. Aquí podremos editar o elegir el modo en el que vamos a jugar, podemos seleccionar modo fácil, medio o difícil, esto hará que los objetivos a disparar tengan variabilidad de movimiento y sea más complicado. 

El prototipo contará con un sistema de puntajes, donde se podrá observar la puntuacion actual

Los objetivos serian:
Mejorar la capacidad de reflejos y de reacción al estar constantemente visualizando objetivos.
Que el usuario sea capaz de interactuar de forma activa y pueda comprender el objetivo del juego.

 


La estructura inicial del programa será la carpeta inicial del ejecutable como /juego/main.py/
en la carpeta juego estarán otras carpetas como /assets/pixel/… y demás.

 
 Aim Trainer 2D
Videojuego 2D desarrollado en Python utilizando principalmente la biblioteca Pygame, como proyecto para la asignatura de Desarrollo de Software 8.
 Idea del proyecto
Inicialmente se plantearon varias ideas para desarrollar un videojuego en 2D, entre ellas:
 Juego de peleas
 Juego de plataformas
 Juego de disparos
 Juego de mundo abierto
 Aim trainer
Después de analizar la complejidad y el tiempo disponible para desarrollar cada propuesta, se decidió realizar un Aim Trainer, debido a que permite crear una experiencia dinámica manteniendo un alcance adecuado para el proyecto.
Aunque el desarrollo de un juego de plataformas podía resultar más sencillo de ejecutar inicialmente, el Aim Trainer ofrece una mecánica más dinámica y permite incorporar diferentes niveles de dificultad, sistemas de puntuación y modos de juego sin aumentar excesivamente la complejidad del proyecto.
🎮 Descripción del juego
El juego se basa en una mecánica sencilla: el jugador utiliza el mouse como medio principal de interacción y debe acertar a los diferentes objetivos que aparecen en pantalla.
Cada objetivo tendrá diferentes zonas de puntuación. Por ejemplo, acertar una zona alejada del centro puede otorgar 1 punto, mientras que acertar directamente en el centro puede otorgar 3 o 5 puntos, dependiendo de las reglas definidas para el juego.
El jugador tendrá un tiempo determinado para conseguir la mayor cantidad de puntos posible.
Al finalizar la partida, se mostrará el puntaje final y el jugador podrá:
Reiniciar la partida.
Cambiar el modo de juego.
Salir del juego.
⚙️ Modos de juego
El juego contará inicialmente con diferentes niveles de dificultad:
🟢 Fácil: objetivos con movimientos y tiempos de aparición más sencillos.
🟡 Medio: mayor variabilidad en el movimiento y aparición de los objetivos.
🔴 Difícil: objetivos más rápidos, con menor tiempo de reacción y mayor dificultad.
También se contempla la posibilidad de incluir un modo Hardcore, en el cual el jugador tendrá un tiempo reducido o los objetivos permanecerán visibles durante un periodo más corto.
La dificultad podrá variar mediante diferentes factores, como:
Velocidad de movimiento de los objetivos.
Tiempo que permanecen visibles.
Tamaño de los objetivos.
Tiempo total de la partida.
Cantidad de objetivos que aparecen.
🏆 Sistema de puntuación
El prototipo contará con un sistema de puntuación basado en la precisión del jugador.
La puntuación podrá depender de la zona del objetivo donde se realice el impacto. De esta manera, los aciertos más precisos otorgarán una mayor cantidad de puntos.
Ejemplo:
Zona del objetivo
Puntos
Zona exterior
1 punto
Zona intermedia
3 puntos
Centro
5 puntos

El sistema podrá ampliarse posteriormente para incluir elementos como combos, precisión, cantidad de aciertos y estadísticas de la partida.
🎯 Objetivos del proyecto
Objetivo general
Desarrollar un videojuego 2D de entrenamiento de precisión y reflejos utilizando Python y Pygame.
Objetivos específicos
Mejorar la capacidad de reacción del jugador mediante la interacción constante con objetivos visuales.
Desarrollar una mecánica de juego sencilla, dinámica e interactiva.
Implementar un sistema de puntuación basado en la precisión.
Incorporar diferentes niveles de dificultad.
Permitir al usuario interactuar con el juego mediante el mouse.
Aplicar conceptos de desarrollo de software durante la planificación, implementación y organización del proyecto.
Desarrollar una aplicación que pueda servir como entretenimiento y, potencialmente, como base para otros usos relacionados con ejercicios de reacción y precisión.
🛠️ Tecnologías
El proyecto será desarrollado utilizando:
Python
Pygame
📁 Estructura inicial del proyecto
La estructura inicial del proyecto será organizada de la siguiente manera:
juego/
│
├── main.py
│
├── assets/
│   ├── pixel/
│   ├── sounds/
│   └── fonts/
│
├── src/
│   ├── player/
│   ├── targets/
│   ├── game/
│   └── ui/
│
└── README.md

La estructura podrá modificarse durante el desarrollo conforme se incorporen nuevas funcionalidades.
🚧 Estado del proyecto
En desarrollo.
Actualmente se encuentra en la etapa de planificación y definición de las mecánicas principales del juego.
Las características y sistemas descritos en este documento pueden cambiar durante el desarrollo dependiendo del tiempo disponible y de las necesidades del proyecto.
👥 Equipo de desarrollo
Integrantes:
Oriel Pinilla
Jhan Sánchez
Anthony Santamaría
Steven Batista
