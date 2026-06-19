# Ejercicio 04 · Matriz, dependencias y condicionales

## Objetivo

Orquestar varios jobs con matriz, `needs`, salidas entre jobs y condicionales.

## Tarea

Crea **`.github/workflows/cap04-flujo.yml`** que:

1. Tenga `name` y se dispare en `push`.
2. Tenga un job `preparar` que **declare un `outputs`** alimentado por una salida
   de step (p.ej. una versión).
3. Tenga un job de **matriz** con al menos **3 valores** (p.ej. 3 versiones de un
   runtime) que **dependa** (`needs`) de `preparar`.
4. Incluya al menos un **condicional `if`** (en un job o en un step).

## Pasos sugeridos

1. Rama `cap04`, crea el archivo, `push`.
2. En **Actions**, observa cómo la matriz genera varios jobs y cómo `needs`
   ordena la ejecución.

## Criterios de evaluación

**Deterministas (60 %)**

- `name` y disparo en `push`.
- Define `outputs` en algún job.
- Usa `needs`.
- Tiene una matriz con ≥ 3 valores.
- Usa al menos un `if`.

**Juez LLM (40 %)** — buen uso de `fail-fast`, paso de datos entre jobs vía
`needs.<job>.outputs`, y condicionales con sentido (p.ej. desplegar solo en `main`).

## Pista

```yaml
strategy:
  fail-fast: false
  matrix:
    version: ["3.10", "3.11", "3.12"]
```

> Solución: `solucion/cap04-flujo.yml`.
