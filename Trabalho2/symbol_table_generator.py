import json
import os

class SymbolTable:
    def __init__(self):
        self.table = []
        self.current_scope = "global"

    def enter_scope(self, scope_name):
        """Entra em um novo escopo."""
        self.current_scope = scope_name

    def exit_scope(self):
        """Sai do escopo atual e retorna ao escopo global."""
        self.current_scope = "global"

    def add_symbol(self, name, symbol_type):
        """Adiciona um símbolo à tabela."""
        self.table.append({
            "name": name,
            "type": symbol_type,
            "scope": self.current_scope
        })

    def find_symbol(self, name):
        """Procura um símbolo na tabela pelo nome e escopo."""
        for entry in reversed(self.table):
            if entry["name"] == name and entry["scope"] == self.current_scope:
                return entry
        return None

    def is_declared(self, name):
        """Verifica se um símbolo foi declarado em qualquer escopo."""
        return any(entry["name"] == name for entry in self.table)

    def check_duplicate(self, name):
        """Verifica duplicidade de variáveis no mesmo escopo."""
        return any(entry["name"] == name and entry["scope"] == self.current_scope for entry in self.table)

    def display(self):
        """Exibe a tabela de símbolos."""
        print("Tabela de Símbolos:")
        for entry in self.table:
            print(f"Nome: {entry['name']}, Tipo: {entry['type']}, Escopo: {entry['scope']}")

def process_node(node, symbol_table):
    """Processa um nó da árvore sintática."""
    node_type = node.get("type")
    node_value = node.get("value")

    if node_type == "Identifier":
        # Verifica se a variável foi declarada
        if not symbol_table.is_declared(node_value):
            print(f"Erro: Variável '{node_value}' não declarada no escopo '{symbol_table.current_scope}'.")
    elif node_type == "Assignment":
        # Declaração de variável
        identifier_node = node["children"][0]
        if symbol_table.check_duplicate(identifier_node["value"]):
            print(f"Erro: Variável '{identifier_node['value']}' já declarada no escopo '{symbol_table.current_scope}'.")
        else:
            symbol_table.add_symbol(identifier_node["value"], "variable")
    elif node_type == "FunctionDeclaration":
        # Declaração de função
        function_name = node_value
        if symbol_table.check_duplicate(function_name):
            print(f"Erro: Função '{function_name}' já declarada no escopo '{symbol_table.current_scope}'.")
        else:
            symbol_table.add_symbol(function_name, "function")
        symbol_table.enter_scope(function_name)
        for child in node.get("children", []):
            process_node(child, symbol_table)
        symbol_table.exit_scope()
    elif node_type == "FunctionCall":
        # Chamada de função
        if not symbol_table.is_declared(node_value):
            print(f"Erro: Função '{node_value}' não declarada.")
        else:
            # Verifica tipos de parâmetros
            declared_function = symbol_table.find_symbol(node_value)
            # Supondo que a função tenha uma lista de tipos esperados
            expected_params = declared_function.get("params", [])
            actual_params = [child.get("type") for child in node.get("children", [])]
            if expected_params != actual_params:
                print(f"Erro: Tipos de parâmetros incorretos na chamada da função '{node_value}'.")
    elif node_type == "Return":
        # Verifica tipo de retorno
        return_type = node.get("returnType")
        if symbol_table.current_scope != "global":
            function_symbol = symbol_table.find_symbol(symbol_table.current_scope)
            if function_symbol and function_symbol.get("returnType") != return_type:
                print(f"Erro: Tipo de retorno incorreto na função '{symbol_table.current_scope}'.")
    elif node_type == "ControlStructure":
        # Estruturas de controle (if, while)
        symbol_table.enter_scope(node_value)
        for child in node.get("children", []):
            process_node(child, symbol_table)
        symbol_table.exit_scope()
    else:
        # Processa os filhos do nó
        for child in node.get("children", []):
            process_node(child, symbol_table)

def generate_symbol_table(json_file):
    """Gera a tabela de símbolos a partir de um arquivo JSON."""
    with open(json_file, "r", encoding="utf-8") as f:
        tree = json.load(f)

    symbol_table = SymbolTable()
    process_node(tree, symbol_table)
    symbol_table.display()

# Caminho para os arquivos JSON
json_folder = "c:\\Users\\Lucas Da Rosa\\Desktop\\Aulas\\Compiladores\\Trabalhos\\Trabalho2\\testes"

# Processa todos os arquivos JSON na pasta
for file_name in os.listdir(json_folder):
    if file_name.endswith(".json"):
        print(f"\nProcessando {file_name}...")
        generate_symbol_table(os.path.join(json_folder, file_name))
