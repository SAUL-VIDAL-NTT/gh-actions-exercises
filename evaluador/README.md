# Motor de evaluación del curso

Esta carpeta contiene el sistema que califica tus entregas. Está pensado también
como material de estudio (lo construyes tú mismo en los capítulos 8, 9 y 10).

## Piezas

| Archivo | Rol |
|---------|-----|
| `descubrir.py` | Detecta qué capítulos tienen entrega y arma la matriz del workflow. |
| `calificar.py` | **Evaluación determinista**: analiza la estructura del workflow YAML contra `criterios.json`. |
| `preparar_juez.py` | Construye el _prompt_ del juez combinando la rúbrica + tu entrega. |
| `llm-judge/juez.system.md` | _System prompt_ del juez (instrucciones y formato JSON de salida). |
| `combinar.py` | **Combina** determinista + juez y calcula la **nota final**. |

El workflow que lo orquesta es [`.github/workflows/00-evaluador.yml`](../.github/workflows/00-evaluador.yml).

## El contrato: `criterios.json`

Cada capítulo evaluable tiene `capitulos/<cap>/evaluacion/criterios.json`:

```json
{
  "capitulo": "01",
  "archivo_entrega": ".github/workflows/cap01-anatomia.yml",
  "peso_determinista": 0.6,
  "peso_juez": 0.4,
  "aprobado_min": 70,
  "checks": [
    { "id": "trigger-push", "tipo": "trigger", "valor": "push", "puntos": 20, "desc": "Se dispara en push" }
  ],
  "enunciado_juez": "Resumen de lo que se pedía, para que el juez tenga contexto.",
  "rubrica_llm": [
    { "nombre": "Buenas prácticas", "peso": 50, "guia": "Qué mirar en este criterio…" }
  ]
}
```

### Tipos de `check` deterministas disponibles

`name_present`, `trigger`, `min_jobs`, `runs_on_regex`, `uses_action`,
`run_present`, `permission`, `matrix_min`, `needs_present`, `if_present`,
`outputs_present`, `env_present`, `concurrency`, `workflow_call`, `regex`,
`not_regex`, `key_path`.

Mira el docstring de [`calificar.py`](calificar.py) para el detalle de cada uno.

## Probarlo en local

```bash
pip install pyyaml
python evaluador/calificar.py capitulos/01-anatomia-workflow/evaluacion/criterios.json
# (la parte del juez requiere GitHub Models, que solo corre dentro de Actions)
python evaluador/combinar.py \
  --criterios capitulos/01-anatomia-workflow/evaluacion/criterios.json \
  --determinista resultado-determinista.json \
  --juez /dev/null
```

## Sobre el juez LLM (GitHub Models)

- Se invoca con la acción oficial [`actions/ai-inference`](https://github.com/actions/ai-inference).
- Requiere el permiso `models: read` en el job y usa el `GITHUB_TOKEN` del run
  (no necesitas claves externas).
- El juez recibe la **rúbrica** + tu **entrega** y devuelve un JSON con puntuación
  y justificación por criterio. `combinar.py` extrae ese JSON de forma robusta.
- Si GitHub Models no está disponible, el paso usa `continue-on-error: true` y la
  nota se calcula solo con la parte determinista (avisándolo en el reporte).

> ⚠️ **Por qué un juez LLM y no solo reglas:** las pruebas deterministas verifican
> hechos comprobables (¿existe el permiso?, ¿usa esta acción?). El juez valora lo
> cualitativo (claridad, idiomática, seguridad razonada). Juntos dan una evaluación
> de _skills_ más completa. Recuerda: un juez LLM es **estocástico**; úsalo como
> señal complementaria, nunca como única verdad para decisiones críticas.

## Fuentes oficiales

- GitHub Models — https://docs.github.com/en/github-models
- `actions/ai-inference` — https://github.com/actions/ai-inference
- Permisos del `GITHUB_TOKEN` — https://docs.github.com/en/actions/security-guides/automatic-token-authentication
