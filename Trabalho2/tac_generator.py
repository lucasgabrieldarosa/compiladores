import json
import os

class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.tac = []
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, node):
        node_type = node.get('type')
        if node_type == 'Program':
            for child in node.get('children', []):
                self.generate(child)
        elif node_type == 'Assignment':
            var_name = node['children'][0]['value']
            expr = node['children'][1]
            temp = self.generate(expr)
            self.tac.append(f"{var_name} = {temp}")
        elif node_type == 'Expression':
            # Só repassa para o filho (único)
            return self.generate(node['children'][0])
        elif node_type == 'Operator':
            op = node['value']
            left = self.generate(node['children'][0])
            right = self.generate(node['children'][1])
            temp = self.new_temp()
            self.tac.append(f"{temp} = {left} {op} {right}")
            return temp
        elif node_type == 'Identifier':
            return node['value']
        elif node_type == 'Integer':
            return node['value']
        elif node_type == 'Return':
            expr = self.generate(node['children'][0])
            self.tac.append(f"return {expr}")
        elif node_type == 'ControlStructure' and node.get('value') == 'if':
            cond = self.generate(node['children'][0])
            label_else = self.new_label()
            label_end = self.new_label()
            self.tac.append(f"ifFalse {cond} goto {label_else}")
            # Corpo do if (pode ter mais de um comando)
            for child in node['children'][1:]:
                self.generate(child)
            self.tac.append(f"goto {label_end}")
            self.tac.append(f"{label_else}:")
            # (Se tivesse else, seria aqui)
            self.tac.append(f"{label_end}:")
        else:
            print(f"Tipo de nó não suportado: {node_type}")

    def print_tac(self):
        print("TAC gerado:")
        for instr in self.tac:
            print(instr)

def main():
    pasta_testes = "Trabalhos/Trabalho2/testes"
    for arquivo in os.listdir(pasta_testes):
        if arquivo.endswith(".json"):
            print(f"\nArquivo: {arquivo}")
            with open(os.path.join(pasta_testes, arquivo), "r") as f:
                ast = json.load(f)
            tac_gen = TACGenerator()
            tac_gen.generate(ast)
            tac_gen.print_tac()

if __name__ == "__main__":
    main()