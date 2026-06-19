# Capítulo 07 · Seguridad: permisos, OIDC y pinning

La seguridad en Actions se basa en **menor privilegio** y en **no confiar a ciegas**
en código de terceros. Tres pilares prácticos:

## 1. Permisos del `GITHUB_TOKEN`

Cada run recibe un `GITHUB_TOKEN`. Por defecto puede tener permisos amplios sobre
tu repo. Declara explícitamente **solo lo que necesitas** con `permissions`:

```yaml
permissions:
  contents: read          # leer el código (lo mínimo habitual)

jobs:
  publicar:
    permissions:
      contents: read
      packages: write     # este job sí puede publicar paquetes
    runs-on: ubuntu-latest
    steps: [ ... ]
```

- Puedes ponerlo a nivel **workflow** (aplica a todos los jobs) o por **job**.
- `permissions: {}` quita todos los permisos.
- Valores por scope: `read`, `write` o `none`. Scopes comunes: `contents`,
  `pull-requests`, `issues`, `packages`, `id-token`, `models`…

> 🔑 **Regla de oro**: empieza con `contents: read` y añade permisos uno a uno
> según los necesites.

## 2. OIDC: autenticación sin secretos de larga vida

Para desplegar en la nube (AWS, Azure, GCP…) lo tradicional era guardar claves
de larga duración como secretos. **OpenID Connect (OIDC)** lo evita: el workflow
solicita un **token JWT efímero** a GitHub, y el proveedor cloud —configurado para
**confiar** en GitHub como identidad federada— lo intercambia por credenciales
temporales.

Requisito en el workflow: el permiso `id-token: write`.

```yaml
permissions:
  id-token: write     # permite pedir el token OIDC
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      # La action oficial del proveedor cloud usa el OIDC para obtener
      # credenciales temporales (ejemplo conceptual con AWS):
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/mi-rol
          aws-region: eu-west-1
```

Ventajas: **sin secretos** que rotar o que se filtren, y credenciales de **corta
vida** ligadas a ese run.

## 3. Pinning: fija las acciones por SHA

Una acción de terceros referenciada por etiqueta (`@v3`) o rama (`@main`) puede
cambiar bajo tus pies —incluso ser comprometida—. Para código de terceros, **fija
por SHA de commit completo** (inmutable):

```yaml
# En vez de:  uses: alguien/accion@v3
- uses: alguien/accion@e3b0c44298fc1c149afbf4c8996fb92427ae41e4   # v3.1.0
```

Buenas prácticas adicionales de _hardening_:
- Evita `@main`/`@master` en acciones de terceros.
- Revisa qué hace una acción antes de darle permisos de escritura.
- Cuidado con `pull_request_target` y con `${{ }}` que interpola entradas no
  confiables dentro de `run` (riesgo de **inyección de scripts**): pásalas por `env`.
- Limita los secretos por entorno y no los expongas en PRs de forks.

```yaml
# Inyección evitada: la entrada va por env, no interpolada en el comando.
- env:
    TITULO: ${{ github.event.issue.title }}
  run: echo "$TITULO"
```

## Fuentes oficiales

- Asignar permisos a jobs — https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs
- Endurecer la seguridad — https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- OIDC (concepto) — https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- Autenticación automática (`GITHUB_TOKEN`) — https://docs.github.com/en/actions/security-guides/automatic-token-authentication
