"""
Programa principal para el Proyecto 2 - Parser CYK
Teoría de la Computación 2025

Implementa conversión a CNF y algoritmo CYK para parsing de oraciones
"""

from src.grammar import create_english_grammar
from src.cnf_converter import CNFConverter
from src.cyk_algorithm import CYKParser
from src.parse_tree import ParseTreeBuilder


def print_header():
    """Imprime el encabezado del programa"""
    print("\n" + "="*70)
    print(" "*15 + "PARSER CYK - PROYECTO 2")
    print(" "*10 + "Teoría de la Computación 2025")
    print("="*70 + "\n")


def print_menu():
    """Imprime el menú de opciones"""
    print("\n" + "-"*70)
    print("OPCIONES:")
    print("  1. Mostrar gramática original")
    print("  2. Mostrar gramática en CNF")
    print("  3. Parsear una oración")
    print("  4. Probar ejemplos predefinidos")
    print("  5. Salir")
    print("-"*70)


def show_original_grammar(grammar):
    """Muestra la gramática original"""
    print("\n" + "="*70)
    print("GRAMÁTICA ORIGINAL")
    print("="*70)
    print(grammar)


def show_cnf_grammar(cnf_grammar):
    """Muestra la gramática en CNF"""
    print("\n" + "="*70)
    print("GRAMÁTICA EN FORMA NORMAL DE CHOMSKY (CNF)")
    print("="*70)
    print(cnf_grammar)


def parse_sentence(sentence, parser, show_details=True):
    """
    Parsea una oración y muestra resultados
    
    Args:
        sentence: string con la oración
        parser: objeto CYKParser
        show_details: si mostrar detalles del proceso
    """
    print("\n" + "="*70)
    print(f"PARSEANDO: '{sentence}'")
    print("="*70)
    
    # Ejecutar CYK
    accepted, time_taken, _ = parser.parse(sentence)
    
    words = sentence.lower().split()
    
    # Mostrar resultado
    print(f"\n{'✓ ACEPTADA' if accepted else '✗ RECHAZADA'}")
    print(f"Tiempo de ejecución: {time_taken*1000:.4f} ms")
    
    if show_details:
        # Mostrar tabla CYK
        parser.print_table(words)
        
        # Mostrar explicación
        explanation = parser.get_parse_explanation(words)
        print(explanation)
    
    # Si fue aceptada, construir árbol
    if accepted:
        print("\n" + "="*70)
        print("ÁRBOL DE PARSING")
        print("="*70)
        
        builder = ParseTreeBuilder(parser)
        tree = builder.build_tree(words)
        
        print("\nVisualización jerárquica:")
        print(builder.visualize_tree_ascii(tree))
        
        print("\nNotación de brackets:")
        print(builder.to_bracket_notation(tree))
    
    return accepted


def test_predefined_examples(parser):
    """
    Prueba los ejemplos requeridos en el proyecto
    """
    print("\n" + "="*70)
    print("EJEMPLOS PREDEFINIDOS - PRUEBAS")
    print("="*70)
    
    examples = {
        "Semánticamente correctas (2 ejemplos)": [
            "she eats a cake",
            "the dog drinks the beer"
        ],
        "Sintácticamente correctas pero semánticamente incorrectas (2 ejemplos)": [
            "the fork eats the oven",
            "he drinks a knife"
        ],
        "No aceptadas por la gramática (2 ejemplos)": [
            "she eats",  # Falta objeto
            "eats she cake"  # Orden incorrecto
        ]
    }
    
    results = []
    
    for category, sentences in examples.items():
        print(f"\n{'─'*70}")
        print(f"{category}:")
        print('─'*70)
        
        for sentence in sentences:
            print(f"\n  → '{sentence}'")
            accepted, time_taken, _ = parser.parse(sentence)
            result = "✓ ACEPTADA" if accepted else "✗ RECHAZADA"
            print(f"     {result} ({time_taken*1000:.4f} ms)")
            
            results.append({
                'sentence': sentence,
                'category': category,
                'accepted': accepted,
                'time': time_taken
            })
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS")
    print("="*70)
    print(f"\nTotal de pruebas: {len(results)}")
    print(f"Aceptadas: {sum(1 for r in results if r['accepted'])}")
    print(f"Rechazadas: {sum(1 for r in results if not r['accepted'])}")
    print(f"Tiempo promedio: {sum(r['time'] for r in results)/len(results)*1000:.4f} ms")


def interactive_mode(parser):
    """Modo interactivo para parsear oraciones"""
    print("\n" + "="*70)
    print("MODO INTERACTIVO")
    print("="*70)
    print("\nIngresa oraciones para parsear (escribe 'salir' para terminar)")
    print("Ejemplo: she eats a cake with a fork")
    
    while True:
        print("\n" + "-"*70)
        sentence = input("Oración: ").strip()
        
        if sentence.lower() in ['salir', 'exit', 'quit', '']:
            break
        
        parse_sentence(sentence, parser, show_details=True)


def main():
    """Función principal"""
    print_header()
    
    # Paso 1: Crear gramática original
    print("Cargando gramática...")
    original_grammar = create_english_grammar()
    
    # Paso 2: Convertir a CNF
    print("Convirtiendo a Forma Normal de Chomsky...")
    converter = CNFConverter(original_grammar)
    cnf_grammar = converter.convert()
    
    # Paso 3: Crear parser CYK
    print("Inicializando parser CYK...")
    parser = CYKParser(cnf_grammar)
    
    print("✓ Sistema listo\n")
    
    # Menú principal
    while True:
        print_menu()
        option = input("Selecciona una opción (1-5): ").strip()
        
        if option == '1':
            show_original_grammar(original_grammar)
            
        elif option == '2':
            show_cnf_grammar(cnf_grammar)
            
        elif option == '3':
            interactive_mode(parser)
            
        elif option == '4':
            test_predefined_examples(parser)
            
        elif option == '5':
            print("\n¡Hasta luego!\n")
            break
            
        else:
            print("\n⚠ Opción inválida. Por favor selecciona 1-5.")


if __name__ == "__main__":
    main()