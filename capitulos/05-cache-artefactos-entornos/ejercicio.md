# Ejercicio 05 · Caché, artefactos y concurrencia

## Objetivo

Persistir y compartir archivos entre jobs, cachear dependencias y serializar runs.

## Tarea

Crea **`.github/workflows/cap05-datos.yml`** que:

1. Tenga `name` y se dispare en `push`.
2. Declare un bloque **`concurrency`** (con `cancel-in-progress`).
3. Tenga un job `build` que:
   - Use **`actions/cache`** (o una `setup-*` con `cache:`).
   - Genere un archivo y lo suba con **`actions/upload-artifact`**.
4. Tenga un job `consumir` que **dependa** (`needs`) de `build` y descargue el
   artefacto con **`actions/download-artifact`** y lo use.

## Criterios de evaluación

**Deterministas (60 %)**

- `name` y disparo en `push`.
- Define `concurrency`.
- Usa `actions/cache`.
- Usa `actions/upload-artifact`.
- Usa `actions/download-artifact`.
- Encadena con `needs`.

**Juez LLM (40 %)** — claves de caché razonables (con `hashFiles`), separación
correcta build/consumo y nombres de artefacto consistentes entre upload y download.

## Pista

La `key` de caché suele combinar el SO y un hash del archivo de dependencias:
`key: pip-${{ runner.os }}-${{ hashFiles('**/requirements.txt') }}`.

> Solución: `solucion/cap05-datos.yml`.
