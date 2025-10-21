"""
Script de prueba rápida para verificar que todo funciona
Ejecuta: python test_quick.py
"""

from src.grammar import create_english_grammar
from src.cnf_converter import CNFConverter
from src.cyk_algorithm import CYKParser
from src.parse_tree import ParseTreeBuilder


def test_basic():
    """Prueba básica del sistema completo"""
    
    print("="*70)
    print("PRUEBA RÁPIDA DEL SISTEMA CYK")
    print("="*70)
    
    # 1. Crear gramática
    print("\n[1/4] Creando gramática original...")
    grammar = create_english_grammar()
    print(f"✓ Gramática creada con {len(grammar.variables)} variables y {len(grammar.terminals)} terminales")
    
    # 2. Convertir a CNF
    print("\n[2/4] Convirtiendo a CNF...")
    converter = CNFConverter(grammar)
    cnf = converter.convert()
    print(f"✓ CNF generada con {len(cnf.variables)} variables")
    
    # 3. Crear parser
    print("\n[3/4] Inicializando parser CYK...")
    parser = CYKParser(cnf)
    print("✓ Parser listo")
    
    # 4. Probar oraciones
    print("\n[4/4] Probando oraciones de ejemplo...")
    print("\n" + "-"*70)
    
    test_sentences = [
        ("she eats a cake", True),
        ("the dog drinks the beer", True),
        ("the fork eats the oven", True),
        ("she eats", False),
        ("eats she cake", False),
    ]
    
    for sentence, expected in test_sentences:
        accepted, time_ms, _ = parser.parse(sentence)
        time_ms = time_ms * 1000
        
        status = "✓" if accepted else "✗"
        expected_str = "(esperado)" if accepted == expected else "(INESPERADO!)"
        
        print(f"{status} '{sentence}'")
        print(f"   Tiempo: {time_ms:.2f} ms {expected_str}")
        
        # Si fue aceptada, mostrar árbol pequeño
        if accepted:
            builder = ParseTreeBuilder(parser)
            tree = builder.build_tree(sentence.split())
            bracket = builder.to_bracket_notation(tree)
            print(f"   Árbol: {bracket}")
        
        print()
    
    print("-"*70)
    print("\n✓ ¡Todas las pruebas completadas!")
    print("\nPara ejecutar el programa completo, usa: python main.py")


if __name__ == "__main__":
    test_basic()