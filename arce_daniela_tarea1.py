# =============================================================================
# Nombre:  Daniela Arce
# Curso:   CIA02 - Introducción a la Inteligencia Artificial (Universidad Creativa)
# Tarea 1: Sistema Experto Basado en Reglas
# Tema 4:  Recomendador de rutina de ejercicio (plan general según objetivo,
#          nivel y tiempo)
# Fecha:   12 de noviembre de 2026
#
# Uso:
#   python arce_daniela_tarea1.py            -> consulta interactiva
#   python arce_daniela_tarea1.py --pruebas  -> ejecuta los casos de prueba
#   python arce_daniela_tarea1.py --gui      -> interfaz gráfica (tkinter)
# =============================================================================

import csv
import os
import sys
import textwrap
from datetime import datetime


# -----------------------------------------------------------------------------
# 1. CONSTANTES Y AVISO DE SALUD
# -----------------------------------------------------------------------------

# Archivo donde se guarda el historial de consultas (en la carpeta actual).
ARCHIVO_HISTORIAL = "historial_consultas.csv"

# Columnas del historial, en el orden en que se escriben.
COLUMNAS_HISTORIAL = [
    "fecha_hora",
    "respuestas",
    "reglas_activadas",
    "conclusion",
    "certeza",
    "alternativas",
]

# Aviso obligatorio para este tema: se muestra al inicio y al final de cada
# consulta.
AVISO_SALUD = (
    "Este sistema da consejos GENERALES de actividad física, no consejos "
    "médicos. No sustituye la valoración de un profesional de la salud. "
    "Si al hacer ejercicio siente dolor en el pecho, mareo o falta de aire, "
    "deténgase y busque atención médica."
)


# -----------------------------------------------------------------------------
# 2. PREGUNTAS (son datos: la función preguntar() las recorre de forma genérica)
# -----------------------------------------------------------------------------
# Cada pregunta tiene:
#   "clave":    nombre del hecho que se guarda con la respuesta
#   "texto":    lo que se le muestra al usuario
#   "tipo":     "menu" (opciones numeradas) o "sn" (sí / no)
#   "opciones": lista de pares (valor interno, texto que ve el usuario)

PREGUNTAS = [
    {
        "clave": "edad",
        "texto": "¿En qué rango de edad está?",
        "tipo": "menu",
        "opciones": [
            ("menor_18", "Menor de 18 años"),
            ("18_64", "De 18 a 64 años"),
            ("65_mas", "65 años o más"),
        ],
    },
    {
        "clave": "condicion_cronica",
        "texto": ("¿Tiene alguna enfermedad crónica diagnosticada (corazón, presión\n"
                  "alta, diabetes u otra) o le han indicado limitar el ejercicio?"),
        "tipo": "sn",
        "opciones": [("si", "Sí"), ("no", "No")],
    },
    {
        "clave": "molestias",
        "texto": ("¿Tiene molestias o dolor en las articulaciones\n"
                  "(rodillas, cadera, espalda, hombros)?"),
        "tipo": "sn",
        "opciones": [("si", "Sí"), ("no", "No")],
    },
    {
        "clave": "nivel",
        "texto": "¿Cuál es su nivel actual de actividad física?",
        "tipo": "menu",
        "opciones": [
            ("principiante", "Principiante (poco o nada activo)"),
            ("intermedio", "Intermedio (activo de forma regular)"),
            ("avanzado", "Avanzado (entreno con regularidad y a intensidad alta)"),
        ],
    },
    {
        "clave": "objetivo",
        "texto": "¿Cuál es su objetivo principal?",
        "tipo": "menu",
        "opciones": [
            ("salud_general", "Mejorar mi salud en general"),
            ("control_peso", "Controlar o bajar de peso"),
            ("fuerza", "Ganar fuerza"),
            ("resistencia", "Mejorar mi resistencia (cardio)"),
        ],
    },
    {
        "clave": "minutos",
        "texto": "¿Cuántos minutos tiene disponibles por sesión?",
        "tipo": "menu",
        "opciones": [
            ("menos_20", "Menos de 20 minutos"),
            ("20_40", "Entre 20 y 40 minutos"),
            ("mas_40", "Más de 40 minutos"),
        ],
    },
    {
        "clave": "dias",
        "texto": "¿Cuántos días por semana puede hacer ejercicio?",
        "tipo": "menu",
        "opciones": [
            ("1_2", "1 o 2 días"),
            ("3_4", "3 o 4 días"),
            ("5_mas", "5 días o más"),
        ],
    },
    {
        "clave": "equipo",
        "texto": "¿Con qué equipo cuenta?",
        "tipo": "menu",
        "opciones": [
            ("ninguno", "Ninguno (solo mi propio peso)"),
            ("bandas_mancuernas", "Bandas elásticas o mancuernas"),
            ("maquinas", "Máquinas de gimnasio"),
        ],
    },
]


# -----------------------------------------------------------------------------
# 3. BASE DE CONOCIMIENTO: CONCLUSIONES Y REGLAS (son datos, no código)
# -----------------------------------------------------------------------------

# Texto de cada conclusión final. La clave es la que aparece en las reglas.
CONCLUSIONES = {
    "plan_salud_general": {
        "titulo": "Plan combinado de salud general",
        "detalle": ("Acumule de 150 a 300 minutos por semana de actividad aeróbica "
                    "moderada (por ejemplo, caminata rápida 30 min, 5 días) y agregue "
                    "2 días de fuerza para piernas, cadera, espalda, abdomen, pecho, "
                    "hombros y brazos."),
    },
    "plan_control_peso": {
        "titulo": "Plan de control de peso",
        "detalle": ("Actividad aeróbica moderada casi todos los días, subiendo poco a "
                    "poco hacia 300 minutos por semana, más 2 días de fuerza. El "
                    "ejercicio funciona mejor junto con una alimentación saludable."),
    },
    "plan_fuerza_peso_corporal": {
        "titulo": "Plan de fuerza con el propio peso",
        "detalle": ("2 o 3 días no seguidos de sentadillas, flexiones apoyadas, "
                    "plancha, puente de cadera y subir gradas, trabajando todos los "
                    "grupos musculares grandes. Complete la semana con caminata u "
                    "otra actividad aeróbica moderada."),
    },
    "plan_fuerza_cargas": {
        "titulo": "Plan de fuerza con cargas (bandas, mancuernas o máquinas)",
        "detalle": ("2 o 3 días no seguidos de ejercicios con carga para piernas, "
                    "espalda, pecho, hombros, brazos y abdomen, aumentando la carga "
                    "de forma gradual. Complete la semana con actividad aeróbica "
                    "moderada."),
    },
    "plan_aerobico_progresivo": {
        "titulo": "Plan aeróbico progresivo",
        "detalle": ("Caminata rápida o bicicleta a ritmo moderado. Empiece con poco "
                    "tiempo y súmele unos minutos cada semana hasta llegar a 150 "
                    "minutos semanales. Agregue 2 días de fuerza."),
    },
    "plan_aerobico_vigoroso": {
        "titulo": "Plan aeróbico con trabajo vigoroso",
        "detalle": ("Trote, carrera o intervalos: de 75 a 150 minutos vigorosos por "
                    "semana, o una mezcla equivalente de moderado y vigoroso. "
                    "Agregue 2 días de fuerza."),
    },
    "plan_bloques_cortos": {
        "titulo": "Plan corto y fraccionado",
        "detalle": ("Use bloques de 10 a 15 minutos repartidos en el día y en la "
                    "semana, combinando actividad aeróbica y de fuerza según su "
                    "objetivo. Poco a poco sume días o minutos: algo de actividad "
                    "es mejor que nada."),
    },
    "plan_bajo_impacto": {
        "titulo": "Plan de bajo impacto",
        "detalle": ("Prefiera natación, ejercicios en el agua, bicicleta o caminata, "
                    "y fuerza sin saltos. Evite los movimientos que le causen dolor y "
                    "aumente la intensidad poco a poco."),
    },
    "plan_adulto_mayor": {
        "titulo": "Plan multicomponente para persona mayor",
        "detalle": ("Actividad aeróbica moderada (por ejemplo, caminar) y, 3 o más "
                    "días por semana, ejercicios de equilibrio y fuerza (pararse de "
                    "una silla, caminar talón-punta) para prevenir caídas."),
    },
    "consultar_profesional": {
        "titulo": "Consultar a un profesional de la salud antes de empezar",
        "detalle": ("Por su situación, conviene que un profesional de la salud le "
                    "indique el tipo y la cantidad de ejercicio adecuados antes de "
                    "empezar o de aumentar la intensidad."),
    },
}

# Reglas del sistema experto. Cada regla tiene:
#   "id":       identificador R1, R2, ...
#   "si":       condiciones; TODAS deben cumplirse (hecho = valor)
#   "entonces": hecho que se agrega (un solo par hecho: valor)
#   "certeza":  confianza en la regla, de 0 a 100
#   "tipo":     "intermedia" (produce un hecho para otras reglas) o
#               "final" (produce una recomendación para el usuario)
# Las reglas finales siempre concluyen el hecho "conclusion".
# Los mismos ID y textos están en investigacion.md.

REGLAS = [
    # --- Reglas intermedias -------------------------------------------------
    {"id": "R1", "si": {"edad": "18_64"},
     "entonces": {"perfil": "adulto"}, "certeza": 95, "tipo": "intermedia"},
    {"id": "R2", "si": {"edad": "65_mas"},
     "entonces": {"perfil": "adulto_mayor"}, "certeza": 95, "tipo": "intermedia"},
    {"id": "R3", "si": {"molestias": "no"},
     "entonces": {"restriccion": "ninguna"}, "certeza": 90, "tipo": "intermedia"},
    {"id": "R4", "si": {"molestias": "si"},
     "entonces": {"restriccion": "bajo_impacto"}, "certeza": 85, "tipo": "intermedia"},
    {"id": "R5", "si": {"minutos": "menos_20"},
     "entonces": {"disponibilidad": "limitada"}, "certeza": 85, "tipo": "intermedia"},
    {"id": "R6", "si": {"dias": "1_2"},
     "entonces": {"disponibilidad": "limitada"}, "certeza": 85, "tipo": "intermedia"},
    {"id": "R7", "si": {"minutos": "20_40", "dias": "3_4"},
     "entonces": {"disponibilidad": "adecuada"}, "certeza": 80, "tipo": "intermedia"},
    {"id": "R8", "si": {"minutos": "20_40", "dias": "5_mas"},
     "entonces": {"disponibilidad": "adecuada"}, "certeza": 90, "tipo": "intermedia"},
    {"id": "R9", "si": {"minutos": "mas_40", "dias": "3_4"},
     "entonces": {"disponibilidad": "adecuada"}, "certeza": 90, "tipo": "intermedia"},
    {"id": "R10", "si": {"minutos": "mas_40", "dias": "5_mas"},
     "entonces": {"disponibilidad": "adecuada"}, "certeza": 90, "tipo": "intermedia"},
    {"id": "R11", "si": {"nivel": "principiante"},
     "entonces": {"intensidad": "progresiva"}, "certeza": 90, "tipo": "intermedia"},
    {"id": "R12", "si": {"nivel": "intermedio"},
     "entonces": {"intensidad": "vigorosa_posible"}, "certeza": 80, "tipo": "intermedia"},
    {"id": "R13", "si": {"nivel": "avanzado"},
     "entonces": {"intensidad": "vigorosa_posible"}, "certeza": 85, "tipo": "intermedia"},
    {"id": "R14", "si": {"equipo": "ninguno"},
     "entonces": {"modalidad_fuerza": "peso_corporal"}, "certeza": 90, "tipo": "intermedia"},
    {"id": "R15", "si": {"equipo": "bandas_mancuernas"},
     "entonces": {"modalidad_fuerza": "cargas"}, "certeza": 85, "tipo": "intermedia"},
    {"id": "R16", "si": {"equipo": "maquinas"},
     "entonces": {"modalidad_fuerza": "cargas"}, "certeza": 85, "tipo": "intermedia"},
    {"id": "R17", "si": {"perfil": "adulto", "restriccion": "ninguna",
                         "disponibilidad": "adecuada"},
     "entonces": {"apto": "plan_estandar"}, "certeza": 90, "tipo": "intermedia"},

    # --- Reglas finales -----------------------------------------------------
    {"id": "R18", "si": {"apto": "plan_estandar", "objetivo": "salud_general"},
     "entonces": {"conclusion": "plan_salud_general"}, "certeza": 90, "tipo": "final"},
    {"id": "R19", "si": {"apto": "plan_estandar", "objetivo": "control_peso"},
     "entonces": {"conclusion": "plan_control_peso"}, "certeza": 85, "tipo": "final"},
    {"id": "R20", "si": {"apto": "plan_estandar", "objetivo": "fuerza",
                         "modalidad_fuerza": "peso_corporal"},
     "entonces": {"conclusion": "plan_fuerza_peso_corporal"}, "certeza": 85, "tipo": "final"},
    {"id": "R21", "si": {"apto": "plan_estandar", "objetivo": "fuerza",
                         "modalidad_fuerza": "cargas"},
     "entonces": {"conclusion": "plan_fuerza_cargas"}, "certeza": 90, "tipo": "final"},
    {"id": "R22", "si": {"apto": "plan_estandar", "objetivo": "resistencia",
                         "intensidad": "progresiva"},
     "entonces": {"conclusion": "plan_aerobico_progresivo"}, "certeza": 90, "tipo": "final"},
    {"id": "R23", "si": {"apto": "plan_estandar", "objetivo": "resistencia",
                         "intensidad": "vigorosa_posible"},
     "entonces": {"conclusion": "plan_aerobico_vigoroso"}, "certeza": 85, "tipo": "final"},
    {"id": "R24", "si": {"perfil": "adulto", "disponibilidad": "limitada"},
     "entonces": {"conclusion": "plan_bloques_cortos"}, "certeza": 80, "tipo": "final"},
    {"id": "R25", "si": {"perfil": "adulto", "restriccion": "bajo_impacto"},
     "entonces": {"conclusion": "plan_bajo_impacto"}, "certeza": 85, "tipo": "final"},
    {"id": "R26", "si": {"perfil": "adulto_mayor"},
     "entonces": {"conclusion": "plan_adulto_mayor"}, "certeza": 90, "tipo": "final"},
    {"id": "R27", "si": {"perfil": "adulto_mayor", "restriccion": "bajo_impacto"},
     "entonces": {"conclusion": "plan_bajo_impacto"}, "certeza": 85, "tipo": "final"},
    {"id": "R28", "si": {"condicion_cronica": "si"},
     "entonces": {"conclusion": "consultar_profesional"}, "certeza": 95, "tipo": "final"},
    {"id": "R29", "si": {"perfil": "adulto_mayor", "intensidad": "progresiva"},
     "entonces": {"conclusion": "consultar_profesional"}, "certeza": 75, "tipo": "final"},
    {"id": "R30", "si": {"restriccion": "bajo_impacto", "intensidad": "progresiva"},
     "entonces": {"conclusion": "consultar_profesional"}, "certeza": 70, "tipo": "final"},
]


# -----------------------------------------------------------------------------
# 4. FUNCIONES AUXILIARES: PRESENTACIÓN (COLORES Y SÍMBOLOS) E HISTORIAL
# -----------------------------------------------------------------------------

# Ancho máximo, en caracteres, de cualquier línea que imprime el programa.
ANCHO = 72

# Paleta semántica: cada color tiene UN solo significado. Solo se usa a
# través de la función color(); ninguna otra parte del código escribe
# códigos ANSI.
PALETA = {
    "titulo": "\033[1;36m",    # encabezados de sección (negrita + cian)
    "pregunta": "\033[1m",     # texto de cada pregunta (negrita)
    "opcion": "\033[36m",      # número de cada opción (cian)
    "error": "\033[31m",       # entrada no válida (rojo)
    "exito": "\033[1;32m",     # recomendación principal (negrita + verde)
    "certeza": "\033[33m",     # barras y valores de certeza (amarillo)
    "aviso": "\033[1;33m",     # aviso de salud (amarillo en negrita, nunca tenue)
    "tenue": "\033[2m",        # texto secundario y separadores (atenuado)
}
FIN_COLOR = "\033[0m"


def activar_ansi_windows():
    """En Windows, intenta activar los colores ANSI de la consola.

    Usa ctypes (biblioteca estándar) para encender el modo
    ENABLE_VIRTUAL_TERMINAL_PROCESSING. Devuelve True si lo logra.
    En otros sistemas no hace nada y devuelve True.
    """
    if os.name != "nt":
        return True
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        manejador = kernel32.GetStdHandle(-11)          # -11 = salida estándar
        modo = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(manejador, ctypes.byref(modo)):
            return False
        # 0x0004 = ENABLE_VIRTUAL_TERMINAL_PROCESSING
        return bool(kernel32.SetConsoleMode(manejador, modo.value | 0x0004))
    except Exception:
        # Si algo falla, simplemente seguimos sin colores.
        return False


def decidir_colores():
    """Decide si se usan colores.

    No se usan si existe la variable de entorno NO_COLOR, si la salida no es
    una terminal (por ejemplo, si se redirige a un archivo) o si Windows no
    permite activarlos.
    """
    if "NO_COLOR" in os.environ:
        return False
    if not sys.stdout.isatty():
        return False
    return activar_ansi_windows()


# Se decide una sola vez al iniciar el programa.
USAR_COLORES = decidir_colores()


def color(texto, rol):
    """Única función que pone color: aplica el color del rol indicado.

    Si los colores están desactivados o el rol no existe en PALETA,
    devuelve el texto sin cambios.
    """
    if not USAR_COLORES or rol not in PALETA:
        return texto
    return PALETA[rol] + texto + FIN_COLOR


# Símbolos de dibujo. Si la salida no puede escribir Unicode (por ejemplo,
# una consola antigua de Windows), se usan sus equivalentes en ASCII.
SIMBOLOS_UNICODE = {"linea": "─", "lleno": "█", "vacio": "░", "rama": "├─",
                    "ultima": "└─", "tronco": "│ ", "flecha": "→", "punto": "·"}
SIMBOLOS_ASCII = {"linea": "-", "lleno": "#", "vacio": ".", "rama": "|-",
                  "ultima": "`-", "tronco": "| ", "flecha": "->", "punto": "*"}


def elegir_simbolos():
    """Devuelve los símbolos Unicode si la codificación de la salida los
    admite; si no, devuelve la versión ASCII."""
    codificacion = getattr(sys.stdout, "encoding", None) or "ascii"
    try:
        "".join(SIMBOLOS_UNICODE.values()).encode(codificacion)
        return SIMBOLOS_UNICODE
    except (UnicodeEncodeError, LookupError):
        return SIMBOLOS_ASCII


SIMBOLOS = elegir_simbolos()


def ajustar(texto, sangria=2, sangria_siguientes=None):
    """Parte un texto largo en líneas de máximo ANCHO caracteres.

    sangria: espacios (o texto) al inicio de la primera línea.
    sangria_siguientes: lo mismo para las demás líneas (por defecto, igual).
    """
    if isinstance(sangria, int):
        sangria = " " * sangria
    if sangria_siguientes is None:
        sangria_siguientes = sangria
    elif isinstance(sangria_siguientes, int):
        sangria_siguientes = " " * sangria_siguientes
    return textwrap.wrap(texto, width=ANCHO, initial_indent=sangria,
                         subsequent_indent=sangria_siguientes)


def barra_certeza(certeza):
    """Barra de 10 bloques: un bloque lleno por cada 10 puntos de certeza."""
    llenos = certeza // 10
    return SIMBOLOS["lleno"] * llenos + SIMBOLOS["vacio"] * (10 - llenos)


def linea_separadora():
    """Una línea horizontal del ancho máximo, como segmento de texto."""
    return [(SIMBOLOS["linea"] * ANCHO, "tenue")]


# Las funciones que ARMAN texto devuelven una lista de líneas. Cada línea es a
# su vez una lista de segmentos (texto, rol). Así la consola puede pintar cada
# segmento con color() y la ventana gráfica con sus propias etiquetas.

def lineas_aviso():
    """Arma el aviso de salud enmarcado (se muestra al inicio y al final)."""
    marco = [(SIMBOLOS["linea"] * ANCHO, "aviso")]
    lineas = [marco, [(" AVISO DE SALUD", "aviso")]]
    for texto in ajustar(AVISO_SALUD, 1):
        lineas.append([(texto, "aviso")])
    lineas.append(marco)
    return lineas


def imprimir_lineas(lineas):
    """Imprime en la consola una lista de líneas formadas por segmentos."""
    for segmentos in lineas:
        print("".join(color(texto, rol) for texto, rol in segmentos))


def mostrar_aviso():
    """Imprime el aviso de salud enmarcado y en el color de aviso."""
    imprimir_lineas(lineas_aviso())


def guardar_historial(respuestas, resultado, ruta=ARCHIVO_HISTORIAL):
    """Agrega una fila con la consulta al archivo CSV del historial.

    Crea el encabezado si el archivo no existe o está vacío. Si no se puede
    escribir (permisos, disco lleno, etc.), avisa y devuelve False sin cerrar
    el programa.
    """
    conclusiones = resultado["conclusiones"]
    if conclusiones:
        principal = conclusiones[0]
        conclusion = principal["clave"]
        certeza = principal["certeza"]
        alternativas = "; ".join(
            "%s (%d)" % (c["clave"], c["certeza"]) for c in conclusiones[1:])
    else:
        conclusion = "sin_conclusion"
        certeza = ""
        alternativas = ""

    fila = {
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "respuestas": "; ".join("%s=%s" % (k, v) for k, v in respuestas.items()),
        "reglas_activadas": " ".join(a["id"] for a in resultado["activadas"]),
        "conclusion": conclusion,
        "certeza": certeza,
        "alternativas": alternativas,
    }

    try:
        escribir_encabezado = (not os.path.exists(ruta)
                               or os.path.getsize(ruta) == 0)
        with open(ruta, "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_HISTORIAL)
            if escribir_encabezado:
                escritor.writeheader()
            escritor.writerow(fila)
        return True
    except OSError as error:
        print(color("No se pudo guardar el historial (%s). "
                       "El programa continúa." % error, "error"))
        return False


# -----------------------------------------------------------------------------
# 5. PREGUNTAR AL USUARIO (con validación)
# -----------------------------------------------------------------------------

def leer_si_no(mensaje):
    """Pide una respuesta s/n hasta que sea válida. Devuelve "si" o "no".

    Acepta s / si / sí / n / no, sin importar mayúsculas.
    """
    while True:
        texto = input(mensaje).strip().lower()
        if texto in ("s", "si", "sí"):
            return "si"
        if texto in ("n", "no"):
            return "no"
        print(color("  Respuesta no válida. Escriba s (sí) o n (no).", "error"))


def preguntar(pregunta, numero=1, total=1):
    """Hace una pregunta de la lista PREGUNTAS y devuelve el valor interno.

    Muestra el progreso ("Pregunta 3 de 8") y repite la pregunta hasta
    recibir una respuesta válida:
      - tipo "menu": un número entre 1 y la cantidad de opciones;
      - tipo "sn":   s / si / sí / n / no (sin importar mayúsculas).
    Ctrl+C y fin de entrada (EOF) no se atrapan aquí: los maneja main().
    """
    print()
    print(color("Pregunta %d de %d" % (numero, total), "tenue"))
    for linea in ajustar(pregunta["texto"], 0):
        print(color(linea, "pregunta"))
    opciones = pregunta["opciones"]

    if pregunta["tipo"] == "sn":
        return leer_si_no("Responda s (sí) o n (no): ")

    # Pregunta de menú numerado: opciones alineadas con sangría de 2 espacios.
    for indice, (_, etiqueta) in enumerate(opciones, start=1):
        print("  " + color("%d." % indice, "opcion") + " " + etiqueta)
    while True:
        texto = input("Elija una opción: ").strip()
        if texto.isdigit() and 1 <= int(texto) <= len(opciones):
            return opciones[int(texto) - 1][0]
        print(color("  Opción no válida. Escriba un número del 1 al %d."
                    % len(opciones), "error"))


def hacer_consulta():
    """Recorre todas las preguntas y devuelve un diccionario {clave: valor}."""
    respuestas = {}
    for numero, pregunta in enumerate(PREGUNTAS, start=1):
        respuestas[pregunta["clave"]] = preguntar(pregunta, numero, len(PREGUNTAS))
    return respuestas


# -----------------------------------------------------------------------------
# 6. MOTOR DE INFERENCIA: ENCADENAMIENTO HACIA ADELANTE
# -----------------------------------------------------------------------------

def numero_regla(id_regla):
    """Convierte "R12" en 12 (sirve para desempatar y ordenar)."""
    return int(id_regla[1:])


def evaluar(respuestas, reglas):
    """Aplica las reglas a las respuestas con encadenamiento hacia adelante.

    Funcionamiento:
      1. Las respuestas del usuario se guardan como hechos con certeza 100.
      2. Se recorren las reglas en orden. Una regla se dispara si TODAS sus
         condiciones coinciden con hechos conocidos y aún no se ha disparado.
      3. Si una regla intermedia agrega un hecho nuevo, se vuelve a recorrer
         la lista, porque ese hecho puede activar otras reglas.
      4. Se termina al llegar a un punto fijo: una pasada completa sin que se
         dispare ninguna regla. Como cada regla se dispara una sola vez, el
         proceso siempre termina (no hay ciclos infinitos).

    Cálculo de certeza:
      - La certeza de lo que concluye una regla es el MÍNIMO entre la certeza
        de la regla y la certeza de cada hecho que usó como condición.
        Así, una cadena nunca es más segura que su eslabón más débil.
      - Si varias reglas llegan al mismo hecho o a la misma conclusión, se
        conserva la certeza MÁS ALTA.
      - Las conclusiones se ordenan de mayor a menor certeza. Si hay empate,
        va primero la que tiene el número de regla más bajo.

    Devuelve un diccionario con:
      "hechos":       {hecho: {"valor", "certeza", "origen"}}
      "activadas":    lista de reglas disparadas, en orden, con su cadena
      "conclusiones": lista ordenada de {"clave", "certeza", "reglas"}
    """
    # Hechos conocidos. "origen" dice si vino del usuario o de qué regla.
    hechos = {}
    for clave, valor in respuestas.items():
        hechos[clave] = {"valor": valor, "certeza": 100, "origen": "usuario"}

    disparadas = set()        # ID de reglas ya disparadas
    activadas = []            # detalle de cada disparo, para explicar()
    conclusiones = {}         # clave -> {"certeza", "reglas", "mejor_regla"}

    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for regla in reglas:
            if regla["id"] in disparadas:
                continue

            # ¿Se cumplen todas las condiciones?
            cumple = all(
                clave in hechos and hechos[clave]["valor"] == valor
                for clave, valor in regla["si"].items())
            if not cumple:
                continue

            # La regla se dispara (una sola vez).
            disparadas.add(regla["id"])
            hubo_cambio = True

            # Certeza encadenada = mínimo de la regla y de los hechos usados.
            certeza = regla["certeza"]
            usados = []
            for clave, valor in regla["si"].items():
                certeza = min(certeza, hechos[clave]["certeza"])
                usados.append((clave, valor, hechos[clave]["origen"]))

            clave_nueva, valor_nuevo = next(iter(regla["entonces"].items()))
            activadas.append({
                "id": regla["id"],
                "tipo": regla["tipo"],
                "condiciones": usados,
                "produce": (clave_nueva, valor_nuevo),
                "certeza": certeza,
            })

            if regla["tipo"] == "final":
                registro = conclusiones.setdefault(
                    valor_nuevo, {"certeza": -1, "reglas": [], "mejor_regla": None})
                registro["reglas"].append(regla["id"])
                # Se conserva la certeza más alta; en empate, la regla de menor número.
                if (certeza > registro["certeza"]
                        or (certeza == registro["certeza"]
                            and numero_regla(regla["id"])
                            < numero_regla(registro["mejor_regla"]))):
                    registro["certeza"] = certeza
                    registro["mejor_regla"] = regla["id"]
            else:
                actual = hechos.get(clave_nueva)
                if actual is None:
                    hechos[clave_nueva] = {"valor": valor_nuevo,
                                           "certeza": certeza,
                                           "origen": regla["id"]}
                elif actual["valor"] == valor_nuevo and certeza > actual["certeza"]:
                    # Mismo hecho por otra regla con más certeza: se actualiza.
                    actual["certeza"] = certeza
                    actual["origen"] = regla["id"]
                # Si el valor fuera distinto (contradicción), se conserva el
                # primero. La base de reglas está diseñada para que no ocurra.

    # Lista ordenada: mayor certeza primero; empate -> número de regla menor.
    lista = [
        {"clave": clave, "certeza": datos["certeza"], "reglas": datos["reglas"],
         "mejor_regla": datos["mejor_regla"]}
        for clave, datos in conclusiones.items()
    ]
    lista.sort(key=lambda c: (-c["certeza"], numero_regla(c["mejor_regla"])))

    return {"hechos": hechos, "activadas": activadas, "conclusiones": lista}


# -----------------------------------------------------------------------------
# 7. MOSTRAR EL RESULTADO Y EXPLICAR LA DECISIÓN (estilo MYCIN)
# -----------------------------------------------------------------------------
# Estas funciones solo ARMAN el texto (listas de líneas con segmentos
# (texto, rol)); no cambian nada de la evaluación. La consola y la ventana
# gráfica muestran exactamente el mismo contenido.

def linea_con_certeza(texto, certeza, rol):
    """Pone el texto a la izquierda y "certeza ████████░░ 80" a la derecha.

    Si no caben juntos en ANCHO caracteres, la barra baja a la línea siguiente.
    """
    cola = "certeza %s %3d" % (barra_certeza(certeza), certeza)
    if len(texto) + 2 + len(cola) <= ANCHO:
        relleno = " " * (ANCHO - len(texto) - len(cola))
        return [[(texto, rol), (relleno, None), (cola, "certeza")]]
    return [[(texto, rol)], [(" " * (ANCHO - len(cola)), None), (cola, "certeza")]]


def lineas_resultado(resultado):
    """Arma la recomendación principal y las alternativas ordenadas.

    Si ninguna regla final se activó, lo dice con calma, sin inventar: muestra
    qué respuestas se evaluaron y que ninguna regla las cubre.
    """
    lineas = [linea_separadora()]
    conclusiones = resultado["conclusiones"]

    if not conclusiones:
        lineas.append([("SIN CONCLUSIÓN", "titulo")])
        lineas += [[(t, None)] for t in ajustar(
            "Ninguna regla final cubre esta combinación de respuestas, así que "
            "el sistema no le dará una recomendación inventada. Es una "
            "limitación del sistema, no un error suyo.", 2)]
        lineas.append([])
        lineas.append([("  Respuestas que se evaluaron:", None)])
        for pregunta in PREGUNTAS:
            hecho = resultado["hechos"].get(pregunta["clave"])
            if hecho and hecho["origen"] == "usuario":
                etiqueta = dict(pregunta["opciones"])[hecho["valor"]]
                texto = "%s %s = %s (%s)" % (SIMBOLOS["punto"], pregunta["clave"],
                                             hecho["valor"], etiqueta)
                lineas += [[(t, None)] for t in ajustar(texto, 2, 4)]
        edad = resultado["hechos"].get("edad")
        if edad and edad["valor"] == "menor_18":
            lineas.append([])
            lineas += [[(t, None)] for t in ajustar(
                "Las reglas de este sistema solo tienen planes para personas de "
                "18 años o más.", 2)]
        lineas.append(linea_separadora())
        return lineas

    principal = conclusiones[0]
    datos = CONCLUSIONES[principal["clave"]]
    lineas.append([("RECOMENDACIÓN PRINCIPAL", "titulo")])
    lineas += linea_con_certeza("  " + datos["titulo"], principal["certeza"], "exito")
    lineas += [[(t, None)] for t in ajustar(datos["detalle"], 2)]

    if len(conclusiones) > 1:
        lineas.append([])
        lineas.append([("OTRAS OPCIONES (ordenadas por certeza)", "titulo")])
        for alternativa in conclusiones[1:]:
            datos = CONCLUSIONES[alternativa["clave"]]
            lineas += linea_con_certeza("  %s %s" % (SIMBOLOS["punto"], datos["titulo"]),
                                        alternativa["certeza"], None)
            lineas += [[(t, "tenue")] for t in ajustar(datos["detalle"], 4)]
    lineas.append(linea_separadora())
    return lineas


def texto_condicion(clave, valor, origen):
    """Arma el texto de una condición, indicando de dónde salió el hecho."""
    if origen == "usuario":
        return "%s = %s" % (clave, valor)
    return "%s = %s [deducido por %s]" % (clave, valor, origen)


def lineas_explicacion(resultado):
    """Arma la explicación al estilo MYCIN, como un árbol.

    1. Cada regla que se activó, en orden: "Se activó R# porque: ..." y, debajo,
       lo que produjo (hecho intermedio o recomendación) con su certeza.
    2. La cadena de hechos intermedios: qué regla produjo cada hecho y qué
       reglas lo usaron después.
    """
    activadas = resultado["activadas"]
    lineas = [[("¿POR QUÉ?", "titulo"),
               ("  reglas que se activaron, en orden", "tenue")]]
    if not activadas:
        lineas.append([("  No se activó ninguna regla.", None)])
        return lineas

    for numero, activada in enumerate(activadas):
        es_ultima = numero == len(activadas) - 1
        rama = "  " + (SIMBOLOS["ultima"] if es_ultima else SIMBOLOS["rama"]) + " "
        tronco = "  " + ("  " if es_ultima else SIMBOLOS["tronco"]) + " "

        # Línea "Se activó R# porque: ..." (puede ocupar varias líneas).
        condiciones = " y ".join(texto_condicion(c, v, o)
                                 for c, v, o in activada["condiciones"])
        texto = "Se activó %s porque: %s" % (activada["id"], condiciones)
        for linea in ajustar(texto, rama, tronco + "    "):
            ancho_prefijo = len(rama) if linea.startswith(rama) else len(tronco)
            lineas.append([(linea[:ancho_prefijo], "tenue"), (linea[ancho_prefijo:], None)])

        # Línea de lo que produjo la regla, con la certeza alineada a la derecha.
        clave, valor = activada["produce"]
        if activada["tipo"] == "final":
            produce = "recomienda: %s" % CONCLUSIONES[valor]["titulo"]
            rol = "exito"
        else:
            produce = "hecho intermedio: %s = %s" % (clave, valor)
            rol = None
        certeza = "(certeza %d)" % activada["certeza"]
        partes = ajustar("%s %s" % (SIMBOLOS["flecha"], produce),
                         tronco + "    ", tronco + "      ")
        for linea in partes[:-1]:
            lineas.append([(tronco, "tenue"), (linea[len(tronco):], rol)])
        ultima = partes[-1]
        if len(ultima) + 2 + len(certeza) <= ANCHO:
            relleno = " " * (ANCHO - len(ultima) - len(certeza))
            lineas.append([(tronco, "tenue"), (ultima[len(tronco):], rol),
                           (relleno, None), (certeza, "certeza")])
        else:
            lineas.append([(tronco, "tenue"), (ultima[len(tronco):], rol)])
            relleno = " " * (ANCHO - len(tronco) - len(certeza))
            lineas.append([(tronco, "tenue"), (relleno, None), (certeza, "certeza")])

    # Cadena de encadenamiento: hechos intermedios, quién los produjo y quién los usó.
    intermedias = [a for a in activadas if a["tipo"] == "intermedia"]
    if intermedias:
        lineas.append([])
        lineas.append([("CADENA DE RAZONAMIENTO", "titulo"),
                       ("  hechos intermedios encadenados", "tenue")])
        vistos = []
        for activada in intermedias:
            if activada["produce"] not in vistos:
                vistos.append(activada["produce"])
        for clave, valor in vistos:
            productoras = [a["id"] for a in intermedias if a["produce"] == (clave, valor)]
            usuarias = [a["id"] for a in activadas
                        if any(c == clave for c, _, _ in a["condiciones"])]
            usado = ", ".join(usuarias) if usuarias else "ninguna regla"
            texto = "%s %s = %s: lo produjo %s; lo usó %s" % (
                SIMBOLOS["punto"], clave, valor, ", ".join(productoras), usado)
            lineas += [[(t, None)] for t in ajustar(texto, 2, 4)]
    lineas.append([])
    lineas += [[(t, "tenue")] for t in ajustar(
        "Certeza: la de una cadena es el mínimo de sus eslabones; si varias "
        "reglas llegan a lo mismo, se toma la más alta.", 0)]
    return lineas


def mostrar_resultado(resultado):
    """Muestra en la consola la recomendación principal y las alternativas."""
    print()
    imprimir_lineas(lineas_resultado(resultado))


def explicar(resultado):
    """Muestra en la consola la explicación de la decisión (estilo MYCIN)."""
    print()
    imprimir_lineas(lineas_explicacion(resultado))


# -----------------------------------------------------------------------------
# 8. CASOS DE PRUEBA (modo: python arce_daniela_tarea1.py --pruebas)
# -----------------------------------------------------------------------------
# Cada caso tiene las respuestas (como hechos) y el resultado esperado: una
# lista de (conclusión, certeza) en el orden en que deben aparecer.
# Las teclas exactas que se escriben en la consulta interactiva se calculan con
# respuestas_a_teclas() y se imprimen al ejecutar las pruebas.

CASOS_PRUEBA = [
    {"nombre": "1. Salud general, adulto sin restricciones",
     "respuestas": {"edad": "18_64", "condicion_cronica": "no", "molestias": "no",
                    "nivel": "intermedio", "objetivo": "salud_general",
                    "minutos": "20_40", "dias": "5_mas", "equipo": "ninguno"},
     "esperado": [("plan_salud_general", 90)]},
    {"nombre": "2. Control de peso, principiante con buen tiempo",
     "respuestas": {"edad": "18_64", "condicion_cronica": "no", "molestias": "no",
                    "nivel": "principiante", "objetivo": "control_peso",
                    "minutos": "mas_40", "dias": "5_mas", "equipo": "ninguno"},
     "esperado": [("plan_control_peso", 85)]},
    # R21 tiene certeza 90, pero la cadena pasa por R16 (certeza 85): mínimo = 85.
    {"nombre": "3. Fuerza con máquinas, avanzado",
     "respuestas": {"edad": "18_64", "condicion_cronica": "no", "molestias": "no",
                    "nivel": "avanzado", "objetivo": "fuerza",
                    "minutos": "mas_40", "dias": "3_4", "equipo": "maquinas"},
     "esperado": [("plan_fuerza_cargas", 85)]},
    {"nombre": "4. Fuerza sin equipo (certeza limitada por R7)",
     "respuestas": {"edad": "18_64", "condicion_cronica": "no", "molestias": "no",
                    "nivel": "intermedio", "objetivo": "fuerza",
                    "minutos": "20_40", "dias": "3_4", "equipo": "ninguno"},
     "esperado": [("plan_fuerza_peso_corporal", 80)]},
    {"nombre": "5. Resistencia, principiante",
     "respuestas": {"edad": "18_64", "condicion_cronica": "no", "molestias": "no",
                    "nivel": "principiante", "objetivo": "resistencia",
                    "minutos": "20_40", "dias": "5_mas", "equipo": "bandas_mancuernas"},
     "esperado": [("plan_aerobico_progresivo", 90)]},
    {"nombre": "6. Resistencia, avanzado",
     "respuestas": {"edad": "18_64", "condicion_cronica": "no", "molestias": "no",
                    "nivel": "avanzado", "objetivo": "resistencia",
                    "minutos": "mas_40", "dias": "5_mas", "equipo": "ninguno"},
     "esperado": [("plan_aerobico_vigoroso", 85)]},
    {"nombre": "7. Seguridad: 65+, principiante, con molestias (encadenamiento)",
     "respuestas": {"edad": "65_mas", "condicion_cronica": "no", "molestias": "si",
                    "nivel": "principiante", "objetivo": "salud_general",
                    "minutos": "20_40", "dias": "3_4", "equipo": "ninguno"},
     "esperado": [("plan_adulto_mayor", 90), ("plan_bajo_impacto", 85),
                  ("consultar_profesional", 75)]},
    {"nombre": "8. Enfermedad crónica y poco tiempo (varias conclusiones)",
     "respuestas": {"edad": "18_64", "condicion_cronica": "si", "molestias": "no",
                    "nivel": "intermedio", "objetivo": "control_peso",
                    "minutos": "menos_20", "dias": "1_2", "equipo": "bandas_mancuernas"},
     "esperado": [("consultar_profesional", 95), ("plan_bloques_cortos", 80)]},
    {"nombre": "9. Adulto con molestias articulares",
     "respuestas": {"edad": "18_64", "condicion_cronica": "no", "molestias": "si",
                    "nivel": "intermedio", "objetivo": "salud_general",
                    "minutos": "mas_40", "dias": "3_4", "equipo": "ninguno"},
     "esperado": [("plan_bajo_impacto", 85)]},
    {"nombre": "10. Menor de edad: sin conclusión",
     "respuestas": {"edad": "menor_18", "condicion_cronica": "no", "molestias": "no",
                    "nivel": "intermedio", "objetivo": "resistencia",
                    "minutos": "20_40", "dias": "3_4", "equipo": "ninguno"},
     "esperado": []},
]


def respuestas_a_teclas(respuestas):
    """Traduce las respuestas a lo que se teclea en cada pregunta (1, 2, s, n...)."""
    teclas = []
    for pregunta in PREGUNTAS:
        valor = respuestas[pregunta["clave"]]
        if pregunta["tipo"] == "sn":
            teclas.append("s" if valor == "si" else "n")
        else:
            valores = [v for v, _ in pregunta["opciones"]]
            teclas.append(str(valores.index(valor) + 1))
    return teclas


def ejecutar_pruebas():
    """Ejecuta los casos de prueba sin pedir datos y sin escribir el historial.

    Inyecta las respuestas como hechos, llama a evaluar() y compara las
    conclusiones (y su orden y certeza) con lo esperado.
    Devuelve 0 si todos pasan y 1 si alguno falla (código de salida).
    """
    print(color("Ejecutando %d casos de prueba..." % len(CASOS_PRUEBA), "titulo"))
    aprobados = 0
    for caso in CASOS_PRUEBA:
        resultado = evaluar(caso["respuestas"], REGLAS)
        obtenido = [(c["clave"], c["certeza"]) for c in resultado["conclusiones"]]
        pasa = obtenido == caso["esperado"]
        if pasa:
            aprobados += 1
        estado = color("PASA ", "exito") if pasa else color("FALLA", "error")
        print()
        print("[%s] %s" % (estado, caso["nombre"]))
        print("   Teclas:   %s" % " ".join(respuestas_a_teclas(caso["respuestas"])))
        print("   Reglas:   %s" % " ".join(a["id"] for a in resultado["activadas"]))
        print("   Esperado: %s" % (caso["esperado"] or "sin conclusión"))
        print("   Obtenido: %s" % (obtenido or "sin conclusión"))

    print()
    resumen = "Resumen: %d de %d casos pasan." % (aprobados, len(CASOS_PRUEBA))
    todos = aprobados == len(CASOS_PRUEBA)
    print(color(resumen, "exito" if todos else "error"))
    return 0 if todos else 1


# -----------------------------------------------------------------------------
# 9. INTERFAZ GRÁFICA (modo: python arce_daniela_tarea1.py --gui)
# -----------------------------------------------------------------------------
# Ventana sencilla hecha con tkinter, que viene incluido con Python (biblioteca
# estándar). Usa los mismos datos (PREGUNTAS, REGLAS) y las mismas funciones
# (evaluar, lineas_resultado, lineas_explicacion, guardar_historial) que la
# consola: solo cambia la forma de preguntar y de mostrar.

# Colores de la ventana (formato hexadecimal).
COLORES_GUI = {
    "fondo": "#f4f6f8",
    "aviso_fondo": "#fff4ce",
    "aviso_texto": "#5c4400",
    "titulo": "#0b5c75",
    "exito": "#1b6e2d",
    "certeza": "#8a6100",
    "opcion": "#0b5c75",
    "error": "#b3261e",
    "tenue": "#666666",
    "boton": "#0b5c75",
}


class VentanaRecomendador:
    """Ventana que hace las preguntas una por una y luego muestra el resultado."""

    def __init__(self, tk, raiz):
        # tk es el módulo tkinter; raiz es la ventana principal.
        self.tk = tk
        self.raiz = raiz
        self.respuestas = {}
        self.indice = 0                      # número de la pregunta actual
        self.seleccion = tk.StringVar()      # opción marcada en pantalla

        raiz.title("Recomendador de rutina de ejercicio")
        raiz.geometry("800x640")
        raiz.minsize(640, 520)
        raiz.configure(bg=COLORES_GUI["fondo"])

        # Aviso de salud fijo en la parte superior (visible siempre).
        tk.Label(raiz, text="AVISO DE SALUD: " + AVISO_SALUD, wraplength=760,
                 justify="left", bg=COLORES_GUI["aviso_fondo"],
                 fg=COLORES_GUI["aviso_texto"], font=("Helvetica", 10, "bold"),
                 padx=12, pady=8).pack(fill="x")

        # Zona central que se vuelve a dibujar en cada pantalla.
        self.contenido = tk.Frame(raiz, bg=COLORES_GUI["fondo"], padx=24, pady=16)
        self.contenido.pack(fill="both", expand=True)

        # Atajos de teclado: Enter avanza y los números marcan una opción.
        raiz.bind("<Return>", lambda evento: self.siguiente())
        for numero in range(1, 10):
            raiz.bind(str(numero), self.marcar_con_numero)

        self.mostrar_pregunta()

    def limpiar(self):
        """Borra lo que hay en la zona central."""
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def boton(self, padre, texto, accion):
        """Crea un botón con el estilo de la aplicación."""
        return self.tk.Button(padre, text=texto, command=accion, width=18,
                              bg=COLORES_GUI["boton"], fg="white",
                              activebackground=COLORES_GUI["titulo"],
                              activeforeground="white", font=("Helvetica", 11, "bold"),
                              relief="flat", padx=8, pady=6)

    # --- Pantalla de preguntas ------------------------------------------------

    def mostrar_pregunta(self):
        """Dibuja la pregunta actual con sus opciones como botones de radio."""
        tk = self.tk
        self.limpiar()
        self.en_resultados = False
        pregunta = PREGUNTAS[self.indice]
        # Si ya se había respondido (al volver atrás), se deja marcada.
        self.seleccion.set(self.respuestas.get(pregunta["clave"], ""))

        tk.Label(self.contenido, text="SISTEMA EXPERTO: RECOMENDADOR DE RUTINA DE EJERCICIO",
                 bg=COLORES_GUI["fondo"], fg=COLORES_GUI["titulo"],
                 font=("Helvetica", 14, "bold")).pack(anchor="w")
        tk.Label(self.contenido, text="Pregunta %d de %d" % (self.indice + 1, len(PREGUNTAS)),
                 bg=COLORES_GUI["fondo"], fg=COLORES_GUI["tenue"],
                 font=("Helvetica", 10)).pack(anchor="w", pady=(4, 12))
        tk.Label(self.contenido, text=pregunta["texto"].replace("\n", " "),
                 wraplength=720, justify="left", bg=COLORES_GUI["fondo"],
                 font=("Helvetica", 13, "bold")).pack(anchor="w", pady=(0, 10))

        for numero, (valor, etiqueta) in enumerate(pregunta["opciones"], start=1):
            tk.Radiobutton(self.contenido, text="%d. %s" % (numero, etiqueta),
                           variable=self.seleccion, value=valor,
                           bg=COLORES_GUI["fondo"], activebackground=COLORES_GUI["fondo"],
                           font=("Helvetica", 12), anchor="w").pack(fill="x", pady=2)

        # Mensaje de validación (vacío hasta que haga falta).
        self.mensaje_error = tk.Label(self.contenido, text="", bg=COLORES_GUI["fondo"],
                                      fg=COLORES_GUI["error"], font=("Helvetica", 11))
        self.mensaje_error.pack(anchor="w", pady=(10, 0))

        botones = tk.Frame(self.contenido, bg=COLORES_GUI["fondo"])
        botones.pack(side="bottom", fill="x", pady=8)
        if self.indice > 0:
            self.boton(botones, "< Atrás", self.atras).pack(side="left")
        ultima = self.indice == len(PREGUNTAS) - 1
        self.boton(botones, "Ver recomendación" if ultima else "Siguiente >",
                   self.siguiente).pack(side="right")

    def marcar_con_numero(self, evento):
        """Permite elegir una opción tecleando su número."""
        if self.en_resultados:
            return
        opciones = PREGUNTAS[self.indice]["opciones"]
        numero = int(evento.char)
        if 1 <= numero <= len(opciones):
            self.seleccion.set(opciones[numero - 1][0])

    def siguiente(self):
        """Valida la respuesta y pasa a la siguiente pregunta o al resultado."""
        if self.en_resultados:
            return
        valor = self.seleccion.get()
        if not valor:
            # Validación: no se avanza sin elegir una opción.
            self.mensaje_error.config(text="Seleccione una opción para continuar.")
            return
        self.respuestas[PREGUNTAS[self.indice]["clave"]] = valor
        if self.indice < len(PREGUNTAS) - 1:
            self.indice += 1
            self.mostrar_pregunta()
        else:
            self.mostrar_resultados()

    def atras(self):
        """Vuelve a la pregunta anterior conservando las respuestas."""
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_pregunta()

    # --- Pantalla de resultados -----------------------------------------------

    def mostrar_resultados(self):
        """Evalúa las reglas, muestra recomendación y explicación, y guarda."""
        tk = self.tk
        self.limpiar()
        self.en_resultados = True

        # Se copian las respuestas en el orden de las preguntas.
        respuestas = {p["clave"]: self.respuestas[p["clave"]] for p in PREGUNTAS}
        resultado = evaluar(respuestas, REGLAS)

        # Cuadro de texto con barra de desplazamiento.
        marco = tk.Frame(self.contenido, bg=COLORES_GUI["fondo"])
        marco.pack(fill="both", expand=True)
        barra = tk.Scrollbar(marco)
        barra.pack(side="right", fill="y")
        texto = tk.Text(marco, wrap="word", font=("Courier", 10), padx=10, pady=10,
                        yscrollcommand=barra.set, relief="flat")
        texto.pack(side="left", fill="both", expand=True)
        barra.config(command=texto.yview)

        # Etiquetas de formato equivalentes a los colores de la consola.
        texto.tag_configure("titulo", foreground=COLORES_GUI["titulo"],
                            font=("Courier", 10, "bold"))
        texto.tag_configure("exito", foreground=COLORES_GUI["exito"],
                            font=("Courier", 10, "bold"))
        texto.tag_configure("certeza", foreground=COLORES_GUI["certeza"])
        texto.tag_configure("error", foreground=COLORES_GUI["error"],
                            font=("Courier", 11, "bold"))
        texto.tag_configure("tenue", foreground=COLORES_GUI["tenue"])
        texto.tag_configure("aviso", foreground=COLORES_GUI["aviso_texto"],
                            background=COLORES_GUI["aviso_fondo"])

        lineas = lineas_resultado(resultado) + [[]] + lineas_explicacion(resultado)
        lineas += [[]] + lineas_aviso()          # aviso al final de la consulta
        for segmentos in lineas:
            for parte, rol in segmentos:
                texto.insert("end", parte, rol or ())
            texto.insert("end", "\n")
        texto.config(state="disabled")                  # solo lectura

        # Historial: si falla, se avisa en la ventana y se sigue.
        if guardar_historial(respuestas, resultado):
            estado, rol_estado = "Consulta guardada en %s." % ARCHIVO_HISTORIAL, "tenue"
        else:
            estado, rol_estado = "No se pudo guardar el historial.", "error"
        tk.Label(self.contenido, text=estado, bg=COLORES_GUI["fondo"],
                 fg=COLORES_GUI[rol_estado], font=("Helvetica", 10)).pack(anchor="w", pady=(6, 0))

        # Equivalente de "¿Desea hacer otra consulta? (s/n)".
        pie = tk.Frame(self.contenido, bg=COLORES_GUI["fondo"])
        pie.pack(fill="x", pady=8)
        tk.Label(pie, text="¿Desea hacer otra consulta?", bg=COLORES_GUI["fondo"],
                 font=("Helvetica", 12, "bold")).pack(side="left")
        self.boton(pie, "No, salir", self.raiz.destroy).pack(side="right")
        self.boton(pie, "Sí, otra consulta", self.nueva_consulta).pack(side="right", padx=8)

    def nueva_consulta(self):
        """Borra las respuestas y empieza de nuevo desde la primera pregunta."""
        self.respuestas = {}
        self.indice = 0
        self.mostrar_pregunta()


def iniciar_interfaz_grafica():
    """Abre la ventana. Devuelve False si tkinter o la pantalla no están disponibles.

    tkinter se importa AQUÍ y no al inicio del archivo: así el modo terminal
    y el modo --pruebas funcionan aunque este Python no traiga tkinter.
    """
    try:
        import tkinter
    except ImportError:
        print("No se pudo abrir la interfaz gráfica: este Python no incluye tkinter.")
        print("Si la necesita, instale Python desde python.org (ya trae tkinter).")
        return False
    try:
        raiz = tkinter.Tk()
    except tkinter.TclError as error:
        # Pasa, por ejemplo, en un servidor sin pantalla gráfica.
        print("No se pudo abrir la interfaz gráfica: no hay una pantalla "
              "disponible (%s)." % error)
        return False
    VentanaRecomendador(tkinter, raiz)
    try:
        raiz.mainloop()
    except KeyboardInterrupt:
        print("Consulta cancelada. ¡Hasta pronto!")
    return True


# -----------------------------------------------------------------------------
# 10. PROGRAMA PRINCIPAL
# -----------------------------------------------------------------------------

def modo_consola():
    """Ciclo de la consola: aviso, preguntas, evaluación, explicación e historial."""
    try:
        print(color("SISTEMA EXPERTO %s RECOMENDADOR DE RUTINA DE EJERCICIO"
                    % SIMBOLOS["punto"], "titulo"))
        while True:
            mostrar_aviso()
            respuestas = hacer_consulta()
            resultado = evaluar(respuestas, REGLAS)
            mostrar_resultado(resultado)
            explicar(resultado)
            if guardar_historial(respuestas, resultado):
                print(color("Consulta guardada en %s." % ARCHIVO_HISTORIAL, "tenue"))
            print()
            mostrar_aviso()
            print()
            if leer_si_no("¿Desea hacer otra consulta? (s/n): ") == "no":
                break
            print()
        print("Gracias por usar el sistema. ¡Hasta pronto!")
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C o fin de entrada: se sale con un mensaje, sin traceback.
        print()
        print("Consulta cancelada. ¡Hasta pronto!")


def main():
    """Elige el modo según la opción de la línea de comandos."""
    global USAR_COLORES
    # Si la salida no admite algún carácter (por ejemplo, al redirigir a un
    # archivo en Windows), se reemplaza por "?" en vez de detener el programa.
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

    argumentos = sys.argv[1:]
    if "--pruebas" in argumentos:
        # Las pruebas se imprimen siempre sin colores (salida comparable).
        USAR_COLORES = False
        sys.exit(ejecutar_pruebas())
    if "--gui" in argumentos:
        if iniciar_interfaz_grafica():
            return
        print("El programa continúa en modo terminal.")
        print()
    modo_consola()


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # La salida se cerró antes de tiempo (por ejemplo, "... | head").
        # Se redirige a os.devnull para terminar sin mostrar un traceback.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(1)
