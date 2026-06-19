# Capítulo 02 · Acciones y Marketplace

## ¿Qué es una acción?

Una **acción** (action) es una unidad de código reutilizable y empaquetada que
realiza una tarea concreta. En lugar de escribir scripts largos, reutilizas
acciones probadas. Se invocan con `uses`:

```yaml
- uses: actions/checkout@v4
```

Hay tres tipos: **JavaScript**, **Docker** y **composite** (las construyes en el
cap. 06). Tú las consumes desde [GitHub Marketplace](https://github.com/marketplace?type=actions)
o desde cualquier repositorio público.

## Sintaxis: `uses`, `with`, `env`

```yaml
- name: Configurar Node.js
  uses: actions/setup-node@v4     # propietario/repo@referencia
  with:                           # parámetros de ENTRADA de la acción
    node-version: "20"
    cache: "npm"
  env:                            # variables de entorno para ESTE step
    MI_VAR: valor
```

- `uses`: qué acción usar y en qué **versión/referencia**.
- `with`: las **entradas** (inputs) que la acción documenta.
- Las salidas de una acción se leen con `steps.<id>.outputs.<nombre>` (cap. 03).

## Referenciar versiones (¡importante!)

Puedes apuntar a:

| Forma | Ejemplo | Notas |
|-------|---------|-------|
| Etiqueta mayor | `@v4` | Recibe parches y minors de esa major. Cómodo. |
| Etiqueta exacta | `@v4.1.7` | Más estable, pero te pierdes parches. |
| Rama | `@main` | **Desaconsejado**: cambia sin avisar. |
| **SHA de commit** | `@a1b2c3...` | **Lo más seguro**: inmutable. Recomendado para terceros. |

> 🔒 Para acciones de **terceros**, fijar por **SHA** evita que una versión
> comprometida se ejecute en tu pipeline. Lo profundizamos en el capítulo 07.

## Acciones esenciales mantenidas por GitHub (`actions/*`)

| Acción | Para qué |
|--------|----------|
| `actions/checkout` | Clonar tu repositorio en el runner. |
| `actions/setup-node`, `setup-python`, `setup-java`, `setup-go`… | Instalar un runtime y su gestor de caché. |
| `actions/cache` | Cachear dependencias entre runs (cap. 05). |
| `actions/upload-artifact` / `download-artifact` | Guardar/recuperar archivos entre jobs (cap. 05). |
| `actions/github-script` | Ejecutar JavaScript con la API de GitHub ya autenticada. |

## Ejemplo: build de un proyecto Node

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-node@v4
    with:
      node-version: "20"
  - run: npm ci
  - run: npm test
```

`setup-node` deja `node` y `npm` disponibles para los `run` siguientes (recuerda:
los steps comparten el runner).

## Fuentes oficiales

- Encontrar y usar acciones — https://docs.github.com/en/actions/using-workflows/using-actions-in-a-workflow
- `actions/setup-node` — https://github.com/actions/setup-node
- `actions/setup-python` — https://github.com/actions/setup-python
- Marketplace de acciones — https://github.com/marketplace?type=actions
