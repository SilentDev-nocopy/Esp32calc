# Resiris frontend – első PC prototípus

A Resiris első PC-s frontendje:

1. Tokenizer
2. Parser
3. AST
4. Minimális Interpreter

## Futtatás

```bash
python3 run_resiris.py
```

Várható eredmény:

```text
=== RESIRIS RUNTIME ===
number = 15 (int)
other = 5 (int)
```

## Fájlok

- `tokenizer.py` – `.resy` forrás → tokenek
- `ast_nodes.py` – AST adatstruktúrák
- `parser.py` – tokenek → AST
- `interpreter.py` – AST → végrehajtás
- `run_resiris.py` – teljes pipeline indítása
- `main.resy` – minimális futtatható példa
- `test_frontend.py` – Tokenizer + Parser teszt

## Első Interpreter scope

Jelenleg kezel:

- `v`
- `c`
- `UnknownObject`
- `int`
- `float`
- `string`
- `bool`
- `=`
- `+=`
- `-=`
- `*=`
- `/=`
- `+ - * / %`
- `== != > < >= <=`
- változónevek
- szám/string/bool literálok

Még nem hajt végre:

- `if / elif / else`
- `fn / return`
- `mat`
- `await`
- modulokat
- `ResirisModuleObject`

A Parser ezeket részben már felismeri, de az Interpreterben szándékosan
nincsenek még implementálva.

A paraméterlista jelenlegi formája (`fn add(a, b):`) továbbra is PROPOSAL /
technikai prototípus, nem végleges Resiris nyelvi döntés.
