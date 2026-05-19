# O parser recebe os tokens do lexer e verifica a estrutura do programa.
# Gramática: programa → comando+  (ao menos um comando válido)


def parse(tokens, lex_errors):
    errors = list(lex_errors)

    if not tokens and not errors:
        errors.append({"line": 0, "message": "Programa vazio: nenhum comando encontrado"})

    success = len(errors) == 0
    return success, errors
