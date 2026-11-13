# Investigación y base de conocimiento – Tarea 1

**Tema n.º 4:** Recomendador de rutina de ejercicio (plan general según objetivo, nivel y tiempo).
**Curso:** CIA02 – Introducción a la Inteligencia Artificial, Universidad Creativa.
**Autor:** Daniela Arce Orozco · **Fecha:** 12 de noviembre de 2026

> **Aviso:** el sistema da consejos generales de actividad física. No son consejos médicos y no sustituyen a un profesional de la salud.

---

## a) Fuentes consultadas

Abrí y leí cada una de estas páginas el **11/11/2026** (entre las 21:42 y las 21:44, hora de Costa Rica). En cada caso comprobé el título, la organización y el enlace.

| ID | Título | Autor / organización | Enlace | Fecha de la fuente | Criterio que aporta |
|----|--------|----------------------|--------|--------------------|---------------------|
| F1 | *WHO guidelines on physical activity and sedentary behaviour* | Organización Mundial de la Salud (OMS) | https://www.who.int/publications/i/item/9789240015128 | Publicada el 25/11/2020 (ISBN 9789240015128) | Documento oficial con las directrices vigentes por grupo de edad. |
| F2 | *World Health Organization 2020 guidelines on physical activity and sedentary behaviour* | Bull F. C., Al-Ansari S. S., Biddle S. y otros. *British Journal of Sports Medicine* 54(24):1451-1462 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7719906/ | 23/11/2020 (doi:10.1136/bjsports-2020-102955) | Resume en un artículo las directrices de la OMS. Aporta: 150-300 min/semana de intensidad moderada o 75-150 min de intensidad vigorosa; fuerza de todos los grupos musculares grandes 2 o más días por semana; para mayores de 65 años, actividad "multicomponente" de equilibrio y fuerza 3 o más días por semana; empezar con poco y aumentar poco a poco la frecuencia, la intensidad y la duración; en general no hace falta un permiso médico previo para actividad ligera o moderada si no hay contraindicaciones. |
| F3 | *Actividad física* (nota descriptiva) | OMS | https://www.who.int/es/news-room/fact-sheets/detail/physical-activity | Actualizada el 04/11/2026 | Un poco de actividad es mejor que nada y toda actividad cuenta; todas las edades deben fortalecer los músculos y reducir el tiempo sentado. |
| F4 | *Adult Activity: An Overview* | Centers for Disease Control and Prevention (CDC), EE. UU. | https://www.cdc.gov/physical-activity-basics/guidelines/adults.html | Actualizada el 03/11/2023 | Los 150 min se pueden repartir, por ejemplo 30 min × 5 días. Fuerza 2 o más días que trabaje piernas, caderas, espalda, abdomen, pecho, hombros y brazos. La alternativa vigorosa es de 75 min (por ejemplo, trotar). |
| F5 | *Older Adult Activity: An Overview* | CDC | https://www.cdc.gov/physical-activity-basics/guidelines/older-adults.html | Actualizada el 04/12/2025 | A partir de los 65 años: actividad aeróbica, de fuerza **y de equilibrio**. Si no se pueden cumplir las metas, moverse tanto como lo permitan la capacidad y las condiciones de salud. |
| F6 | *Adding Physical Activity as an Adult* | CDC | https://www.cdc.gov/physical-activity-basics/adding-adults/index.html | Actualizada el 04/12/2025 | La actividad moderada es segura para la mayoría. Con una enfermedad crónica (por ejemplo, del corazón, artritis o diabetes) conviene hablar con el médico. También antes de empezar actividad vigorosa si la persona ha estado inactiva. |
| F7 | *Physical Activity and Your Weight and Health* | CDC | https://www.cdc.gov/healthy-weight-growth/physical-activity/index.html | Actualizada el 07/04/2026 | Para controlar el peso puede hacer falta más de 150 min/semana. La actividad física debe ir junto con una alimentación saludable, y la fuerza se mantiene 2 días por semana. |
| F8 | *Guías de actividad física para Costa Rica 2025* (1.ª ed., 35 p., ISBN 978-9977-62-296-5) | Ministerio de Salud de Costa Rica – Red Costarricense de Actividad Física para la Salud (RECAFIS) | https://www.ministeriodesalud.go.cr/index.php/biblioteca-de-archivos-left/documentos-ministerio-de-salud/ministerio-de-salud/recafis/9075-guias-de-actividad-fisica-para-costa-rica/file | 2025 | Guía nacional que adopta las metas de la OMS. Aporta: se puede fraccionar el tiempo en bloques de 5-10 min; nadar y andar en bicicleta son recomendables para personas con problemas en las articulaciones o con sobrepeso; la fuerza se puede trabajar con el propio peso y con objetos cotidianos; quien tenga una enfermedad crónica debe consultar a profesionales; a partir de los 65 años, equilibrio y fuerza 3 o más días por semana para evitar caídas. |

**Fuentes que no se usan:**
- **ACSM** (acsm.org): el sitio rechazó el acceso automático (HTTP 403), así que no pude abrir sus páginas. Queda **POR VERIFICAR** y no se cita.
- **Wikipedia:** no se usó.

---

## b) Factores (preguntas) y sus valores

La clave interna es la misma que usa el código.

| # | Factor (clave) | Pregunta | Valores posibles | Fuente del factor |
|---|----------------|----------|------------------|-------------------|
| P1 | `edad` | Rango de edad | `menor_18`, `18_64`, `65_mas` | F2, F5, F8: la OMS y la guía de Costa Rica dan recomendaciones distintas para los grupos de 18-64 años y de 65 o más. |
| P2 | `condicion_cronica` | ¿Tiene alguna enfermedad crónica diagnosticada (corazón, presión alta, diabetes u otra) o le indicaron limitar el ejercicio? | `si`, `no` | F6, F8 |
| P3 | `molestias` | ¿Tiene molestias o dolor en las articulaciones (rodillas, cadera, espalda, hombros)? | `si`, `no` | F8 (problemas articulares → nadar o bicicleta) |
| P4 | `nivel` | Nivel actual de actividad | `principiante` (poco o nada activo), `intermedio` (activo de forma regular), `avanzado` (entrena con regularidad y a intensidad alta) | F2 (empezar con poco), F6 (inactivo → consultar antes de actividad vigorosa) |
| P5 | `objetivo` | Objetivo principal | `salud_general`, `control_peso`, `fuerza`, `resistencia` | F4, F7 |
| P6 | `minutos` | Minutos disponibles por sesión | `menos_20`, `20_40`, `mas_40` | F4, F8 (meta de 150 min/semana; se puede fraccionar) |
| P7 | `dias` | Días por semana | `1_2`, `3_4`, `5_mas` | F4 (30 min × 5 días), F8 |
| P8 | `equipo` | Equipo disponible | `ninguno`, `bandas_mancuernas`, `maquinas` | F8 (fuerza con el propio peso u objetos), F4 |

**Cambio respecto a la propuesta inicial:** quité la pregunta "lugar". Ninguna de las fuentes usa el lugar como criterio para decidir el tipo de plan, y lo que de verdad importa del lugar (si hay pesas o máquinas) ya lo recoge la pregunta P8 sobre el equipo. A cambio agregué P2 (enfermedad crónica), porque las fuentes F6 y F8 la señalan como el criterio principal para recomendar una consulta previa.

### Hechos intermedios que deduce el sistema

Ninguno de estos hechos se pregunta al usuario: los producen las reglas intermedias.

| Hecho | Valores | Significado |
|-------|---------|-------------|
| `perfil` | `adulto`, `adulto_mayor` | El grupo de edad para el que existen recomendaciones (18-64 o 65 y más). |
| `restriccion` | `ninguna`, `bajo_impacto` | Si conviene evitar impactos (saltos, correr) por molestias articulares. |
| `disponibilidad` | `limitada`, `adecuada` | Si el tiempo semanal alcanza para acercarse a la meta de 150 min. |
| `intensidad` | `progresiva`, `vigorosa_posible` | Si hay que empezar suave e ir subiendo, o si se puede incluir trabajo vigoroso. |
| `modalidad_fuerza` | `peso_corporal`, `cargas` | Cómo se trabaja la fuerza con el equipo disponible. |
| `apto` | `plan_estandar` | Persona adulta, sin restricción y con tiempo adecuado: puede seguir un plan según su objetivo. |

---

## c) Conclusiones posibles (10 finales)

| Clave | Recomendación (resumen) |
|-------|-------------------------|
| `plan_salud_general` | Plan combinado de salud general: 150-300 min/semana de actividad aeróbica moderada, por ejemplo caminata rápida 30 min × 5 días, más fuerza de los grupos musculares grandes 2 días por semana. |
| `plan_control_peso` | Plan de control de peso: aeróbico moderado subiendo hacia 300 min/semana, más fuerza 2 días por semana, acompañado de una alimentación saludable. |
| `plan_fuerza_peso_corporal` | Plan de fuerza con el propio peso (sentadillas, flexiones apoyadas, plancha, subir gradas), 2-3 días no consecutivos, más actividad aeróbica moderada. |
| `plan_fuerza_cargas` | Plan de fuerza con bandas, mancuernas o máquinas para todos los grupos musculares grandes, 2-3 días no consecutivos, más actividad aeróbica moderada. |
| `plan_aerobico_progresivo` | Plan aeróbico progresivo: caminata rápida o bicicleta a ritmo moderado, aumentando poco a poco el tiempo hasta llegar a 150 min/semana, más fuerza 2 días. |
| `plan_aerobico_vigoroso` | Plan aeróbico con trabajo vigoroso (trote o intervalos): 75-150 min/semana, o una mezcla de moderado y vigoroso, más fuerza 2 días. |
| `plan_bloques_cortos` | Plan corto y fraccionado: bloques de 10-15 min repartidos en la semana, aumentando poco a poco los días o los minutos. |
| `plan_bajo_impacto` | Plan de bajo impacto: natación, ejercicios en el agua, bicicleta o caminata, y fuerza sin saltos, evitando los movimientos que causen dolor. |
| `plan_adulto_mayor` | Plan multicomponente para personas mayores: actividad aeróbica moderada, más equilibrio y fuerza 3 o más días por semana para prevenir caídas. |
| `consultar_profesional` | Consultar a un profesional de la salud antes de empezar o de aumentar la intensidad. |

---

## d) Reglas (30 en total)

El formato es: `R#: SI condición y condición ENTONCES hecho = valor (certeza N, tipo, fuente)`. Los ID, las condiciones, las conclusiones y las certezas son **idénticos** a los del código.

### Cómo se escogió la certeza de cada regla
- **90-95:** lo dicen las fuentes de forma explícita.
- **80-85:** es una interpretación razonable de lo que dicen las fuentes.
- **70-75:** es un criterio de prudencia o de sentido común.

Son estimaciones del autor, no valores estadísticos. La forma de combinarlas se explica en la sección "Cálculo de certeza".

### Reglas intermedias (producen hechos que usan otras reglas)

```
R1: SI edad = 18_64 ENTONCES perfil = adulto (certeza 95, intermedia, F2/F8)
R2: SI edad = 65_mas ENTONCES perfil = adulto_mayor (certeza 95, intermedia, F2/F5/F8)
R3: SI molestias = no ENTONCES restriccion = ninguna (certeza 90, intermedia, sentido común)
R4: SI molestias = si ENTONCES restriccion = bajo_impacto (certeza 85, intermedia, F8)
R5: SI minutos = menos_20 ENTONCES disponibilidad = limitada (certeza 85, intermedia, F4/F8)
R6: SI dias = 1_2 ENTONCES disponibilidad = limitada (certeza 85, intermedia, F4/F8)
R7: SI minutos = 20_40 y dias = 3_4 ENTONCES disponibilidad = adecuada (certeza 80, intermedia, F4/F8)
R8: SI minutos = 20_40 y dias = 5_mas ENTONCES disponibilidad = adecuada (certeza 90, intermedia, F4/F8)
R9: SI minutos = mas_40 y dias = 3_4 ENTONCES disponibilidad = adecuada (certeza 90, intermedia, F4/F8)
R10: SI minutos = mas_40 y dias = 5_mas ENTONCES disponibilidad = adecuada (certeza 90, intermedia, F4/F8)
R11: SI nivel = principiante ENTONCES intensidad = progresiva (certeza 90, intermedia, F2/F6)
R12: SI nivel = intermedio ENTONCES intensidad = vigorosa_posible (certeza 80, intermedia, F2/F4)
R13: SI nivel = avanzado ENTONCES intensidad = vigorosa_posible (certeza 85, intermedia, F2/F4)
R14: SI equipo = ninguno ENTONCES modalidad_fuerza = peso_corporal (certeza 90, intermedia, F8)
R15: SI equipo = bandas_mancuernas ENTONCES modalidad_fuerza = cargas (certeza 85, intermedia, F4/F8)
R16: SI equipo = maquinas ENTONCES modalidad_fuerza = cargas (certeza 85, intermedia, F4)
R17: SI perfil = adulto y restriccion = ninguna y disponibilidad = adecuada ENTONCES apto = plan_estandar (certeza 90, intermedia, F2/F4)
```

### Reglas finales (producen una conclusión)

```
R18: SI apto = plan_estandar y objetivo = salud_general ENTONCES conclusion = plan_salud_general (certeza 90, final, F2/F4)
R19: SI apto = plan_estandar y objetivo = control_peso ENTONCES conclusion = plan_control_peso (certeza 85, final, F7/F8)
R20: SI apto = plan_estandar y objetivo = fuerza y modalidad_fuerza = peso_corporal ENTONCES conclusion = plan_fuerza_peso_corporal (certeza 85, final, F4/F8)
R21: SI apto = plan_estandar y objetivo = fuerza y modalidad_fuerza = cargas ENTONCES conclusion = plan_fuerza_cargas (certeza 90, final, F2/F4)
R22: SI apto = plan_estandar y objetivo = resistencia y intensidad = progresiva ENTONCES conclusion = plan_aerobico_progresivo (certeza 90, final, F2/F4)
R23: SI apto = plan_estandar y objetivo = resistencia y intensidad = vigorosa_posible ENTONCES conclusion = plan_aerobico_vigoroso (certeza 85, final, F2/F4)
R24: SI perfil = adulto y disponibilidad = limitada ENTONCES conclusion = plan_bloques_cortos (certeza 80, final, F3/F4/F8)
R25: SI perfil = adulto y restriccion = bajo_impacto ENTONCES conclusion = plan_bajo_impacto (certeza 85, final, F8)
R26: SI perfil = adulto_mayor ENTONCES conclusion = plan_adulto_mayor (certeza 90, final, F2/F5/F8)
R27: SI perfil = adulto_mayor y restriccion = bajo_impacto ENTONCES conclusion = plan_bajo_impacto (certeza 85, final, F8)
R28: SI condicion_cronica = si ENTONCES conclusion = consultar_profesional (certeza 95, final, F6/F8)
R29: SI perfil = adulto_mayor y intensidad = progresiva ENTONCES conclusion = consultar_profesional (certeza 75, final, F6 + prudencia)
R30: SI restriccion = bajo_impacto y intensidad = progresiva ENTONCES conclusion = consultar_profesional (certeza 70, final, sentido común)
```

**Encadenamiento:** 17 reglas son intermedias. La cadena más larga tiene tres eslabones. Por ejemplo:
1. R1 (deduce `perfil`), R3 (deduce `restriccion`) y R8 (deduce `disponibilidad`).
2. R17 usa esos tres hechos y deduce `apto`.
3. R18 usa `apto` y produce la conclusión final.

### Cálculo de certeza
- **Certeza de una conclusión encadenada:** es el **mínimo** entre la certeza de la regla y la de cada hecho intermedio que usa. Una cadena no puede ser más segura que su eslabón más débil. Las respuestas del usuario cuentan con certeza 100.
- **Mismo hecho o conclusión por varias reglas:** si dos reglas llegan al mismo hecho o a la misma conclusión (por ejemplo R5 y R6, o R28, R29 y R30), se conserva la certeza **más alta**.
- **Empate de certeza entre conclusiones:** se ordenan por el número de regla más bajo.

### Verificación de consistencia
- **Sin duplicados:** no hay dos reglas con las mismas condiciones.
- **Sin contradicciones:** cada hecho intermedio solo puede tomar un valor en cada consulta.
  - `perfil`: R1 y R2 dependen de valores de `edad` que se excluyen entre sí.
  - `restriccion`: R3 y R4 dependen de `molestias = no` o `molestias = si`.
  - `disponibilidad`: los valores `limitada` y `adecuada` no pueden darse a la vez. "Adecuada" exige `minutos` distinto de `menos_20` **y** `dias` distinto de `1_2`, que son justo los casos en que se deduce "limitada".
  - `intensidad`: depende de un único `nivel`.
  - `modalidad_fuerza`: depende de un único `equipo`.
- **Todas las conclusiones son alcanzables:**

  | Conclusión | Regla(s) |
  |------------|----------|
  | `plan_salud_general` | R18 |
  | `plan_control_peso` | R19 |
  | `plan_fuerza_peso_corporal` | R20 |
  | `plan_fuerza_cargas` | R21 |
  | `plan_aerobico_progresivo` | R22 |
  | `plan_aerobico_vigoroso` | R23 |
  | `plan_bloques_cortos` | R24 |
  | `plan_bajo_impacto` | R25 y R27 |
  | `plan_adulto_mayor` | R26 |
  | `consultar_profesional` | R28, R29 y R30 |

---

## e) Limitaciones (combinaciones sin regla o tratadas de forma simple)

1. **Menores de 18 años:** la OMS tiene recomendaciones distintas para niños y adolescentes, y esta base no las incluye. Si `edad = menor_18`, ninguna regla de plan se activa y el sistema dice con claridad que no tiene conclusión. La única excepción es R28: si hay una enfermedad crónica, el sistema igual recomienda consultar a un profesional.
2. **Embarazo y discapacidad:** las fuentes tienen recomendaciones específicas para estos casos, pero el sistema no pregunta por ellos.
3. **Tiempo limitado:** cuando `disponibilidad = limitada`, el sistema recomienda el plan de bloques cortos y no un plan según el objetivo. El objetivo se aplica dentro de esos bloques.
4. **Persona mayor con poco tiempo:** a partir de los 65 años, el sistema recomienda siempre el plan multicomponente. No genera el plan de bloques cortos, porque R24 solo aplica a `perfil = adulto`.
5. **Límite inferior de "disponibilidad adecuada":** 20 min × 3 días suma unos 60 min por semana, muy por debajo de 150. Por eso R7 tiene una certeza más baja (80), y el plan pide aumentar el tiempo poco a poco.
6. **Molestias articulares:** el sistema no distingue entre molestias leves y lesiones agudas, ni dice en qué articulación están. Cualquier molestia se trata como `bajo_impacto`.
7. **Un solo objetivo por consulta:** no se combinan objetivos.
8. **Combinaciones poco coherentes** (por ejemplo, nivel "avanzado" con "1-2 días"): se aceptan tal como vienen, sin detectar incoherencias.
9. **Certezas:** son juicios del autor basados en lo explícita que es cada fuente, no probabilidades medidas.
10. **Reglas escritas a mano:** solo cubren lo que se previó. El sistema no aprende de los casos.
