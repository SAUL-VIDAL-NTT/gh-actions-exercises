# Ejercicio 01 · Anatomía de un workflow

## Objetivo

Construir un workflow con varios jobs y steps, usando el primer `uses` (checkout).

## Tarea

Crea **`.github/workflows/cap01-anatomia.yml`** que:

1. Tenga `name`.
2. Se dispare en `push` **y** en `pull_request`.
3. Tenga **al menos dos jobs** (p.ej. `inspeccionar` y `reportar`).
4. Ambos jobs corran en **Ubuntu**.
5. Al menos un job use la acción **`actions/checkout`** como primer step.
6. Tenga **steps con `name`** descriptivos y al menos un step `run` que ejecute
   varios comandos (usa `|`).

## Pasos sugeridos

1. Rama `cap01`, crea el archivo, `commit` y `push`.
2. En **Actions**, observa que **los dos jobs corren en paralelo**.
3. Abre cada job y revisa los logs de cada step.

## Criterios de evaluación

**Deterministas (60 %)**

- Define `name`.
- Dispara en `push` y en `pull_request`.
- Tiene ≥ 2 jobs.
- Corre en `ubuntu`.
- Usa `actions/checkout`.
- Tiene al menos un step `run`.

**Juez LLM (40 %)** — organización de jobs/steps, nombres claros y uso idiomático
de checkout y de comandos multilínea.

## Pista

Recuerda que cada job arranca en una máquina limpia: si `reportar` necesita el
código, también debe hacer su propio `checkout`.

> Solución: `solucion/cap01-anatomia.yml`.
