"""
Implementación del algoritmo CYK (Cocke-Younger-Kasami)
para parsing de gramáticas libres de contexto en CNF
"""

import time


class CYKParser:
    """
    Implementa el algoritmo CYK para verificar si una cadena
    pertenece al lenguaje generado por una gramática en CNF
    """
    
    def __init__(self, grammar):
        """
        Args:
            grammar: Gramática en CNF
        """
        self.grammar = grammar
        self.table = None
        self.backpointers = None  # Para construcción del árbol
        
    def parse(self, sentence):
        """
        Verifica si una oración pertenece al lenguaje
        
        Args:
            sentence: string o lista de palabras
            
        Returns:
            tuple (accepted, time_taken, table)
            - accepted: True si la oración es aceptada
            - time_taken: tiempo de ejecución en segundos
            - table: la tabla CYK completa
        """
        start_time = time.time()
        
        # Convertir oración a lista de palabras
        if isinstance(sentence, str):
            words = sentence.lower().split()
        else:
            words = [w.lower() for w in sentence]
        
        n = len(words)
        
        # Inicializar tabla CYK
        # table[i][j] contiene el conjunto de variables que pueden
        # derivar la subcadena desde posición i con longitud j+1
        self.table = [[set() for _ in range(n)] for _ in range(n)]
        
        # Inicializar backpointers para construcción del árbol
        # backpointers[i][j] = {variable: (regla, split_point)}
        self.backpointers = [[{} for _ in range(n)] for _ in range(n)]
        
        # PASO 1: Llenar la diagonal (palabras individuales)
        # Para cada palabra, encontrar qué variables la producen
        for i, word in enumerate(words):
            for variable, productions in self.grammar.productions.items():
                for prod in productions:
                    # Buscar producciones A → word
                    if prod == word:
                        self.table[i][0].add(variable)
                        self.backpointers[i][0][variable] = (word, None)
        
        # PASO 2: Llenar el resto de la tabla (programación dinámica)
        # length: longitud de la subcadena (2, 3, ..., n)
        for length in range(2, n + 1):
            # i: posición inicial de la subcadena
            for i in range(n - length + 1):
                # j: índice en la tabla (length - 1)
                j = length - 1
                
                # k: punto de división de la subcadena
                # Probamos todas las formas de dividir la subcadena
                for k in range(length - 1):
                    # Subcadena izquierda: table[i][k]
                    # Subcadena derecha: table[i+k+1][j-k-1]
                    
                    left_vars = self.table[i][k]
                    right_vars = self.table[i + k + 1][j - k - 1]
                    
                    # Buscar reglas A → B C donde B está en left y C en right
                    for variable, productions in self.grammar.productions.items():
                        for prod in productions:
                            # Solo nos interesan producciones binarias A → B C
                            if isinstance(prod, tuple) and len(prod) == 2:
                                left_sym, right_sym = prod
                                
                                if left_sym in left_vars and right_sym in right_vars:
                                    self.table[i][j].add(variable)
                                    # Guardar backpointer
                                    self.backpointers[i][j][variable] = (
                                        (left_sym, right_sym),
                                        k
                                    )
        
        # Verificar si el símbolo inicial está en la celda final
        accepted = self.grammar.start_symbol in self.table[0][n - 1]
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        return accepted, time_taken, self.table
    
    def print_table(self, words):
        """
        Imprime la tabla CYK de forma legible
        
        Args:
            words: lista de palabras de la oración
        """
        n = len(words)
        
        print("\n" + "="*60)
        print("TABLA CYK")
        print("="*60)
        
        print("\nPalabras:", " ".join(words))
        print()
        
        # Imprimir tabla
        for j in range(n - 1, -1, -1):
            print(f"Longitud {j+1}:", end=" ")
            for i in range(n - j):
                cell = self.table[i][j]
                if cell:
                    print(f"{{{','.join(sorted(cell))}}}", end=" ")
                else:
                    print("{∅}", end=" ")
            print()
        
        print("\n" + "="*60)
    
    def get_parse_explanation(self, words):
        """
        Genera una explicación paso a paso del parsing
        
        Args:
            words: lista de palabras
            
        Returns:
            string con la explicación
        """
        n = len(words)
        explanation = []
        
        explanation.append("\n=== PROCESO DE PARSING ===\n")
        
        # Paso 1: palabras individuales
        explanation.append("Paso 1: Palabras individuales")
        for i, word in enumerate(words):
            vars_found = self.table[i][0]
            if vars_found:
                explanation.append(f"  '{word}' puede ser: {', '.join(sorted(vars_found))}")
        
        # Paso 2: subcadenas más largas
        for length in range(2, n + 1):
            explanation.append(f"\nPaso {length}: Subcadenas de longitud {length}")
            
            for i in range(n - length + 1):
                j = length - 1
                subcadena = " ".join(words[i:i+length])
                vars_found = self.table[i][j]
                
                if vars_found:
                    explanation.append(f"  '{subcadena}' puede ser: {', '.join(sorted(vars_found))}")
        
        # Resultado final
        explanation.append("\n=== RESULTADO ===")
        if self.grammar.start_symbol in self.table[0][n-1]:
            explanation.append(f"✓ La oración ES ACEPTADA (contiene '{self.grammar.start_symbol}')")
        else:
            explanation.append(f"✗ La oración NO es aceptada (no contiene '{self.grammar.start_symbol}')")
            explanation.append(f"  Celda final contiene: {self.table[0][n-1] if self.table[0][n-1] else '∅'}")
        
        return "\n".join(explanation)


if __name__ == "__main__":
    # Prueba del módulo
    from .grammar import create_english_grammar
    from .cnf_converter import CNFConverter
    
    # Crear y convertir gramática
    original = create_english_grammar()
    converter = CNFConverter(original)
    cnf_grammar = converter.convert()
    
    # Crear parser
    parser = CYKParser(cnf_grammar)
    
    # Probar oraciones
    test_sentences = [
        "she eats a cake",
        "the dog drinks the beer",
        "he cooks",  # Debería fallar (no hay objeto)
    ]
    
    for sentence in test_sentences:
        print(f"\n{'='*60}")
        print(f"Probando: '{sentence}'")
        print('='*60)
        
        accepted, time_taken, _ = parser.parse(sentence)
        
        print(f"Resultado: {'ACEPTADA' if accepted else 'RECHAZADA'}")
        print(f"Tiempo: {time_taken*1000:.2f} ms")
        
        words = sentence.split()
        parser.print_table(words)