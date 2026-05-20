# Análise sintática: valida a estrutura do programa (gramática: programa → comando+)
def parse(tokens, lex_errors):
    errors = list(lex_errors)

    if not tokens and not errors:
        errors.append(
            {"line": 0, "message": "Programa vazio: nenhum comando encontrado"})

    success = len(errors) == 0
    return success, errors
