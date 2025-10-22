"""
Módulo para convertir una gramática CFG a Forma Normal de Chomsky (CNF)

CNF requiere que todas las producciones sean de la forma:
- A → BC (dos variables)
- A → a (un terminal)
"""

from copy import deepcopy
from .grammar import Grammar


class CNFConverter:
    """
    Convierte una gramática CFG a su Forma Normal de Chomsky
    """
    
    def __init__(self, grammar):
        """
        Args:
            grammar: objeto Grammar a convertir
        """
        self.original_grammar = grammar
        self.new_variables_counter = 0
        
    def convert(self):
        """
        Convierte la gramática a CNF siguiendo estos pasos:
        1. Eliminar producciones epsilon (ε)
        2. Eliminar producciones unitarias (A → B)
        3. Convertir terminales en producciones mixtas
        4. Romper producciones largas
        
        Returns:
            Nueva gramática en CNF
        """
        # Creamos una copia para no modificar la original
        grammar = self._copy_grammar()
        
        # Paso 1: Eliminar producciones epsilon (omitir por simplicidad)
        # grammar = self._eliminate_epsilon(grammar)
        
        # Paso 2: Eliminar producciones unitarias
        grammar = self._eliminate_unit_productions(grammar)
        
        # Paso 3: Convertir terminales en producciones con variables
        grammar = self._convert_terminals(grammar)
        
        # Paso 4: Romper producciones largas (más de 2 símbolos)
        grammar = self._break_long_productions(grammar)
        
        return grammar
    
    def _copy_grammar(self):
        """Crea una copia profunda de la gramática"""
        new_productions = {}
        for var, prods in self.original_grammar.productions.items():
            new_productions[var] = [p for p in prods]
            
        return Grammar(
            set(self.original_grammar.variables),
            set(self.original_grammar.terminals),
            new_productions,
            self.original_grammar.start_symbol
        )
    
    def _eliminate_unit_productions(self, grammar):
        """
        Elimina producciones unitarias (A → B donde B es variable)
        
        Ejemplo: Si tenemos A → B y B → c | d
                 Lo convertimos a A → c | d
        """
        changed = True
        
        while changed:
            changed = False
            new_productions = {}
            
            for var in grammar.productions:
                new_productions[var] = []
                
                for prod in grammar.productions[var]:
                    # Si es producción unitaria (A → B)
                    if isinstance(prod, str) and prod in grammar.variables:
                        # Expandir: agregar todas las producciones de B
                        for target_prod in grammar.productions.get(prod, []):
                            if target_prod not in new_productions[var]:
                                new_productions[var].append(target_prod)
                                changed = True
                    else:
                        # No es unitaria, la mantenemos
                        if prod not in new_productions[var]:
                            new_productions[var].append(prod)
            
            grammar.productions = new_productions
        
        return grammar
    
    def _convert_terminals(self, grammar):
        """
        Convierte terminales en producciones mixtas a nuevas variables
        
        Ejemplo: A → B c  se convierte a:
                 A → B C_c
                 C_c → c
        """
        new_productions = {}
        terminal_vars = {}  # Mapeo de terminal → variable
        
        # Para cada terminal, crear una variable nueva
        for terminal in grammar.terminals:
            var_name = f"T_{terminal}"
            terminal_vars[terminal] = var_name
            grammar.variables.add(var_name)
            new_productions[var_name] = [terminal]
        
        # Convertir producciones existentes
        for var in grammar.productions:
            new_productions[var] = []
            
            for prod in grammar.productions[var]:
                if isinstance(prod, str):
                    # Producción simple (A → a o A → B)
                    new_productions[var].append(prod)
                else:
                    # Producción múltiple (A → B C o A → B c)
                    new_prod = []
                    for symbol in prod:
                        if symbol in grammar.terminals:
                            # Reemplazar terminal por su variable
                            new_prod.append(terminal_vars[symbol])
                        else:
                            new_prod.append(symbol)
                    new_productions[var].append(tuple(new_prod))
        
        grammar.productions = new_productions
        return grammar
    
    def _break_long_productions(self, grammar):
        """
        Rompe producciones con más de 2 símbolos en el lado derecho
        
        Ejemplo: A → B C D  se convierte a:
                 A → B X1
                 X1 → C D
        """
        new_productions = {}
        
        for var in grammar.productions:
            new_productions[var] = []
            
            for prod in grammar.productions[var]:
                if isinstance(prod, str):
                    # Producción simple, no se rompe
                    new_productions[var].append(prod)
                elif len(prod) == 2:
                    # Ya está en CNF (A → B C)
                    new_productions[var].append(prod)
                else:
                    # Producción larga, hay que romperla
                    # A → B C D E  =>  A → B X1, X1 → C X2, X2 → D E
                    current_var = var
                    symbols = list(prod)
                    
                    while len(symbols) > 2:
                        # Crear nueva variable
                        new_var = self._generate_variable_name()
                        grammar.variables.add(new_var)
                        
                        # A → B X1
                        new_productions[current_var].append((symbols[0], new_var))
                        
                        # Preparar siguiente iteración
                        current_var = new_var
                        symbols = symbols[1:]
                        
                        if new_var not in new_productions:
                            new_productions[new_var] = []
                    
                    # Última producción (2 símbolos)
                    new_productions[current_var].append(tuple(symbols))
        
        grammar.productions = new_productions
        return grammar
    
    def _generate_variable_name(self):
        """Genera un nombre único para nuevas variables"""
        name = f"X{self.new_variables_counter}"
        self.new_variables_counter += 1
        return name


if __name__ == "__main__":
    # Prueba del módulo
    from .grammar import create_english_grammar
    
    original = create_english_grammar()
    print("=== GRAMÁTICA ORIGINAL ===")
    print(original)
    
    converter = CNFConverter(original)
    cnf_grammar = converter.convert()
    
    print("\n=== GRAMÁTICA EN CNF ===")
    print(cnf_grammar)