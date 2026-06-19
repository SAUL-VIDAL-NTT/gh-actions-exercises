# Capítulo 01 · Anatomía de un workflow

Ya viste un workflow mínimo. Ahora desglosamos cada parte.

## 1. Disparadores: `on`

`on` define **qué eventos** ejecutan el workflow. Puede ser un evento, una lista o
un mapa con configuración fina:

```yaml
on: push                       # un evento

on: [push, pull_request]       # varios eventos

on:                            # mapa con filtros
  push:
    branches: [main]
    paths: ["src/**"]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 6 * * 1"        # lunes a las 06:00 UTC
  workflow_dispatch:           # disparo manual desde la UI
```

Eventos habituales: `push`, `pull_request`, `schedule`, `workflow_dispatch`
(manual), `workflow_call` (reutilizable), `issues`, `release`, etc.

## 2. Jobs

Un workflow tiene uno o más **jobs**. Por defecto **se ejecutan en paralelo** y
cada uno en su propio runner (máquina limpia). Cada job tiene un **id** (la clave):

```yaml
jobs:
  build:                 # id del job
    runs-on: ubuntu-latest
    steps: [ ... ]
  test:
    runs-on: ubuntu-latest
    steps: [ ... ]
```

Para encadenarlos se usa `needs` (capítulo 04).

## 3. `runs-on`: el runner

Indica el sistema de la máquina que ejecuta el job. Etiquetas comunes de runners
alojados por GitHub:

- `ubuntu-latest` (Linux, el más usado y rápido de arrancar)
- `windows-latest`
- `macos-latest`

```yaml
runs-on: ubuntu-latest
```

## 4. Steps

Cada job tiene una lista de **steps** que se ejecutan **en orden**, en el mismo
runner (comparten el sistema de archivos). Un step hace **una de dos cosas**:

```yaml
steps:
  - name: Clonar el repo          # step que USA una acción
    uses: actions/checkout@v4

  - name: Ejecutar comandos       # step que CORRE comandos de shell
    run: |
      echo "Línea 1"
      echo "Línea 2"
```

- `uses`: invoca una **acción** reutilizable (ver capítulo 02).
- `run`: ejecuta comandos en la shell del runner. Con `|` puedes poner varias líneas.
- `name`: etiqueta legible (opcional pero muy recomendable).

> 💡 `actions/checkout` es casi siempre el primer step: descarga tu repositorio
> en el runner. Sin él, el runner no tiene tu código.

## 5. El ciclo de vida de un run

```
evento (push) → GitHub lee .github/workflows/*.yml → crea un RUN
   → por cada job: arranca un runner limpio
       → ejecuta los steps en orden
   → reporta éxito/fallo en la pestaña Actions
```

Si **cualquier step falla** (código de salida ≠ 0), el job falla y los steps
siguientes no se ejecutan (salvo que uses `if:` o `continue-on-error`, cap. 04).

## Fuentes oficiales

- Sintaxis de workflows (`on`, `jobs`, `steps`, `runs-on`) — https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- Eventos que disparan workflows — https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows
- `actions/checkout` — https://github.com/actions/checkout
