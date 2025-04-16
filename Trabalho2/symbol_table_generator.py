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

    def display(self):
        """Exibe a tabela de símbolos."""
        print("Tabela de Símbolos:")
        for entry in self.table:
            print(f"Nome: {entry['name']}, Tipo: {entry['type']}, Escopo: {entry['scope']}")

def process_node(node, symbol_table):
    """Processa um nó da árvore sintática."""
    node_type = node.get("type")
    node_value = node.get("value")

    if node_type == "Identifier" and symbol_table.current_scope != "global":
        # Identificadores dentro de expressões
        symbol_table.add_symbol(node_value, "variable")
    elif node_type == "Assignment":
        # Declaração de variável
        identifier_node = node["children"][0]
        symbol_table.add_symbol(identifier_node["value"], "variable")
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
