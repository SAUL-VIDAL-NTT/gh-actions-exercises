# Curso rápido de GitHub Actions con evaluación de skills

Curso práctico y autocontenido para aprender **GitHub Actions** desde cero, pensado
para practicarse en **tu cuenta personal de GitHub**. Cada capítulo combina:

- **Teoría** breve y directa (`teoria.md`), 100 % basada en documentación oficial.
- Un **ejercicio práctico** (`ejercicio.md`) con un entregable concreto.
- **Evaluación automática de tus skills** mediante dos mecanismos complementarios:
  - **Pruebas deterministas**: análisis estructural de tu workflow (¿dispara en el
    evento correcto?, ¿declara permisos mínimos?, ¿usa la acción pedida?, etc.).
  - **Evaluación semántica tipo _LLM as a Judge_**: un modelo de
    [GitHub Models](https://docs.github.com/en/github-models) califica tu entrega
    contra una rúbrica (buenas prácticas, seguridad, claridad) usando la acción
    oficial [`actions/ai-inference`](https://github.com/actions/ai-inference).

> Todo el contenido se apoya exclusivamente en fuentes oficiales: GitHub Docs,
> los repositorios oficiales `actions/*` y GitHub Models. Cada `teoria.md` cierra
> con su sección **Fuentes oficiales**.

---

## ¿Cómo funciona la calificación? (visión general)

```
 Tu entrega (.github/workflows/capNN-*.yml)
            │
            ▼
 ┌─────────────────────────────────────────────┐
 │  Workflow evaluador  (.github/workflows/     │
 │            00-evaluador.yml)                 │
 │                                              │
 │  1) Determinista  → evaluador/calificar.py   │  → resultado-determinista.json
 │  2) LLM as a Judge → actions/ai-inference    │  → resultado-juez.json
 │  3) Combinación   → evaluador/combinar.py    │  → nota final + reporte
 └─────────────────────────────────────────────┘
            │
            ▼
 Resumen en la pestaña "Summary" del run + (en PRs) comentario con tu nota
```

La nota final por defecto pondera **60 % determinista + 40 % juez LLM** (configurable
por capítulo en su `evaluacion/criterios.json`).

---

## Requisitos previos

1. Una **cuenta personal de GitHub** (gratuita sirve).
2. Conocer lo mínimo de **Git** (clonar, commit, push) — o usar la edición web de GitHub.
3. Para la parte de LLM as a Judge: acceso a **GitHub Models** (incluido en cuentas
   personales con límites de uso gratuitos). No necesitas claves de API externas:
   el modelo se invoca con el `GITHUB_TOKEN` del propio workflow y el permiso
   `models: read`.

No necesitas instalar nada en tu máquina: todo corre en los _runners_ de GitHub.
Opcionalmente, para trabajar en local, te ayuda tener Python 3 y el
[CLI `gh`](https://cli.github.com/).

---

## Puesta en marcha (5 minutos)

1. Crea un repositorio **nuevo y privado** (o público) en tu cuenta, p. ej. `gha-curso`.
2. Copia el contenido de esta carpeta a la raíz de tu repo y haz `push`.
   (Incluye la carpeta `.github/`, `evaluador/` y `capitulos/`.)
3. Ve a la pestaña **Actions** de tu repo y, si te lo pide, habilita los workflows.
4. Verifica que GitHub Models está disponible: la primera vez que se ejecute el
   capítulo 9, el run te dirá si falta habilitarlo (ver `capitulos/09-llm-as-a-judge`).
5. Empieza por `capitulos/00-introduccion-y-setup/`.

> 💡 Consejo: trabaja **un capítulo por rama** y abre un Pull Request hacia `main`.
> Así recibes la nota como comentario en el PR y practicas el flujo real de trabajo.

---

## Índice de capítulos

| Nº | Capítulo | Aprendes a… |
|----|----------|-------------|
| 00 | [Introducción y setup](capitulos/00-introduccion-y-setup/teoria.md) | Entender qué es Actions y ejecutar tu primer workflow |
| 01 | [Anatomía de un workflow](capitulos/01-anatomia-workflow/teoria.md) | `on`, `jobs`, `steps`, `runs-on`, runners |
| 02 | [Acciones y Marketplace](capitulos/02-acciones-y-marketplace/teoria.md) | `uses`, `with`, `checkout`, `setup-*`, versionado |
| 03 | [Expresiones, contextos, variables y secretos](capitulos/03-expresiones-contextos-variables-secretos/teoria.md) | `${{ }}`, contextos, `env`, `vars`, `secrets` |
| 04 | [Control de flujo en jobs](capitulos/04-jobs-matrix-dependencias-condicionales/teoria.md) | `needs`, `matrix`, `if`, `outputs`, `fail-fast` |
| 05 | [Caché, artefactos y entornos](capitulos/05-cache-artefactos-entornos/teoria.md) | `cache`, `upload/download-artifact`, `environments`, `concurrency` |
| 06 | [Reutilización: composite y reusable workflows](capitulos/06-reutilizacion-composite-reusable/teoria.md) | `workflow_call`, composite actions |
| 07 | [Seguridad: permisos, OIDC y pinning](capitulos/07-seguridad-permisos-oidc/teoria.md) | Permisos mínimos, OIDC, fijar acciones por SHA |
| 08 | [Evaluaciones deterministas](capitulos/08-evaluaciones-deterministicas/teoria.md) | Construir gates de CI: lint, tests y aserciones |
| 09 | [LLM as a Judge](capitulos/09-llm-as-a-judge/teoria.md) | Evaluar semánticamente con GitHub Models + rúbricas |
| 10 | [Capstone: pipeline de evaluación](capitulos/10-capstone-pipeline-evaluacion/teoria.md) | Unir determinista + juez LLM en un pipeline real |

---

## Estructura del repositorio

```
.
├── README.md                     ← este archivo
├── .github/
│   └── workflows/
│       └── 00-evaluador.yml       ← workflow que califica tus entregas
├── evaluador/                     ← el "motor" de evaluación del curso
│   ├── calificar.py               ← evaluación determinista (estructural)
│   ├── combinar.py                ← combina determinista + juez → nota final
│   ├── llm-judge/
│   │   └── juez.system.md         ← instrucciones (system prompt) del juez
│   └── README.md
├── capitulos/
│   ├── 00-introduccion-y-setup/
│   │   ├── teoria.md
│   │   ├── ejercicio.md
│   │   ├── evaluacion/criterios.json
│   │   └── solucion/              ← solución de referencia
│   └── ...
└── entregas/                      ← (opcional) borradores antes de pasarlos a .github/workflows
```

---

## Cómo entregar cada ejercicio

1. Lee `teoria.md` y `ejercicio.md` del capítulo.
2. Crea el archivo pedido en `.github/workflows/` con el nombre exacto indicado
   (p. ej. `capitulos/01-anatomia-workflow/ejercicio.md` te pide
   `.github/workflows/cap01-anatomia.yml`).
3. Haz `commit` y `push` (idealmente en una rama + PR).
4. El workflow `00-evaluador.yml` se ejecuta solo, detecta qué capítulo cambió y
   publica tu nota en **Actions → Summary** (y como comentario si es un PR).
5. Compara con `solucion/` solo después de intentarlo.

---

## Licencia y atribución

Material de estudio. Los textos se basan en documentación pública de GitHub
(GitHub Docs, repositorios `actions/*`, GitHub Models). Revisa siempre la fuente
oficial enlazada en cada capítulo, ya que el producto evoluciona.
