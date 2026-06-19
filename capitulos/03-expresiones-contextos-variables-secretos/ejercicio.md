# Ejercicio 03 · Expresiones, contextos, variables y secretos

## Objetivo

Manejar expresiones `${{ }}`, contextos, variables de entorno, secretos y salidas
entre steps.

## Tarea

Crea **`.github/workflows/cap03-contextos.yml`** que:

1. Tenga `name` y se dispare en `push`.
2. Defina un bloque **`env`** (a nivel workflow o job) con al menos una variable.
3. Use al menos una **expresión `${{ }}`** que lea el **contexto `github`**
   (p.ej. imprimir `${{ github.actor }}` o `${{ github.ref_name }}`).
4. Genere una **salida de step** escribiendo en `$GITHUB_OUTPUT` y la **consuma**
   en otro step vía `steps.<id>.outputs.<nombre>`.
5. Referencie un **secreto o una variable de configuración** (`secrets.*` o
   `vars.*`). Puede ser `secrets.GITHUB_TOKEN`, que siempre existe.

> 🔒 No imprimas el valor del secreto: pásalo por `env:` o úsalo en un comando.

## Preparación opcional

Para probar `vars`/`secrets` propios: en tu repo → **Settings → Secrets and
variables → Actions**, crea una variable (p.ej. `SALUDO`) o un secreto de prueba.

## Criterios de evaluación

**Deterministas (60 %)**

- `name` y disparo en `push`.
- Define `env`.
- Usa una expresión `${{ }}`.
- Lee el contexto `github.`.
- Usa `$GITHUB_OUTPUT` para una salida de step.
- Referencia `secrets.*` o `vars.*`.

**Juez LLM (40 %)** — manejo correcto/seguro de secretos (sin imprimirlos), uso
idiomático de contextos y claridad del flujo de datos entre steps.

> Solución: `solucion/cap03-contextos.yml`.
