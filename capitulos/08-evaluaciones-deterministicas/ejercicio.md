# Ejercicio 08 · Construye tu propio gate determinista

## Objetivo

Crear un workflow que **evalúe** algo de forma determinista: corre aserciones,
falla si no se cumplen y publica un resumen.

## Tarea

Crea **`.github/workflows/cap08-gate.yml`** que:

1. Tenga `name` y se dispare en `push` **y** `pull_request`.
2. Tenga un step que ejecute **aserciones** (usa `set -e` y comandos como `test`,
   `grep -q`, comparaciones `[ ... ]`…) de modo que **falle** si no se cumplen.
3. Escriba un **resumen** en `$GITHUB_STEP_SUMMARY`.
4. Suba un **artefacto** con el reporte (`actions/upload-artifact`).

Idea concreta: valida tu propio repo. Por ejemplo, aserta que existe `README.md`,
que contiene la palabra "Actions", y deja constancia en el resumen.

## Pasos sugeridos

1. Rama `cap08`, crea el archivo, `push`.
2. Provoca un fallo a propósito (cambia una aserción) y observa cómo el job se
   pone en rojo. Luego arréglalo.

## Criterios de evaluación

**Deterministas (60 %)**

- `name`; dispara en `pull_request`.
- Tiene steps `run`.
- Escribe en `$GITHUB_STEP_SUMMARY`.
- Incluye aserciones reales (`set -e`, `test`, `grep`, `[ ... ]`…).
- Sube un artefacto.

**Juez LLM (40 %)** — calidad de las aserciones (¿prueban algo significativo?),
claridad del resumen y manejo correcto de fallos.

## Pista

```yaml
- name: Aserciones
  run: |
    set -e
    test -f README.md
    grep -q "Actions" README.md
    echo "## Gate ✅" >> "$GITHUB_STEP_SUMMARY"
```

> Solución: `solucion/cap08-gate.yml`.
