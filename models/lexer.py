COMMANDS_WITH_ARG = {'MOVE', 'BACK'}
COMMANDS_NO_ARG = {'LEFT', 'RIGHT', 'SCAN'}


class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def to_dict(self):
        return {"type": self.type, "value": self.value, "line": self.line}


def tokenize(script):
    tokens = []
    errors = []

    for line_num, raw_line in enumerate(script.splitlines(), start=1):
        line = raw_line.strip()

        if not line or line.startswith('#'):
            continue

        line = line.split('#')[0].strip()
        parts = line.upper().split()
        command = parts[0]

        if command in COMMANDS_WITH_ARG:
            if len(parts) != 2:
                errors.append({
                    "line": line_num,
                    "message": f"'{command}' requer exatamente um argumento numérico",
                })
                continue
            try:
                n = int(parts[1])
                if n < 1:
                    raise ValueError
                tokens.append(Token(command, n, line_num))
            except ValueError:
                errors.append({
                    "line": line_num,
                    "message": f"'{command}' requer inteiro positivo, recebeu '{parts[1]}'",
                })

        elif command in COMMANDS_NO_ARG:
            if len(parts) != 1:
                errors.append({
                    "line": line_num,
                    "message": f"'{command}' não aceita argumentos",
                })
                continue
            tokens.append(Token(command, None, line_num))

        else:
            errors.append({
                "line": line_num,
                "message": f"Comando desconhecido: '{parts[0]}'",
            })

    return tokens, errors
