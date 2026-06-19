# Capítulo 06 · Reutilización: composite actions y reusable workflows

Cuando repites lógica entre repos o workflows, tienes dos herramientas oficiales
para no copiar y pegar: **composite actions** y **reusable workflows**.

## Reusable workflows (`workflow_call`)

Un **workflow reutilizable** es un workflow normal que se puede **llamar desde otro
workflow**. Se declara con el evento `workflow_call` y puede recibir `inputs`,
`secrets` y devolver `outputs`:

```yaml
# .github/workflows/ci-reutilizable.yml
name: CI reutilizable
on:
  workflow_call:
    inputs:
      entorno:
        required: true
        type: string
    secrets:
      token:
        required: false
    outputs:
      resultado:
        value: ${{ jobs.run.outputs.resultado }}

jobs:
  run:
    runs-on: ubuntu-latest
    outputs:
      resultado: ${{ steps.s.outputs.r }}
    steps:
      - id: s
        run: echo "r=ok-${{ inputs.entorno }}" >> "$GITHUB_OUTPUT"
```

Y se **llama** desde otro workflow con `uses` a nivel de **job**:

```yaml
# .github/workflows/llamador.yml
on: [push]
jobs:
  llamar:
    uses: ./.github/workflows/ci-reutilizable.yml   # mismo repo
    with:
      entorno: staging
    secrets:
      token: ${{ secrets.MI_TOKEN }}
```

> Para llamar a uno de **otro** repo: `usuario/repo/.github/workflows/x.yml@v1`.

## Composite actions

Una **composite action** empaqueta varios steps en una sola acción reutilizable.
Vive en su propia carpeta con un `action.yml`:

```yaml
# .github/actions/saludar/action.yml
name: Saludar
description: Imprime un saludo personalizado
inputs:
  nombre:
    description: A quién saludar
    required: true
    default: mundo
outputs:
  mensaje:
    description: El saludo generado
    value: ${{ steps.gen.outputs.mensaje }}
runs:
  using: composite
  steps:
    - id: gen
      shell: bash
      run: echo "mensaje=Hola, ${{ inputs.nombre }}" >> "$GITHUB_OUTPUT"
```

Y se usa como cualquier acción:

```yaml
steps:
  - uses: ./.github/actions/saludar
    with:
      nombre: Ada
```

> ⚠️ En composite actions, **cada step `run` necesita `shell:`** (p.ej. `bash`).

## ¿Cuál elijo?

| Si quieres… | Usa |
|-------------|-----|
| Reutilizar **uno o varios jobs completos** (con sus runners, matrices, permisos) | **Reusable workflow** |
| Reutilizar **una secuencia de steps** dentro de un job | **Composite action** |

## Fuentes oficiales

- Reutilizar workflows (`workflow_call`) — https://docs.github.com/en/actions/using-workflows/reusing-workflows
- Crear una composite action — https://docs.github.com/en/actions/creating-actions/creating-a-composite-action
- Metadatos de acciones (`action.yml`) — https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions
