# Flujo de Trabajo Colaborativo

## 1. Flujo Seleccionado: GitHub Flow
Hemos seleccionado **GitHub Flow** porque es un modelo de trabajo ágil e ideal para entregas continuas en equipos pequeños. Permite desarrollar características y solucionar defectos en ramas independientes y de corta duración, integrándolas a la rama `main` de forma segura mediante Pull Requests (PR) para mantener el proyecto siempre funcional.

## 2. Nomenclatura de Ramas
Toda rama nueva se crea a partir de `main` y utiliza prefijos descriptivos:
* `tipo-funcionalidad`: Para desarrollo de nuevas características (ej. `cambio-menu-pausa`).
* `correción/nombre-defecto`: Para correcciones de errores (ej. `correción-rebote-dianas`).
* `docs/nombre-documento`: Para actualizaciones en el README o documentación.

## 3. Ciclo de Vida de los Cambios
1. **Issue:** Se registra la tarea utilizando las plantillas del repositorio y se vincula al tablero de GitHub Projects, asignando un responsable.
2. **Desarrollo (Rama):** El responsable crea la rama local y trabaja en la solución.
3. **Commits:** Se realizan commits atómicos con sugerencias de los desarrolladores (ej. `agregar - calculo de precision matematica`).
4. **Pull Request:** Se abre un PR hacia la rama `main`, vinculándolo al issue que resuelve (ej. escribiendo `Closes #5`).
5. **Revisión y Aprobación:** 
   * Las GitHub Actions validan automáticamente la calidad y formato del código.
   * Otro miembro del equipo (distinto al autor) debe revisar el código y aprobar el PR.
6. **Integración (Merge):** Una vez aprobado y con las validaciones exitosas, los cambios se integran a `main`.