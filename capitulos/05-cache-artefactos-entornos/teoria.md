# Capítulo 05 · Caché, artefactos, entornos y concurrencia

## Caché de dependencias: `actions/cache`

Cachear dependencias (node_modules, pip, etc.) acelera mucho los runs. La acción
`actions/cache` guarda y restaura un directorio según una **clave** (`key`):

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      pip-${{ runner.os }}-
```

- `key`: si coincide exactamente, hay **cache hit** y se restaura.
- `restore-keys`: claves de respaldo (prefijos) para un hit parcial.
- `hashFiles(...)`: cambia la clave cuando cambian las dependencias, invalidando
  la caché de forma controlada.

> 💡 Muchas acciones `setup-*` traen caché integrada: `actions/setup-node` con
> `cache: npm`, o `setup-python` con `cache: pip`. Suele bastar con eso.

## Artefactos: `upload-artifact` / `download-artifact`

Los **artefactos** persisten archivos **del run** (informes, binarios, logs) y
permiten **pasar archivos entre jobs**. Cada job tiene un sistema de archivos
propio, así que se sube en uno y se descarga en otro:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: mkdir dist && echo "ok" > dist/app.txt
      - uses: actions/upload-artifact@v4
        with:
          name: app
          path: dist/

  publicar:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: app
      - run: cat app.txt
```

Diferencia clave: **caché** optimiza velocidad entre runs; **artefactos** entregan
resultados de un run (y se pueden descargar desde la UI).

## Entornos: `environment`

Un **environment** (Settings → Environments) agrupa configuración y reglas de
protección para despliegues: secretos/variables propios, **revisores requeridos**,
ramas permitidas y tiempos de espera.

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production      # aplica reglas de protección de ese entorno
    steps:
      - run: ./deploy.sh
```

Si `production` exige aprobación manual, el job **se pausa** hasta que un revisor
lo apruebe.

## Concurrencia: `concurrency`

Evita ejecuciones simultáneas que se pisan (p.ej. varios despliegues a la vez).
Los runs del mismo **grupo** se serializan, y puedes cancelar los antiguos:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true       # cancela runs anteriores del mismo grupo
```

Muy útil en PRs: al hacer push nuevo, cancela el run anterior de esa rama.

## Fuentes oficiales

- Caché de dependencias — https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows
- Artefactos — https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts
- Entornos de despliegue — https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
- Concurrencia — https://docs.github.com/en/actions/using-jobs/using-concurrency
