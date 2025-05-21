import json  # Import para exportar a árvore em JSON
import re
import sys
import os  # Adicione este import no início do arquivo
sys.stdout.reconfigure(encoding='utf-8')

# Definição dos tokens da linguagem
token_specification = [
    ('KEYWORD', r'\b(if|while|return)\b'),  # Palavras-chave
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),  # Identificadores
    ('INTEGER', r'\d+'),  # Números inteiros
    ('OPERATOR', r'[+\-*/=<>!]'),  # Operadores matemáticos e relacionais
    ('SYMBOL', r'[;(){}]'),  # Símbolos especiais
    ('WHITESPACE', r'\s+'),  # Espaços em branco (ignorados)
    ('UNKNOWN', r'[^\w\s;+\-*/=<>!{}()]')  # Caracteres inválidos
]

# Expressão regular para encontrar tokens
token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)

# Função do analisador léxico
def lexer(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group(kind)
        if kind == 'UNKNOWN':
            raise SyntaxError(f"Erro léxico: Caractere inválido '{value}' encontrado.")
        elif kind != 'WHITESPACE':
            tokens.append((kind, value))
    return tokens

# Classe para representar nós da árvore sintática
class SyntaxTreeNode:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []

    def to_dict(self):
        """Converte o nó e seus filhos para um dicionário (para exportação JSON)."""
        return {
            "type": self.type,
            "value": self.value,
            "children": [child.to_dict() for child in self.children]
        }

# Modificação no Parser para construir a árvore
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.root = SyntaxTreeNode("Program")  # Nó raiz da árvore

    def match(self, expected_type):
        """Verifica se o próximo token é do tipo esperado"""
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
            return True
        return False

    def parse_expression(self):
        """Regra: Expressão → Termo (OPERATOR Termo)*"""
        node = SyntaxTreeNode("Expression")
        term_node = self.parse_term()
        if not term_node:
            return None
        node.children.append(term_node)
        while self.match("OPERATOR"):
            operator_node = SyntaxTreeNode("Operator", self.tokens[self.pos - 1][1])
            term_node = self.parse_term()
            if not term_node:
                return None
            operator_node.children.append(node.children.pop())
            operator_node.children.append(term_node)
            node.children.append(operator_node)
        return node

    def parse_term(self):
        """Regra: Termo → IDENTIFIER | INTEGER | ( Expressão )"""
        if self.match("IDENTIFIER"):
            return SyntaxTreeNode("Identifier", self.tokens[self.pos - 1][1])
        if self.match("INTEGER"):
            return SyntaxTreeNode("Integer", self.tokens[self.pos - 1][1])
        if self.match("SYMBOL") and self.tokens[self.pos - 1][1] == "(":
            expr_node = self.parse_expression()
            if not expr_node or not self.match("SYMBOL") or self.tokens[self.pos - 1][1] != ")":
                return None
            return expr_node
        return None

    def parse_statement(self):
        """Regra: Comando → EstruturaControle | Atribuicao | Retorno"""
        if self.match("KEYWORD"):
            keyword = self.tokens[self.pos - 1][1]
            if keyword in ["if", "while"]:
                node = SyntaxTreeNode("ControlStructure", keyword)
                if self.match("SYMBOL") and self.tokens[self.pos - 1][1] == "(":
                    condition_node = self.parse_expression()
                    if not condition_node or not self.match("SYMBOL") or self.tokens[self.pos - 1][1] != ")":
                        return None
                    node.children.append(condition_node)
                    if not self.match("SYMBOL") or self.tokens[self.pos - 1][1] != "{":
                        return None
                    while True:
                        statement_node = self.parse_statement()
                        if not statement_node:
                            break
                        node.children.append(statement_node)
                    if not self.match("SYMBOL") or self.tokens[self.pos - 1][1] != "}":
                        return None
                self.root.children.append(node)
                return node
            elif keyword == "return":
                node = SyntaxTreeNode("Return")
                expr_node = self.parse_expression()
                if not expr_node or not self.match("SYMBOL") or self.tokens[self.pos - 1][1] != ";":
                    return None
                node.children.append(expr_node)
                self.root.children.append(node)
                return node
        elif self.match("IDENTIFIER"):
            node = SyntaxTreeNode("Assignment")
            identifier_node = SyntaxTreeNode("Identifier", self.tokens[self.pos - 1][1])
            if not self.match("OPERATOR") or self.tokens[self.pos - 1][1] != "=":
                return None
            expr_node = self.parse_expression()
            if not expr_node or not self.match("SYMBOL") or self.tokens[self.pos - 1][1] != ";":
                return None
            node.children.append(identifier_node)
            node.children.append(expr_node)
            self.root.children.append(node)
            return node
        return None

    def parse(self):
        """Regra: Programa → Comandos"""
        while self.parse_statement():
            pass
        return self.pos == len(self.tokens)  # Verifica se todos os tokens foram consumidos

# Testes de código
test_cases = [
    "if (x + 10) { return y; }",
    "while (a - 5) { x = x * 2; }",
    "return (x + y) * z;",
    "x = 10 + 5;",
    "if (n > 0) { n = n - 1; return result; }",
    # Teste com erro
    "y = x + 1; return z;"  
]

os.makedirs("testes", exist_ok=True)

# Execução dos testes
for i, code in enumerate(test_cases, 1):
    print(f"\nTest Case {i}: {code}")
    try:
        tokens = lexer(code)
        print("Tokens:", tokens)
        parser = Parser(tokens)
        if parser.parse():
            print("✅ Código válido!")
            # Exporta a árvore sintática para JSON
            tree_json = json.dumps(parser.root.to_dict(), indent=4, ensure_ascii=False)
            print("Árvore Sintática (JSON):")
            print(tree_json)
            # Salvar a árvore sintática em um arquivo JSON
            with open(f"testes/tree_test_case_{i}.json", "w", encoding="utf-8") as f:
                json.dump(parser.root.to_dict(), f, indent=4, ensure_ascii=False)
        else:
            print("❌ Erro sintático!")
    except SyntaxError as e:
        print("❌", e)
