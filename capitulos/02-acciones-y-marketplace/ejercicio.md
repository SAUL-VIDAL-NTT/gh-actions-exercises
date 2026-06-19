# Ejercicio 02 · Usar acciones del Marketplace

## Objetivo

Componer un workflow real usando acciones oficiales con sus entradas (`with`).

## Tarea

Crea **`.github/workflows/cap02-acciones.yml`** que:

1. Tenga `name` y se dispare en `push`.
2. Use **`actions/checkout`** (versión fijada, p.ej. `@v4`).
3. Use **`actions/setup-python`** (o `setup-node`) con el bloque **`with`** para
   fijar una versión del runtime.
4. Tenga un step `run` que **use ese runtime** (p.ej. `python --version` y
   ejecutar un pequeño script, o `node --version`).

## Pasos sugeridos

1. Rama `cap02`, crea el archivo, `push`.
2. En los logs, confirma que la versión instalada coincide con la que pediste en `with`.

## Criterios de evaluación

**Deterministas (60 %)**

- Define `name` y dispara en `push`.
- Usa `actions/checkout`.
- Usa `actions/setup-` (python/node/…).
- Incluye un bloque `with:`.
- Tiene al menos un step `run`.

**Juez LLM (40 %)** — versionado correcto de las acciones (no `@main`), uso
coherente del runtime instalado y orden lógico de steps.

## Pista

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
- run: python -c "print('Hola desde Python', __import__('sys').version)"
```

> Solución: `solucion/cap02-acciones.yml`.
