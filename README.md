# 🎯 Aim Trainer 2D

Videojuego 2D desarrollado en **Python** utilizando principalmente la biblioteca **Pygame**, como proyecto para la asignatura **Desarrollo de Software 8**.

## 💡 Idea del proyecto

Inicialmente se plantearon varias ideas para desarrollar un videojuego en 2D: juego de peleas, juego de plataformas, juego de disparos e incluso un aim trainer.


Después de analizar la complejidad de cada propuesta y el tiempo disponible para el desarrollo, se decidió realizar un **Aim Trainer**, ya que permite crear una experiencia dinámica manteniendo un alcance adecuado para el proyecto.

Aunque un juego de plataformas podía resultar más sencillo de implementar, el Aim Trainer permite incorporar diferentes **niveles de dificultad, modos de juego y sistemas de puntuación** sin aumentar excesivamente la complejidad del proyecto.

## 🎮 Descripción del juego

El juego se basa en una mecánica sencilla: el jugador utilizará el **mouse como medio principal de interacción** y deberá acertar a los diferentes objetivos que aparecerán en pantalla.

Cada objetivo estará dividido en diferentes zonas de puntuación. Por ahora no lo tenemos distribuidos.

El jugador contará con un **tiempo determinado** para conseguir la mayor cantidad de puntos posible.

Al finalizar la partida, se mostrará el **puntaje final** y el jugador podrá:

* 🔄 Reiniciar la partida.
* 🚪 Salir del juego.

## ⚙️ Modos de juego y dificultad

El prototipo contará inicialmente con diferentes niveles de dificultad:

### 🟢 Fácil

* Objetivos con movimientos sencillos.
* Mayor tiempo de reacción.
* Mayor tiempo de permanencia de los objetivos.

### 🟡 Medio

* Mayor variabilidad en el movimiento.
* Menor tiempo de reacción.
* Aparición de objetivos con mayor frecuencia.

### 🔴 Difícil

* Objetivos más rápidos.
* Menor tiempo de reacción.
* Menor tiempo de permanencia de los objetivos.
* Mayor variabilidad en la posición y movimiento.


La dificultad podrá modificarse mediante diferentes factores:

* Velocidad de movimiento de los objetivos.
* Tiempo de permanencia en pantalla.
* Tamaño de los objetivos.
* Tiempo total de la partida.
* Cantidad de objetivos que aparecen.

## 🏆 Sistema de puntuación

El prototipo contará con un sistema de puntuación basado principalmente en la **precisión del jugador**.

La puntuación dependerá de la zona del objetivo donde se realice el impacto. Los aciertos más cercanos al centro otorgarán una mayor cantidad de puntos.

En futuras versiones, el sistema podría ampliarse para incluir:

* Combos.
* Porcentaje de precisión.
* Cantidad de aciertos.
* Cantidad de objetivos fallados.
* Tiempo promedio de reacción.
* Estadísticas de la partida.

## 🎯 Objetivos del proyecto

### Objetivo general

Desarrollar un videojuego 2D de entrenamiento de precisión y reflejos utilizando **Python y Pygame**.

### Objetivos específicos

* Mejorar la capacidad de reacción del jugador mediante la interacción constante con objetivos visuales.
* Desarrollar una mecánica de juego sencilla, dinámica e interactiva.
* Implementar un sistema de puntuación basado en la precisión.
* Incorporar diferentes niveles de dificultad.
* Permitir al usuario interactuar con el juego mediante el mouse.
* Aplicar conceptos de desarrollo de software durante la planificación, implementación y organización del proyecto.
* Desarrollar una aplicación que pueda servir como medio de entretenimiento y, potencialmente, como base para otros ejercicios relacionados con la reacción y la precisión.

## 🛠️ Tecnologías

El proyecto será desarrollado utilizando:

* **Python**
* **Pygame**

## 📁 Estructura inicial del proyecto

La estructura inicial del proyecto estará organizada de la siguiente manera:

```text
juego/
│
├── main.py
│
├── assets/
│   ├── pixel/
│   ├── sounds/
│   └── gfx/
│
├── src/
│   ├── player/
│   ├── targets/
│   ├── game/
│   └── ui/
│
└── README.md
```

Esta estructura podrá modificarse durante el desarrollo conforme se incorporen nuevas funcionalidades y componentes al proyecto.

## 🚧 Estado del proyecto

**En desarrollo.**

Actualmente, el proyecto se encuentra en la etapa de **planificación y definición de las mecánicas principales**.

Las características descritas en este documento representan la propuesta inicial y podrán modificarse durante el desarrollo, dependiendo del tiempo disponible, las necesidades del proyecto y las decisiones tomadas por el equipo.

## 👥 Equipo de desarrollo

* **Oriel Pinilla**
* **Jhan Sánchez**
* **Anthony Santamaría**
* **Steven Batista**
* **Maria Gonzales**
