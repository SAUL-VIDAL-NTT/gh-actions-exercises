# Capítulo 04 · Control de flujo en jobs

Por defecto los jobs corren en paralelo y los steps en serie. Aquí aprendes a
**ordenar**, **multiplicar** y **condicionar** ese trabajo.

## Dependencias entre jobs: `needs`

`needs` hace que un job espere a que otro(s) terminen con éxito:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [ ... ]
  test:
    needs: build            # test no arranca hasta que build termine OK
    runs-on: ubuntu-latest
    steps: [ ... ]
  deploy:
    needs: [build, test]    # espera a varios
    runs-on: ubuntu-latest
    steps: [ ... ]
```

## Salidas entre jobs: `outputs` + `needs`

Como cada job corre en un runner distinto, para pasar datos se declaran `outputs`
del job (alimentados por una salida de step) y se leen con `needs`:

```yaml
jobs:
  preparar:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.v.outputs.version }}
    steps:
      - id: v
        run: echo "version=1.4.0" >> "$GITHUB_OUTPUT"
  usar:
    needs: preparar
    runs-on: ubuntu-latest
    steps:
      - run: echo "Versión recibida: ${{ needs.preparar.outputs.version }}"
```

## Matrices: `strategy.matrix`

Una **matriz** ejecuta el mismo job varias veces con combinaciones de valores.
Ideal para probar en varias versiones/sistemas:

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false           # no cancela el resto si una combinación falla
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [18, 20, 22]
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

Eso genera 2 × 3 = **6 jobs**. Opciones útiles:
- `fail-fast: true` (por defecto) cancela las demás combinaciones si una falla.
- `max-parallel: N` limita cuántas corren a la vez.
- `include` / `exclude` añaden o quitan combinaciones concretas.

## Condicionales: `if`

`if` decide si un job o un step se ejecuta. Dentro de `if`, las expresiones no
necesitan `${{ }}` (es opcional):

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'   # solo en main
    runs-on: ubuntu-latest
    steps:
      - name: Paso solo en push
        if: github.event_name == 'push'
        run: echo "Desplegando…"
```

### Funciones de estado

Útiles en `if` de steps para reaccionar al resultado previo:

- `success()` — verdadero si todo fue bien hasta aquí (implícito por defecto).
- `failure()` — verdadero si algo falló.
- `always()` — se ejecuta siempre, incluso tras un fallo (ideal para limpieza/reportes).
- `cancelled()` — si el run fue cancelado.

```yaml
- name: Subir logs aunque falle
  if: always()
  uses: actions/upload-artifact@v4
  with: { name: logs, path: logs/ }
```

## `continue-on-error`

Permite que un step (o job) **falle sin tumbar** el run:

```yaml
- run: ./paso-opcional.sh
  continue-on-error: true
```

## Fuentes oficiales

- Usar `needs` y dependencias — https://docs.github.com/en/actions/using-jobs/using-jobs-in-a-workflow
- Matrices — https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs
- `jobs.<id>.outputs` — https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs
- Expresiones y funciones de estado — https://docs.github.com/en/actions/learn-github-actions/expressions
