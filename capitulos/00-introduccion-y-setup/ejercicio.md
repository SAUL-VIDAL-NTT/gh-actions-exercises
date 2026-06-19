# Ejercicio 00 · Tu primer workflow

## Objetivo

Crear y ejecutar tu primer workflow, y comprobar que el evaluador del curso funciona.

## Tarea

Crea el archivo **`.github/workflows/cap00-hola.yml`** con un workflow que:

1. Tenga un `name` descriptivo.
2. Se dispare **tanto** con `push` **como** de forma manual (`workflow_dispatch`).
3. Tenga un job que corra en un runner **Ubuntu**.
4. Incluya al menos un step que ejecute un comando (`run`) e imprima un saludo.

## Pasos sugeridos

1. Crea una rama: `git checkout -b cap00`.
2. Crea el archivo `.github/workflows/cap00-hola.yml`.
3. `git add`, `git commit`, `git push`.
4. (Opcional pero recomendado) abre un Pull Request hacia `main`.
5. Ve a la pestaña **Actions**:
   - Verás ejecutarse tu workflow `cap00-hola`.
   - Verás ejecutarse el **Evaluador del curso**: abre su run y mira el **Summary**.
6. Prueba el disparo manual: en **Actions → tu workflow → Run workflow**.

## Criterios de evaluación

**Deterministas (60 %)**

- ✅ Define `name`.
- ✅ Se dispara en `push`.
- ✅ Se dispara en `workflow_dispatch`.
- ✅ Tiene al menos 1 job.
- ✅ El job corre en `ubuntu`.
- ✅ Hay al menos un step con `run`.

**Juez LLM (40 %)** — valora claridad de nombres, legibilidad y que el workflow
realmente cumpla el enunciado de forma idiomática.

## Pista

Revisa el ejemplo de la teoría. Para el disparo manual, recuerda que `on` puede ser
un mapa con varias claves:

```yaml
on:
  push:
  workflow_dispatch:
```

> ¿Atascado? Mira `solucion/cap00-hola.yml` **después** de intentarlo.
