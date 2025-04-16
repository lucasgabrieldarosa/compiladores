import re  # Importa o módulo de expressões regulares
import sys  # Importa o módulo do sistema

# Garante a codificação correta da saída
sys.stdout.reconfigure(encoding='utf-8')

# Definição das especificações dos tokens
# Cada tupla contém o nome do token e a expressão regular correspondente
token_specification = [
    ('KEYWORD', r'\b(if|while|return)\b'),  # Palavras-chave da linguagem
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),  # Identificadores (nomes de variáveis, funções, etc.)
    ('INTEGER', r'\d+'),  # Números inteiros
    ('OPERATOR', r'[+\-*/]'),  # Operadores matemáticos
    ('SYMBOL', r'[;(){}]'),  # Símbolos como parênteses e chaves
    ('WHITESPACE', r'\s+'),  # Espaços em branco (serão ignorados)
    ('UNKNOWN', r'[^\w\s;+\-*/{}()]')  # Caracteres inválidos
]

# Concatena as expressões regulares em um único padrão
token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)

# Função que realiza a análise léxica
def lexer(code):
    tokens = []  # Lista para armazenar os tokens
    for match in re.finditer(token_regex, code):  # Percorre o código-fonte em busca de padrões
        kind = match.lastgroup  # Obtém o tipo do token encontrado
        value = match.group(kind)  # Obtém o valor correspondente ao token
        if kind == 'UNKNOWN':  # Trata erros de caracteres inválidos
            print(f"Erro: Caractere inválido '{value}' encontrado.")
        elif kind != 'WHITESPACE':  # Ignora espaços em branco
            tokens.append((kind, value))  # Adiciona o token à lista
    return tokens  # Retorna a lista de tokens

# Bloco principal para testar o analisador léxico
if __name__ == "__main__":
    test_cases = [  # Casos de teste
        "if (x + 10) { return y; }",  # Exemplo com palavras-chave, identificadores e operadores
        "while (a - 5) { x = x * 2; }",  # Loop com operadores matemáticos
        "return 42;",  # Retorno de um número inteiro
        "var_1 = 100 @",  # Teste com caractere inválido '@'
        "func() { return x % 2; }"  # Teste com caractere inválido '%'
    ]
    
    for i, code in enumerate(test_cases, 1):  # Itera sobre os casos de teste
        print(f"Test Case {i}:")  # Exibe o número do teste
        tokens = lexer(code)  # Executa o analisador léxico no código de teste
        for token in tokens:  # Exibe cada token encontrado
            print(token)
        print()  # Linha em branco para separar os testes
