# Ejercicio 10 · Capstone: pipeline de evaluación completo

## Objetivo

Construir un pipeline que combine evaluación **determinista** y **juez LLM**,
calcule una nota y deje **feedback en el PR**.

## Tarea

Crea **`.github/workflows/cap10-pipeline.yml`** que:

1. Tenga `name` y se dispare en `pull_request` (y `workflow_dispatch`).
2. Tenga un job con `permissions`: **`contents: read`**, **`models: read`** y
   **`pull-requests: write`**.
3. Ejecute una **evaluación determinista** (un step `run` con aserciones o un
   pequeño script que produzca un puntaje).
4. Ejecute un **juez LLM** con `actions/ai-inference` (rúbrica + salida JSON).
5. **Combine** ambos puntajes en una nota final (puedes hacerlo con un step `run`
   en bash/python).
6. **Comente la nota en el PR** (con `actions/github-script` o `gh pr comment`).
7. Use `needs` para encadenar etapas (si separas en varios jobs) **o** un único
   job con steps ordenados.

> Puedes basarte en el evaluador del curso (`evaluador/*.py`) o escribir tu propia
> lógica más simple. Lo importante es que el pipeline produzca una nota combinada y
> la reporte.

## Criterios de evaluación

**Deterministas (60 %)**

- `name`; dispara en `pull_request`.
- `models: read` y `pull-requests: write`.
- Usa `actions/ai-inference`.
- Tiene steps `run` (lógica determinista / combinación).
- Encadena con `needs` **o** comenta en el PR.
- Publica un comentario en el PR (`github-script`/`gh`/createComment).

**Juez LLM (40 %)** — coherencia de la arquitectura (pesos explícitos, degradación
elegante si Models falla, reporte accionable, auditabilidad).

## Pista

Para comentar en el PR con `actions/github-script`:

```yaml
- uses: actions/github-script@v7
  with:
    script: |
      await github.rest.issues.createComment({
        owner: context.repo.owner, repo: context.repo.repo,
        issue_number: context.issue.number,
        body: `Nota final: ${process.env.NOTA}`,
      });
```

> Solución: `solucion/cap10-pipeline.yml`.
