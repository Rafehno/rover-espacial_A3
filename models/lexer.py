COMMANDS_WITH_ARG = {'MOVE', 'BACK'}
COMMANDS_NO_ARG   = {'LEFT', 'RIGHT', 'SCAN'}

MAX_LINES = 200
MAX_ARG   = 100


# Unidade mínima extraída do script: tipo, valor numérico e linha de origem
class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def to_dict(self):
        return {"type": self.type, "value": self.value, "line": self.line}


# Análise léxica: transforma o texto do script em uma lista de Tokens
def tokenize(script):
    tokens = []
    errors = []

    all_lines = script.splitlines()

    if len(all_lines) > MAX_LINES:
        errors.append({"line": 0, "message": f"Script muito longo: máximo {MAX_LINES} linhas (recebido {len(all_lines)})"})
        return tokens, errors

    for line_num, raw_line in enumerate(all_lines, start=1):
        line = raw_line.strip()

        if not line or line.startswith('#'):
            continue

        line = line.split('#')[0].strip()
        parts = line.upper().split()
        command = parts[0]

        if command in COMMANDS_WITH_ARG:
            if len(parts) != 2:
                errors.append({"line": line_num, "message": f"'{command}' requer exatamente um argumento numérico"})
                continue
            try:
                n = int(parts[1])
                if n < 1 or n > MAX_ARG:
                    raise ValueError
                tokens.append(Token(command, n, line_num))
            except ValueError:
                errors.append({"line": line_num, "message": f"'{command}' requer inteiro entre 1 e {MAX_ARG}, recebeu '{parts[1]}'"})

        elif command in COMMANDS_NO_ARG:
            if len(parts) != 1:
                errors.append({"line": line_num, "message": f"'{command}' não aceita argumentos"})
                continue
            tokens.append(Token(command, None, line_num))

        else:
            errors.append({"line": line_num, "message": f"Comando desconhecido: '{parts[0]}'"})

    return tokens, errors
