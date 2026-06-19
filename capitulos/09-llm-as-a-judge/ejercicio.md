# Ejercicio 09 · Tu propio juez LLM

## Objetivo

Construir un workflow que use **GitHub Models** (vía `actions/ai-inference`) para
evaluar algo semánticamente contra una rúbrica y reportar el resultado.

## Requisito previo

GitHub Models debe estar disponible en tu cuenta. La primera vez, si el run falla
con un error de permisos/acceso a Models, revisa que:
- el job declara `permissions: models: read`, y
- tu cuenta tiene GitHub Models habilitado (es gratuito con límites de uso).

## Tarea

Crea **`.github/workflows/cap09-juez.yml`** que:

1. Tenga `name` y se dispare de forma manual (`workflow_dispatch`) y/o en `pull_request`.
2. Tenga un job con **`permissions: models: read`**.
3. Use **`actions/ai-inference`** con un **`system-prompt`** (rol de evaluador que
   responde **solo JSON**) y un **`prompt`** que incluya una **rúbrica** y el texto
   o código a evaluar.
4. Lea la salida (`steps.<id>.outputs.response`) y la escriba en
   **`$GITHUB_STEP_SUMMARY`**.

Idea concreta: evalúa la calidad del `README.md` de tu repo (claridad, completitud,
estructura) con una rúbrica de 2-3 criterios.

## Criterios de evaluación

**Deterministas (60 %)**

- `name`.
- El job declara `models: read`.
- Usa `actions/ai-inference`.
- Pasa un `system-prompt` y/o `prompt`.
- Lee `outputs.response`.
- Escribe en `$GITHUB_STEP_SUMMARY`.

**Juez LLM (40 %)** — calidad de tu rúbrica y de tu system prompt: ¿pide salida
estructurada (JSON)?, ¿criterios con pesos?, ¿maneja el caso de que Models falle
(`continue-on-error`)?

## Pista

```yaml
permissions:
  models: read
steps:
  - id: j
    uses: actions/ai-inference@v1
    with:
      model: openai/gpt-4o-mini
      system-prompt: |
        Eres un evaluador. Devuelve SOLO JSON: {"puntuacion":0-100,"comentario":"..."}
      prompt: |
        Rúbrica: claridad (50), completitud (50).
        Evalúa este README:
        ...
  - run: echo "${{ steps.j.outputs.response }}" >> "$GITHUB_STEP_SUMMARY"
```

> Solución: `solucion/cap09-juez.yml`.
