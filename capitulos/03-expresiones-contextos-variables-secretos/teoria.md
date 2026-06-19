# Capítulo 03 · Expresiones, contextos, variables y secretos

## Expresiones `${{ }}`

GitHub Actions evalúa **expresiones** dentro de `${{ ... }}`. Sirven para inyectar
valores dinámicos, leer contextos y construir condiciones:

```yaml
run: echo "Rama actual: ${{ github.ref_name }}"
if: ${{ github.event_name == 'push' }}
```

Operadores: `==`, `!=`, `&&`, `||`, `!`, y funciones como `contains()`,
`startsWith()`, `format()`, `toJSON()`, `fromJSON()`, `hashFiles()`.

## Contextos

Los **contextos** son objetos con información del run. Los más usados:

| Contexto | Contiene | Ejemplo |
|----------|----------|---------|
| `github` | Datos del evento y del repo | `github.sha`, `github.actor`, `github.event_name`, `github.ref_name` |
| `env` | Variables de entorno definidas con `env:` | `env.MI_VAR` |
| `vars` | **Variables de configuración** del repo/entorno | `vars.REGION` |
| `secrets` | **Secretos** del repo/entorno | `secrets.API_TOKEN`, `secrets.GITHUB_TOKEN` |
| `job` / `steps` | Estado y salidas | `steps.<id>.outputs.<nombre>` |
| `matrix` / `needs` | Valores de matriz y de jobs previos | `matrix.version`, `needs.build.outputs.x` |
| `runner` | Datos del runner | `runner.os`, `runner.temp` |

## Variables: `env` vs `vars`

- **`env`**: variables de entorno. Se definen en el workflow y aplican a todo el
  workflow, a un job o a un step (el nivel más específico gana):

  ```yaml
  env:
    APP: demo            # nivel workflow
  jobs:
    build:
      env:
        APP: demo-build  # sobreescribe en el job
      steps:
        - run: echo "$APP"          # como variable de shell
        - run: echo "${{ env.APP }}" # como expresión
  ```

- **`vars`**: **variables de configuración** que defines en la web del repo
  (Settings → Secrets and variables → Actions → Variables). No son secretas. Se
  leen con `${{ vars.NOMBRE }}`.

## Secretos

Los **secretos** guardan datos sensibles (tokens, contraseñas). Se definen en
Settings → Secrets and variables → Actions → Secrets, y se leen con
`${{ secrets.NOMBRE }}`:

```yaml
steps:
  - run: ./deploy.sh
    env:
      TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

Reglas clave:
- GitHub **enmascara** los secretos en los logs (aparecen como `***`).
- **Nunca** los imprimas ni los pases por `run: echo`.
- No están disponibles para PRs desde forks (por seguridad).

### El secreto especial: `GITHUB_TOKEN`

En cada run, GitHub crea automáticamente `secrets.GITHUB_TOKEN`, un token de
instalación con permisos sobre **tu** repo (ver cap. 07 para ajustarlos). Sirve
para llamar a la API de GitHub sin configurar nada:

```yaml
run: gh issue list
env:
  GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Salidas entre steps: `$GITHUB_OUTPUT`

Para pasar datos de un step a otro, escribe en el archivo `$GITHUB_OUTPUT`:

```yaml
steps:
  - id: calc
    run: echo "resultado=42" >> "$GITHUB_OUTPUT"
  - run: echo "El resultado fue ${{ steps.calc.outputs.resultado }}"
```

Para pasar datos **entre jobs** se usan `outputs` del job + `needs` (cap. 04).

## Variables de entorno por defecto

GitHub define muchas variables listas para usar en `run`: `GITHUB_REPOSITORY`,
`GITHUB_SHA`, `GITHUB_REF_NAME`, `GITHUB_WORKSPACE`, `RUNNER_OS`, etc.

## Fuentes oficiales

- Contextos — https://docs.github.com/en/actions/learn-github-actions/contexts
- Expresiones — https://docs.github.com/en/actions/learn-github-actions/expressions
- Variables (incl. `vars` y por defecto) — https://docs.github.com/en/actions/learn-github-actions/variables
- Uso de secretos — https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions
- `GITHUB_TOKEN` — https://docs.github.com/en/actions/security-guides/automatic-token-authentication
