"""
Módulo para representar y manejar gramáticas libres de contexto (CFG)
"""

class Grammar:
    """
    Representa una gramática libre de contexto.
    
    Atributos:
        variables: conjunto de símbolos no terminales (ej: S, NP, VP)
        terminals: conjunto de símbolos terminales (ej: a, the, cat)
        productions: diccionario con las reglas de producción
                    {variable: [lista de producciones]}
        start_symbol: símbolo inicial de la gramática (normalmente S)
    """
    
    def __init__(self, variables, terminals, productions, start_symbol='S'):
        """
        Inicializa la gramática
        
        Args:
            variables: set o list de variables
            terminals: set o list de terminales
            productions: dict con las producciones
            start_symbol: símbolo de inicio
        """
        self.variables = set(variables)
        self.terminals = set(terminals)
        self.productions = productions
        self.start_symbol = start_symbol
        
    def add_production(self, variable, production):
        """
        Añade una regla de producción
        
        Args:
            variable: lado izquierdo de la regla
            production: lado derecho (puede ser string o tupla)
        """
        if variable not in self.productions:
            self.productions[variable] = []
        self.productions[variable].append(production)
        
    def get_productions(self, variable):
        """
        Obtiene todas las producciones de una variable
        
        Returns:
            Lista de producciones o lista vacía si no existe
        """
        return self.productions.get(variable, [])
    
    def is_terminal(self, symbol):
        """Verifica si un símbolo es terminal"""
        return symbol in self.terminals
    
    def is_variable(self, symbol):
        """Verifica si un símbolo es variable"""
        return symbol in self.variables
    
    def __str__(self):
        """Representación en string de la gramática"""
        result = f"Gramática con símbolo inicial: {self.start_symbol}\n"
        result += f"Variables: {sorted(self.variables)}\n"
        result += f"Terminales: {sorted(self.terminals)}\n"
        result += "\nProducciones:\n"
        
        for var in sorted(self.productions.keys()):
            prods = self.productions[var]
            result += f"  {var} → "
            result += " | ".join([self._prod_to_str(p) for p in prods])
            result += "\n"
        
        return result
    
    def _prod_to_str(self, production):
        """Convierte una producción a string"""
        if isinstance(production, tuple):
            return " ".join(production)
        return str(production)


def create_english_grammar():
    """
    Crea la gramática del proyecto (oraciones simples en inglés)
    
    Returns:
        Objeto Grammar con las reglas definidas en el proyecto
    """
    variables = {'S', 'NP', 'VP', 'PP', 'V', 'P', 'N', 'Det'}
    
    terminals = {
        'he', 'she',
        'cooks', 'drinks', 'eats', 'cuts',
        'in', 'with',
        'cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup',
        'fork', 'knife', 'oven', 'spoon',
        'a', 'the'
    }
    
    # Definimos las producciones como en el documento
    # Usamos tuplas para producciones con múltiples símbolos
    # y strings para producciones con un solo símbolo
    productions = {
        'S': [('NP', 'VP')],
        
        'VP': [
            ('VP', 'PP'),
            ('V', 'NP'),
            'cooks', 'drinks', 'eats', 'cuts'
        ],
        
        'PP': [('P', 'NP')],
        
        'NP': [
            ('Det', 'N'),
            'he', 'she'
        ],
        
        'V': ['cooks', 'drinks', 'eats', 'cuts'],
        
        'P': ['in', 'with'],
        
        'N': [
            'cat', 'dog',
            'beer', 'cake', 'juice', 'meat', 'soup',
            'fork', 'knife', 'oven', 'spoon'
        ],
        
        'Det': ['a', 'the']
    }
    
    return Grammar(variables, terminals, productions, start_symbol='S')


if __name__ == "__main__":
    # Prueba del módulo
    g = create_english_grammar()
    print(g)
    print("\nEjemplo de producciones de VP:")
    print(g.get_productions('VP'))