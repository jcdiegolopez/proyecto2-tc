"""
Módulo para construir y visualizar el árbol de parsing (parse tree)
"""


class ParseTreeNode:
    """
    Representa un nodo en el árbol de parsing
    """
    
    def __init__(self, symbol, children=None):
        """
        Args:
            symbol: el símbolo (variable o terminal) del nodo
            children: lista de nodos hijos
        """
        self.symbol = symbol
        self.children = children if children else []
    
    def is_leaf(self):
        """Verifica si el nodo es una hoja (terminal)"""
        return len(self.children) == 0
    
    def __repr__(self):
        return f"Node({self.symbol})"


class ParseTreeBuilder:
    """
    Construye el árbol de parsing a partir de la tabla CYK y backpointers
    """
    
    def __init__(self, parser):
        """
        Args:
            parser: objeto CYKParser que ya ejecutó el parsing
        """
        self.parser = parser
        self.grammar = parser.grammar
        self.table = parser.table
        self.backpointers = parser.backpointers
    
    def build_tree(self, words):
        """
        Construye el árbol de parsing completo
        
        Args:
            words: lista de palabras de la oración
            
        Returns:
            ParseTreeNode raíz del árbol, o None si no se aceptó
        """
        n = len(words)
        
        # Verificar que la oración fue aceptada
        if self.grammar.start_symbol not in self.table[0][n - 1]:
            return None
        
        # Construir árbol recursivamente desde la raíz
        return self._build_recursive(
            self.grammar.start_symbol,
            0,  # posición inicial
            n - 1,  # índice en tabla (longitud - 1)
            words
        )
    
    def _build_recursive(self, symbol, i, j, words):
        """
        Construye el árbol recursivamente
        
        Args:
            symbol: símbolo actual (variable o terminal)
            i: posición inicial en la oración
            j: índice en la tabla
            words: lista de palabras
            
        Returns:
            ParseTreeNode
        """
        # Caso base: es una hoja (palabra individual)
        if j == 0:
            # El nodo representa una palabra
            word = words[i]
            return ParseTreeNode(symbol, [ParseTreeNode(word)])
        
        # Caso recursivo: obtener backpointer
        if symbol not in self.backpointers[i][j]:
            # No hay backpointer, error
            return ParseTreeNode(symbol)
        
        production, split_point = self.backpointers[i][j][symbol]
        
        # Si es una producción binaria (A → B C)
        if isinstance(production, tuple):
            left_sym, right_sym = production
            
            # Construir subárbol izquierdo
            left_child = self._build_recursive(
                left_sym,
                i,
                split_point,
                words
            )
            
            # Construir subárbol derecho
            right_child = self._build_recursive(
                right_sym,
                i + split_point + 1,
                j - split_point - 1,
                words
            )
            
            return ParseTreeNode(symbol, [left_child, right_child])
        else:
            # Es una producción terminal (A → a)
            return ParseTreeNode(symbol, [ParseTreeNode(production)])
    
    def print_tree(self, tree, indent=0):
        """
        Imprime el árbol de forma jerárquica
        
        Args:
            tree: ParseTreeNode raíz
            indent: nivel de indentación actual
        """
        if tree is None:
            print("No se pudo construir el árbol (oración no aceptada)")
            return
        
        # Imprimir el nodo actual
        print("  " * indent + "├─ " + tree.symbol)
        
        # Imprimir hijos recursivamente
        for child in tree.children:
            self.print_tree(child, indent + 1)
    
    def to_string(self, tree, indent=0):
        """
        Convierte el árbol a string
        
        Args:
            tree: ParseTreeNode raíz
            indent: nivel de indentación
            
        Returns:
            string representando el árbol
        """
        if tree is None:
            return "No tree available"
        
        result = "  " * indent + tree.symbol + "\n"
        
        for child in tree.children:
            result += self.to_string(child, indent + 1)
        
        return result
    
    def to_bracket_notation(self, tree):
        """
        Convierte el árbol a notación de brackets
        Ejemplo: [S [NP she] [VP eats]]
        
        Args:
            tree: ParseTreeNode raíz
            
        Returns:
            string en notación de brackets
        """
        if tree is None:
            return ""
        
        if tree.is_leaf():
            return tree.symbol
        
        children_str = " ".join([self.to_bracket_notation(child) for child in tree.children])
        return f"[{tree.symbol} {children_str}]"
    
    def visualize_tree_ascii(self, tree):
        """
        Crea una visualización ASCII del árbol más elaborada
        
        Args:
            tree: ParseTreeNode raíz
            
        Returns:
            string con visualización ASCII
        """
        if tree is None:
            return "No tree available"
        
        lines = []
        self._build_ascii_tree(tree, lines, "", "", "")
        return "\n".join(lines)
    
    def _build_ascii_tree(self, node, lines, prefix, child_prefix, connector):
        """
        Construye visualización ASCII recursivamente
        """
        lines.append(prefix + connector + node.symbol)
        
        children = node.children
        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)
            
            if is_last:
                new_connector = "└── "
                new_child_prefix = child_prefix + "    "
            else:
                new_connector = "├── "
                new_child_prefix = child_prefix + "│   "
            
            self._build_ascii_tree(
                child,
                lines,
                child_prefix,
                new_child_prefix,
                new_connector
            )


if __name__ == "__main__":
    # Prueba del módulo
    from .grammar import create_english_grammar
    from .cnf_converter import CNFConverter
    from .cyk_algorithm import CYKParser
    
    # Preparar gramática
    original = create_english_grammar()
    converter = CNFConverter(original)
    cnf_grammar = converter.convert()
    
    # Parser
    parser = CYKParser(cnf_grammar)
    
    # Probar oración
    sentence = "she eats a cake"
    print(f"Parsing: '{sentence}'")
    
    accepted, time_taken, _ = parser.parse(sentence)
    
    if accepted:
        print(f"\n✓ Oración ACEPTADA en {time_taken*1000:.2f} ms\n")
        
        # Construir árbol
        builder = ParseTreeBuilder(parser)
        tree = builder.build_tree(sentence.split())
        
        print("=== ÁRBOL DE PARSING ===")
        builder.print_tree(tree)
        
        print("\n=== NOTACIÓN DE BRACKETS ===")
        print(builder.to_bracket_notation(tree))
        
        print("\n=== VISUALIZACIÓN ASCII ===")
        print(builder.visualize_tree_ascii(tree))
    else:
        print(f"\n✗ Oración RECHAZADA")