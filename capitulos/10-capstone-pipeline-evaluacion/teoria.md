# Capítulo 10 · Capstone: pipeline de evaluación de skills

Aquí unes todo: construyes un **pipeline de evaluación** que combina pruebas
**deterministas** y un **juez LLM**, calcula una nota ponderada, la **reporta** y
opcionalmente **bloquea** la integración. Es, en esencia, el mismo diseño que el
evaluador del curso ([`.github/workflows/00-evaluador.yml`](../../.github/workflows/00-evaluador.yml)).

## Arquitectura de referencia

```
on: pull_request
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ Job: evaluar  (permissions: contents:read, models:read,    │
│                pull-requests:write)                        │
│                                                            │
│  1) Determinista → script de aserciones → puntaje objetivo │
│  2) Juez LLM     → actions/ai-inference  → puntaje semántico│
│  3) Combinar     → nota = w1·det + w2·juez                 │
│  4) Reportar     → $GITHUB_STEP_SUMMARY + comentario en PR │
│  5) (opcional) Gate → exit ≠ 0 si nota < umbral            │
└──────────────────────────────────────────────────────────┘
```

## Decisiones de diseño clave

### Ponderación
Asigna pesos explícitos. Lo determinista debe pesar lo suficiente para que la nota
no dependa solo del LLM (estocástico). En el curso: **60 % determinista / 40 % juez**.

### Degradación elegante
Si GitHub Models no está disponible, **no rompas** el pipeline: usa
`continue-on-error: true` en el step del juez y calcula la nota con lo determinista,
avisando en el reporte. (Ver `evaluador/combinar.py`.)

### Reporte accionable
Publica **qué** falló y **por qué**. Combina:
- `$GITHUB_STEP_SUMMARY` para el detalle del run.
- Un **comentario en el PR** (con `actions/github-script` o el CLI `gh`) para que el
  feedback llegue donde se trabaja.

### Idempotencia del comentario (mejora)
Para no llenar el PR de comentarios, busca uno previo del bot y **actualízalo** en
vez de crear uno nuevo (con `github.rest.issues.listComments` + `updateComment`).

### El gate
Convierte la nota en decisión: `exit 1` si `nota < umbral`, y marca el workflow como
**required status check** para bloquear el merge (cap. 08).

## Calibración y confianza

- **Valida tu juez**: prueba con entregas buenas y malas conocidas; ajusta rúbrica y
  pesos hasta que las notas sean razonables.
- **Auditabilidad**: guarda como **artefacto** las entradas y salidas (rúbrica,
  prompt, respuesta cruda del modelo, JSON de nota). Permite revisar reclamaciones.
- **Humano en el bucle**: para decisiones importantes, el pipeline informa; la
  persona decide. El LLM as a Judge es una **señal**, no un veredicto inapelable.

## El reto

Construirás un pipeline que evalúa la calidad de un Pull Request (o de un archivo)
combinando ambas señales y dejando feedback en el propio PR. Con eso, cierras el
círculo: **sabes usar GitHub Actions y sabes construir evaluaciones de skills**
deterministas y semánticas sobre él.

## Fuentes oficiales

- `actions/github-script` — https://github.com/actions/github-script
- API REST de comentarios de issues/PR — https://docs.github.com/en/rest/issues/comments
- `actions/ai-inference` — https://github.com/actions/ai-inference
- Resúmenes y comandos de workflow — https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
- Status checks requeridos — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
