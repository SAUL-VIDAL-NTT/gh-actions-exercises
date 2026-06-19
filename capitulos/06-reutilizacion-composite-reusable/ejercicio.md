# Ejercicio 06 · Workflow reutilizable

## Objetivo

Crear un workflow reutilizable parametrizable con `workflow_call`.

## Tarea

Crea **`.github/workflows/cap06-reusable.yml`** que:

1. Tenga `name`.
2. Se dispare con **`workflow_call`** y defina al menos un **`inputs`**.
3. Tenga al menos un job que **use ese input** (p.ej. `${{ inputs.entorno }}`).

## Bonus (no calificado, muy recomendado)

Crea también un **llamador** `.github/workflows/cap06-llamador.yml` que se dispare
en `push` y llame a tu reutilizable:

```yaml
on: [push]
jobs:
  usar:
    uses: ./.github/workflows/cap06-reusable.yml
    with:
      entorno: staging
```

Así verás el reutilizable ejecutarse de verdad en la pestaña Actions.

## Criterios de evaluación (sobre `cap06-reusable.yml`)

**Deterministas (60 %)**

- Define `name`.
- Se dispara con `workflow_call`.
- Declara un bloque `inputs:`.
- Tiene al menos un job.
- El workflow **usa** el input (`inputs.`).

**Juez LLM (40 %)** — inputs bien tipados (`type:`, `required:`, `default:`),
diseño reutilizable real y, si procede, `outputs`/`secrets` coherentes.

> Solución: `solucion/cap06-reusable.yml` (+ `solucion/cap06-llamador.yml`).
