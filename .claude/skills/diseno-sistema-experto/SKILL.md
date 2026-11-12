---
name: diseno-sistema-experto
description: Criterio de diseño para el sistema experto de rutinas de ejercicio (Tarea 1 CIA02). Úsalo al construir o mejorar la interfaz de terminal del .py (colores, menús, explicación, certezas) o la página de presentación del proyecto en docs/. Evita resultados genéricos y protege los requisitos de la tarea.
---

# Diseño del Sistema Experto de Rutinas de Ejercicio

Este proyecto es la Tarea 1 de CIA02 (Universidad Creativa): un sistema experto basado en reglas, en Python, que recomienda una rutina general de ejercicio. Este skill da dirección de diseño para dos superficies:

1. **La interfaz de terminal** del programa `.py`, que es lo que se califica.
2. **La página de presentación** en `docs/index.html`, para GitHub Pages. Es un extra de portafolio y no se califica.

La idea central del diseño: **un sistema experto se distingue por mostrar su razonamiento.** Todo el diseño debe hacer que el "¿Por qué?" sea la parte más clara y atractiva de la experiencia, no una nota al pie.

## Reglas que el diseño nunca puede romper

Antes de cualquier decisión estética, verifica que no rompes nada de esto:

- El `.py` usa **solo la biblioteca estándar**. Nada de `rich`, `colorama`, `curses` de terceros ni otros paquetes. Colores con códigos ANSI; interfaz gráfica, si se pide, solo con `tkinter`.
- Las reglas siguen siendo **datos** (lista de diccionarios) evaluados por una función aparte. El diseño cambia cómo se *muestran*, nunca cómo se *evalúan*.
- El **aviso de salud** ("consejo general, no sustituye a un profesional de la salud") aparece al inicio y al final de cada consulta, siempre legible y nunca escondido en colores tenues.
- Los colores se **desactivan** si `sys.stdout.isatty()` es falso o si existe la variable de entorno `NO_COLOR`. Sin colores, la salida debe seguir siendo perfectamente comprensible.
- El modo `--pruebas` produce salida sin colores ni adornos que rompan la comparación de resultados.
- Nada de lo que muestre la interfaz puede inventar datos: certezas, reglas y conclusiones salen tal cual de la base de conocimiento.

## Dirección estética: "bitácora de entrenamiento"

Piensa en la libreta de un buen entrenador: ordenada, directa, con anotaciones al margen que explican cada decisión. Sobria y con energía, nunca infantil ni "de gimnasio genérico".

Evita: emojis en cada línea, arcoíris de colores, banners ASCII gigantes, mayúsculas gritando, y en la web, gradientes morados, tipografías por defecto y tarjetas idénticas en cuadrícula.

## 1. Interfaz de terminal

### Paleta semántica

Cada color tiene **un solo significado**. Defínelos en un diccionario y úsalos solo a través de una función auxiliar (p. ej. `color(texto, rol)`):

| Rol | Uso | ANSI sugerido |
|---|---|---|
| `titulo` | encabezados de sección | negrita + cian |
| `pregunta` | texto de cada pregunta | negrita |
| `opcion` | número de cada opción | cian |
| `error` | entrada inválida | rojo |
| `exito` | recomendación principal | negrita + verde |
| `certeza` | barras y porcentajes | amarillo |
| `aviso` | aviso de salud | amarillo (nunca gris tenue) |
| `tenue` | texto secundario, separadores | atenuado (`\033[2m`) |

Máximo 2 o 3 colores visibles a la vez en una misma pantalla.

### Composición

- Ancho máximo de **72 caracteres**. Separadores con `─` y, si la terminal no soporta Unicode, con `-` (prueba con `sys.stdout.encoding`).
- Una línea en blanco entre bloques. Nunca más de dos seguidas.
- Muestra el progreso en cada pregunta: `Pregunta 3 de 8`.
- Las opciones van numeradas y alineadas, con sangría de dos espacios.

### Mensajes

- Trata al usuario de **usted**, de forma consistente.
- Errores que digan qué pasó y qué hacer: `Opción no válida. Escriba un número del 1 al 4.` Nunca culpes al usuario ni muestres un traceback.
- Salida limpia con Ctrl+C: `Consulta cancelada. ¡Hasta pronto!`

### La explicación es la protagonista

La explicación muestra la **cadena de razonamiento** como un árbol, con la certeza visible:

```
RECOMENDACIÓN PRINCIPAL
  Rutina de fuerza de bajo impacto          certeza ████████░░ 80

¿POR QUÉ?
  ├─ R2  molestias_articulares = sí
  │      → restriccion = bajo_impacto              (certeza 90)
  └─ R14 restriccion = bajo_impacto y objetivo = ganar músculo
         → Rutina de fuerza de bajo impacto        (certeza 80)

OTRAS OPCIONES
  · Movilidad y caminata                     certeza ██████░░░░ 60
```

- La barra de certeza es de 10 bloques (`█` llenos, `░` vacíos; con ASCII, `#` y `.`), seguida del número.
- Los hechos intermedios se distinguen de las conclusiones finales.
- Si no hay conclusión, dilo con calma y explica qué faltó: qué respuestas se dieron y que ninguna regla las cubre. Es una limitación del sistema, no un error del usuario.

## 2. Página de presentación (`docs/index.html`)

### Formato

- **Un solo archivo HTML** con CSS y JS en línea, sin herramientas de compilación, listo para GitHub Pages desde la carpeta `docs/`.
- Fuentes desde Google Fonts como máximo. Sugerencia: una grotesca con carácter para títulos (p. ej. *Bricolage Grotesque*) y una monoespaciada para las reglas y la demo (p. ej. *IBM Plex Mono*). Nada de Inter, Roboto ni Arial.
- Colores como variables CSS en `:root`, con modo oscuro mediante `prefers-color-scheme`. La paleta de la web debe dialogar con la de la terminal.

### Secciones, en este orden

1. **Hero**: qué hace el sistema en una frase, más un fragmento de terminal estilizado que muestre una consulta real.
2. **Cómo razona**: diagrama simple de *hechos → reglas → hechos intermedios → conclusión*. Explica el encadenamiento hacia adelante y las certezas.
3. **Las reglas**: tabla o lista de las reglas con su ID, **idénticas** a las del código y a `investigacion.md`. Nunca las reescribas ni las resumas de otra forma.
4. **Cómo ejecutarlo**: comandos para el programa y para `--pruebas`, y el requisito de Python 3 sin dependencias.
5. **Limitaciones**: reglas escritas a mano, conocimiento incompleto y casos sin conclusión. Es uno de los objetivos de la tarea: muéstralo con honestidad.
6. **Fuentes**: las referencias reales de `investigacion.md`, con enlace.
7. **Pie**: aviso de salud, curso y autoría.

### Movimiento

- Una sola entrada orquestada al cargar (p. ej. la consulta de la terminal "escribiéndose" línea por línea) vale más que muchos efectos dispersos.
- Respeta `prefers-reduced-motion`: sin animación, todo se muestra completo.
- Si el MCP de AnimatedWebs está conectado, puedes usarlo **solo para el hero**. Si no lo está, implementa el efecto con CSS y JS propios; nunca dejes el trabajo a medias por eso.

### Calidad mínima

- Contraste WCAG AA en ambos modos.
- Sin desplazamiento horizontal a 390 px de ancho; márgenes laterales de 16 px en móvil.
- HTML semántico (`header`, `main`, `section`, `footer`), con navegación por teclado.
- Sin rastreadores, analíticas ni datos personales del usuario.

## Lista de verificación antes de terminar

- [ ] `python -m py_compile` sin errores y `--pruebas` con todo en PASA.
- [ ] Con `NO_COLOR=1` y con la salida redirigida a un archivo, la interfaz se entiende y no muestra códigos ANSI sueltos.
- [ ] El aviso de salud se ve al inicio y al final de cada consulta.
- [ ] La explicación muestra la cadena completa y las certezas coinciden con la base de conocimiento.
- [ ] La entrada inválida avisa y vuelve a preguntar; Ctrl+C sale limpio.
- [ ] Si existe `docs/index.html`: las reglas coinciden con el código, funciona a 390 px, en modo oscuro y con movimiento reducido.
