# Parser CYK - Proyecto 2
## Teoría de la Computación 2025

Implementación del algoritmo CYK (Cocke-Younger-Kasami) para parsing de gramáticas libres de contexto con conversión automática a Forma Normal de Chomsky (CNF).

---

## 📋 Descripción

Este proyecto implementa un parser sintáctico para oraciones simples en inglés utilizando:
- **Conversión a CNF**: Transforma gramáticas CFG a Forma Normal de Chomsky
- **Algoritmo CYK**: Parsing eficiente usando programación dinámica
- **Construcción de Parse Trees**: Genera árboles de parsing visuales

---

## 🚀 Instalación

### Requisitos previos
- Python 3.7 o superior

### Pasos de instalación

```bash
# 1. Clonar o crear el directorio del proyecto
mkdir proyecto2-tc
cd proyecto2-tc

# 2. Crear ambiente virtual
python -m venv venv

# 3. Activar ambiente virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

```

---

## 📁 Estructura del Proyecto

```
cyk_parser/
│
├── src/
│   ├── __init__.py           # Inicializador del paquete
│   ├── grammar.py            # Definición de gramáticas
│   ├── cnf_converter.py      # Conversión a CNF
│   ├── cyk_algorithm.py      # Algoritmo CYK
│   └── parse_tree.py         # Construcción de árboles
│
├── main.py                   # Programa principal
├── requirements.txt          # Dependencias
└── README.md                 # Esta documentación
```

---

## 🎮 Uso

### Ejecutar el programa principal

```bash
python main.py
```

### Menú de opciones

El programa ofrece las siguientes opciones:

1. **Mostrar gramática original** - Visualiza las reglas de la gramática CFG
2. **Mostrar gramática en CNF** - Muestra la conversión a Forma Normal de Chomsky
3. **Parsear una oración** - Modo interactivo para ingresar oraciones
4. **Probar ejemplos predefinidos** - Ejecuta los 6 ejemplos requeridos
5. **Salir** - Termina el programa

---

## 🗃️ Generar informe técnico

Se ha incluido una utilidad para generar automáticamente un informe técnico en formato Markdown: `generate_report.py`.

Qué hace:
- Ejecuta conversiones, pruebas y genera un documento completo `INFORME_TECNICO.md` con:
    - Portada y datos de integrantes
    - Gramática original y gramática convertida a CNF
    - Resultados de pruebas (aceptadas/rechazadas), tablas CYK y árboles de parsing
    - Análisis estadístico y conclusiones

Requisitos:
- Python 3.7+
- Tener el proyecto en el directorio raíz (las importaciones usan `src.*`).

Uso rápido:

```powershell
# Desde el directorio del proyecto (Windows PowerShell)
python generate_report.py
```

Salida:
- Archivo: `INFORME_TECNICO.md` (Markdown) creado/reescrito en el directorio raíz.
- Incluye visualización ASCII de los árboles y tablas CYK.

Notas:
- El script abre y escribe archivos con `encoding='utf-8'` para compatibilidad en Windows.
- Si deseas generar el informe con un subconjunto de pruebas o modificar la información de los integrantes, edita `generate_report.py`.


## 🗄️ Gramática

El proyecto utiliza la siguiente gramática para oraciones simples en inglés:

```
S → NP VP
VP → VP PP | V NP | cooks | drinks | eats | cuts
PP → P NP
NP → Det N | he | she
V → cooks | drinks | eats | cuts
P → in | with
N → cat | dog | beer | cake | juice | meat | soup | fork | knife | oven | spoon
Det → a | the
```

---

## 🧪 Ejemplos de Uso

### Ejemplos semánticamente correctos (aceptadas)
```
✓ "she eats a cake"
✓ "the dog drinks the beer"
```

### Ejemplos sintácticamente correctos pero semánticamente incorrectos (aceptadas)
```
✓ "the fork eats the oven"
✓ "he drinks a knife"
```

### Ejemplos no aceptados por la gramática (rechazadas)
```
✗ "she eats"           # Falta objeto directo
✗ "eats she cake"      # Orden incorrecto
```

---

## 🔧 Módulos

### 1. `grammar.py`
Define la clase `Grammar` para representar gramáticas libres de contexto.

**Funciones principales:**
- `create_english_grammar()`: Crea la gramática del proyecto

### 2. `cnf_converter.py`
Convierte gramáticas CFG a Forma Normal de Chomsky.

**Pasos de conversión:**
1. Eliminar producciones unitarias (A → B)
2. Convertir terminales en producciones mixtas
3. Romper producciones largas (más de 2 símbolos)

**Clase principal:**
- `CNFConverter`: Realiza la conversión completa

### 3. `cyk_algorithm.py`
Implementa el algoritmo CYK para parsing.

**Clase principal:**
- `CYKParser`: Ejecuta el algoritmo de programación dinámica

**Métodos importantes:**
- `parse(sentence)`: Verifica si una oración es aceptada
- `print_table(words)`: Muestra la tabla CYK
- `get_parse_explanation(words)`: Genera explicación paso a paso

### 4. `parse_tree.py`
Construye y visualiza árboles de parsing.

**Clases principales:**
- `ParseTreeNode`: Representa un nodo del árbol
- `ParseTreeBuilder`: Construye árboles desde backpointers

**Métodos de visualización:**
- `print_tree()`: Visualización jerárquica
- `to_bracket_notation()`: Notación de brackets `[S [NP she] [VP ...]]`
- `visualize_tree_ascii()`: Visualización ASCII avanzada

---

## ⚙️ Algoritmo CYK

### Funcionamiento

El algoritmo CYK utiliza **programación dinámica** para construir una tabla triangular:

```
Para una oración de n palabras:
- Tabla[i][j] contiene las variables que pueden derivar 
  la subcadena desde posición i con longitud j+1
```

### Pasos:

1. **Inicialización**: Llenar tabla con palabras individuales
2. **Construcción bottom-up**: Combinar subcadenas más pequeñas
3. **Verificación**: Si S está en Tabla[0][n-1], la oración es aceptada

### Complejidad

- **Tiempo**: O(n³ × |G|) donde n es longitud de la oración y |G| es tamaño de la gramática
- **Espacio**: O(n²)

---

## 📊 Salida del Programa

### Información proporcionada:

1. **Resultado de aceptación**: SI o NO
2. **Tiempo de ejecución**: En milisegundos
3. **Tabla CYK**: Visualización de la tabla de programación dinámica
4. **Explicación paso a paso**: Proceso de parsing detallado
5. **Árbol de parsing**: Representación visual (si es aceptada)

### Ejemplo de salida:

```
======================================================================
PARSEANDO: 'she eats a cake'
======================================================================

✓ ACEPTADA
Tiempo de ejecución: 2.3456 ms

============================================================
TABLA CYK
============================================================

Palabras: she eats a cake

Longitud 4: {S}
Longitud 3:  {VP}
Longitud 2:   {VP} {NP}
Longitud 1: {NP} {V,VP} {Det} {N}

======================================================================
ÁRBOL DE PARSING
======================================================================

S
├── NP
│   └── she
└── VP
    ├── V
    │   └── eats
    └── NP
        ├── Det
        │   └── a
        └── N
            └── cake
```

---

## 🧠 Conceptos Teóricos

### Forma Normal de Chomsky (CNF)

Todas las producciones deben ser:
- `A → BC` (dos variables)
- `A → a` (un terminal)

**Ventajas:**
- Simplifica el parsing
- Permite uso eficiente de programación dinámica
- Facilita análisis de complejidad

### Programación Dinámica

El CYK usa programación dinámica para:
- Evitar recálculos de subcadenas
- Construir soluciones de abajo hacia arriba
- Garantizar complejidad polinomial

---

## 📚 Referencias

- [Wikipedia: CYK Algorithm](https://en.wikipedia.org/wiki/CYK_algorithm)
- [GeeksforGeeks: CYK Algorithm](https://www.geeksforgeeks.org/cyk-algorithm-for-context-free-grammar/)
- [CFG to CNF Converter](https://devimam.github.io/cfgtocnf/)
- [UC Davis: CYK PDF](https://web.cs.ucdavis.edu/~rogaway/classes/120/winter12/CYK.pdf)

---

## 👨‍💻 Desarrollo

### Extender la gramática

Para añadir nuevas reglas, modificar `create_english_grammar()` en `grammar.py`:

```python
productions = {
    'S': [('NP', 'VP')],
    'NP': [('Det', 'N'), 'he', 'she', 'it'],  # Añadir 'it'
    # ... más producciones
}
```

### Probar módulos individuales

Cada módulo puede ejecutarse independientemente:

```bash
python -m src.grammar
python -m src.cnf_converter
python -m src.cyk_algorithm
python -m src.parse_tree
```
