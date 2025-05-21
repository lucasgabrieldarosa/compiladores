def tac_to_riscv(tac_lines):
    reg_map = {}  # Mapeia temporários TAC para registradores RISC-V
    reg_pool = [f"t{i}" for i in range(7)]  # t0-t6
    reg_idx = 0

    for line in tac_lines:
        parts = line.split()
        if '=' in line and '+' in line:
            # Exemplo: t1 = x + 1
            dest, _, left, op, right = parts
            reg = reg_pool[reg_idx % len(reg_pool)]
            reg_map[dest] = reg
            print(f"    li {reg}, {right}" if right.isdigit() else f"    lw {reg}, {right}")
            print(f"    lw t6, {left}" if not left.isdigit() else f"    li t6, {left}")
            print(f"    add {reg}, t6, {reg}")
        elif '=' in line:
            # Exemplo: y = t1
            dest, _, src = parts
            reg = reg_map.get(src, "t0")
            print(f"    sw {reg}, {dest}")
        elif line.startswith("return"):
            _, src = line.split()
            reg = reg_map.get(src, "t0")
            print(f"    mv a0, {reg}")
            print("    ret")
        # Adicione outros casos conforme necessário

if __name__ == "__main__":
    # Exemplo de uso:
    tac = [
        "t1 = x + 1",
        "y = t1",
        "return y"
    ]
    tac_to_riscv(tac)