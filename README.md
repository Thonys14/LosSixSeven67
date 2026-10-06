# Aim game 2D 🎯

## 1. Problema y Usuarios
**Problema:** Muchos jugadores carecen de herramientas ligeras, reproducibles y de rápida ejecución para calentar sus reflejos y mejorar su precisión antes de iniciar sesiones de juegos competitivos.
**Usuarios:** Jugadores de videojuegos (*gamers*) y entusiastas de los e-sports que buscan mejorar su coordinación ojo-mano y precisión con el ratón.
**Alcance y Limitaciones:** Una aplicación de escritorio 2D enfocada en la precisión del clic y el tiempo de reacción. No incluye conectividad multijugador ni gráficos 3D complejos.

## 2. Requisitos Funcionales
1. **Aparición y dinámica de objetivos:** Las dianas deben aparecer dentro de un área jugable delimitada y rebotar matemáticamente en los bordes de la pantalla.
2. **Sistema de puntuación y métricas:** El sistema debe registrar los disparos totales, aciertos (otorgando puntos según la zona de impacto) y fallos, calculando la precisión exacta del usuario.
3. **Gestión de estados:** El juego debe permitir la transición fluida entre un Menú Principal, la Partida en curso, un Menú de Pausa (congelando el temporizador) y una Pantalla de Resultados Finales.

## 3. Tecnologías y Herramientas
* **Lenguaje:** Python 3.10+
* **Librería principal:** pygame-ce (3.5.8)
* **Análisis de calidad y seguridad:** Ruff (validación de formato PEP 8) y Snyk (análisis de vulnerabilidades de dependencias).

## 4. Instalación y Ejecución
1. Clonar el repositorio.
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual: 
   * Windows: `venv\Scripts\activate`
   * macOS/Linux: `source venv/bin/activate`
4. Instalar las dependencias: `python -m pip install -r requirements.txt`
5. Ejecutar el juego: `python main.py`

## 5. Configuración y Secretos
Este proyecto lee configuraciones desde variables de entorno. Puedes copiar el archivo `.env.example` y renombrarlo a `.env`. Actualmente, la solución no utiliza contraseñas, tokens ni credenciales sensibles que requieran protección en GitHub Secrets.

## 6. Equipo de Desarrollo
* **Oriel Pinilla [Supervisor de desarrollo, Dev]**
* **Jhan Sánchez [Supervisor general, Dev y Control de Calidad]**
* **Anthony Santamaría [Supervisor de Sonido, Host]**
* **Steven Batista [Desarrollador in-game]** 
* **Steephen Lascano [Diseñador gráfico]**
* **María González [Control de versiones, repositorio y documentación]**

## 7. Enlaces del Proyecto
* [Tablero de Seguimiento](https://github.com/users/Thonys14/projects/1)
* [Documentación del Flujo de Trabajo](docs/flujo_trabajo.md)