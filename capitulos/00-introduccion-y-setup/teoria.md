# Capítulo 00 · Introducción y setup

## ¿Qué es GitHub Actions?

GitHub Actions es la plataforma de **integración y entrega continua (CI/CD)** y de
**automatización** integrada en GitHub. Te permite ejecutar procesos automáticos
(compilar, testear, desplegar, etiquetar issues, publicar paquetes…) en respuesta
a **eventos** que ocurren en tu repositorio: un `push`, un Pull Request, un
calendario (`schedule`), o un disparo manual.

Conceptos clave (los veremos en detalle en los próximos capítulos):

| Concepto | Qué es |
|----------|--------|
| **Workflow** | Un proceso automatizado, definido en un archivo YAML dentro de `.github/workflows/`. |
| **Evento** (`on`) | Lo que dispara el workflow (push, pull_request, schedule, workflow_dispatch…). |
| **Job** | Un conjunto de pasos que se ejecutan en un mismo _runner_. Por defecto, los jobs corren en paralelo. |
| **Step** | Un paso individual: o ejecuta un comando de shell (`run`) o usa una **acción** (`uses`). |
| **Action** | Una unidad de código reutilizable y empaquetada (p.ej. `actions/checkout`). |
| **Runner** | La máquina (Linux, Windows o macOS) que ejecuta el job. GitHub ofrece runners alojados. |

## Anatomía mínima de un workflow

Los workflows viven **siempre** en `.github/workflows/` en la raíz del repo, con
extensión `.yml` o `.yaml`:

```yaml
name: Hola Mundo            # nombre visible en la pestaña Actions
on: [push]                  # cuándo se ejecuta
jobs:
  saludar:                  # id del job
    runs-on: ubuntu-latest  # tipo de runner
    steps:
      - name: Saludar
        run: echo "¡Hola, GitHub Actions!"
```

Cada vez que hagas `push`, GitHub detecta el archivo, crea un **run** del workflow
y lo verás en la pestaña **Actions** de tu repositorio.

## YAML en 2 minutos

GitHub Actions se configura en [YAML](https://yaml.org/). Lo esencial:

- La **indentación con espacios** (no tabuladores) define la jerarquía.
- Pares `clave: valor`. Las listas usan `-`.
- Cadenas pueden ir con o sin comillas; usa comillas si hay caracteres especiales.
- Comentarios con `#`.

```yaml
clave: valor
lista:
  - elemento1
  - elemento2
objeto:
  subclave: subvalor
```

> ⚠️ **Trampa clásica:** la clave `on:` es interpretada por algunos analizadores
> YAML como el booleano `true` (por la norma YAML 1.1). GitHub lo maneja bien, pero
> tenlo presente si procesas el YAML con tus propias herramientas.

## Cómo funciona la evaluación de este curso

Cuando entregues un ejercicio (creando el archivo de workflow pedido y haciendo
`push`), el workflow `00-evaluador.yml` te calificará con:

1. **Pruebas deterministas** — comprueban hechos: ¿se dispara en el evento correcto?,
   ¿declara un job?, ¿usa la acción pedida?
2. **Juez LLM** — un modelo de GitHub Models valora la **calidad** de tu solución
   contra una rúbrica.

La nota aparece en **Actions → (tu run) → Summary**, y como comentario si trabajas
con Pull Requests.

## Fuentes oficiales

- Qué es GitHub Actions — https://docs.github.com/en/actions/about-github-actions/understanding-github-actions
- Inicio rápido — https://docs.github.com/en/actions/quickstart
- Sintaxis de workflows — https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- Runners alojados por GitHub — https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners
