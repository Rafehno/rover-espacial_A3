# Linguagem de Comandos — Rover Espacial

## Gramática Formal (GLC)

```
programa     → comando+
comando      → cmd_move
             | cmd_back
             | cmd_left
             | cmd_right
             | cmd_scan

cmd_move     → "MOVE" NUMERO
cmd_back     → "BACK" NUMERO
cmd_left     → "LEFT"
cmd_right    → "RIGHT"
cmd_scan     → "SCAN"

NUMERO       → [1-9][0-9]*
```

---

## Comandos Disponíveis

| Comando    | Sintaxe  | Descrição                               | Exemplo  |
|------------|----------|-----------------------------------------|----------|
| Avançar    | `MOVE n` | Avança n casas na direção atual         | `MOVE 3` |
| Recuar     | `BACK n` | Recua n casas na direção oposta         | `BACK 2` |
| Girar esq. | `LEFT`   | Gira 90° à esquerda                     | `LEFT`   |
| Girar dir. | `RIGHT`  | Gira 90° à direita                      | `RIGHT`  |
| Detectar   | `SCAN`   | Detecta obstáculo na célula à frente    | `SCAN`   |

---

## Regras de Sintaxe

- Cada comando ocupa **uma linha**
- Comandos são **case-insensitive** — `MOVE` = `move` = `Move`
- `n` deve ser um inteiro **positivo** (≥ 1)
- Linhas em branco são **ignoradas**
- Comentários com `#` são **ignorados**

---

## Comportamento em Bordas e Colisões

- Se o rover atingir a **borda do grid**, o movimento é cancelado e registrado no log
- Se houver um **obstáculo** no caminho, o rover para antes dele e o erro é registrado
- `SCAN` verifica apenas a célula **imediatamente à frente** (1 casa)

---

## Exemplos de Scripts

### Missão básica
```
MOVE 3
RIGHT
MOVE 2
SCAN
LEFT
MOVE 1
```

### Patrulha em L
```
MOVE 4
RIGHT
MOVE 4
RIGHT
MOVE 4
```

### Exploração com scan
```
SCAN
MOVE 2
LEFT
SCAN
MOVE 3
RIGHT
MOVE 1
SCAN
```

---

## Erros Detectados pelo Compilador

| Tipo                  | Exemplo       | Mensagem gerada                                      |
|-----------------------|---------------|------------------------------------------------------|
| Comando desconhecido  | `FLY 3`       | Comando desconhecido: 'FLY'                          |
| Argumento ausente     | `MOVE`        | 'MOVE' requer exatamente um argumento numérico       |
| Argumento inválido    | `MOVE -1`     | 'MOVE' requer inteiro positivo, recebeu '-1'         |
| Argumento indesejado  | `LEFT 2`      | 'LEFT' não aceita argumentos                         |
| Programa vazio        | *(em branco)* | Programa vazio: nenhum comando encontrado            |

---

## Comandos Bônus (opcionais)

| Comando                    | Descrição                                       |
|----------------------------|-------------------------------------------------|
| `IF OBSTACLE THEN RIGHT`   | Se há obstáculo à frente, gira à direita        |
| `REPEAT n { ... }`         | Repete o bloco de comandos n vezes              |

### Exemplo com bônus
```
REPEAT 4 {
  MOVE 2
  IF OBSTACLE THEN RIGHT
}
```
