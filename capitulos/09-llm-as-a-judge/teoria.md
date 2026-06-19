# Capítulo 09 · LLM as a Judge con GitHub Models

Las pruebas deterministas (cap. 08) no capturan bien lo **cualitativo**: ¿el código
es claro?, ¿el texto es correcto y respetuoso?, ¿la solución es idiomática? Para eso
sirve **LLM as a Judge**: un modelo de lenguaje evalúa una salida contra una
**rúbrica** y emite una puntuación con justificación.

## GitHub Models

[GitHub Models](https://docs.github.com/en/github-models) da acceso a modelos de IA
(de varios proveedores) directamente desde tu cuenta de GitHub, con un **nivel
gratuito** sujeto a límites de uso. Lo clave para este curso: puedes invocarlos
**desde un workflow** sin gestionar claves externas, usando el `GITHUB_TOKEN` del
propio run y el permiso `models: read`.

## La acción oficial: `actions/ai-inference`

[`actions/ai-inference`](https://github.com/actions/ai-inference) llama a un modelo
de GitHub Models. Requiere el permiso `models: read`:

```yaml
jobs:
  juez:
    runs-on: ubuntu-latest
    permissions:
      models: read                      # imprescindible
    steps:
      - id: evaluacion
        uses: actions/ai-inference@v1
        with:
          model: openai/gpt-4o-mini      # del catálogo de GitHub Models
          system-prompt: "Eres un evaluador estricto. Responde solo JSON."
          prompt: "Evalúa este texto: ..."
          max-completion-tokens: 800
      - run: echo "${{ steps.evaluacion.outputs.response }}"
```

### Entradas más útiles

| Input | Para qué |
|-------|----------|
| `prompt` / `prompt-file` | El mensaje de usuario (texto o archivo). El archivo tiene prioridad. |
| `system-prompt` / `system-prompt-file` | Las instrucciones del sistema (rol, formato de salida). |
| `model` | Modelo del catálogo (por defecto `openai/gpt-4o`). |
| `max-completion-tokens`, `temperature`, `top-p` | Parámetros de muestreo. |
| `token` | Por defecto `github.token`. |

### Salidas

| Output | Contenido |
|--------|-----------|
| `response` | La respuesta del modelo (texto). |
| `response-file` | Ruta a un archivo con la respuesta (útil si es larga o multilínea). |

## El patrón "LLM as a Judge"

1. **Rúbrica explícita**: define criterios con pesos (p.ej. claridad 40, seguridad 35,
   idiomática 25). Cuanto más concreta, más consistente el juez.
2. **Formato de salida estructurado**: pide al modelo que devuelva **solo JSON** con
   puntuación y justificación por criterio. Así puedes parsearlo y combinarlo con
   otras señales.
3. **System prompt** con el rol y las reglas; **user prompt** con la rúbrica + lo que
   se evalúa.
4. **Parseo robusto**: el modelo a veces añade texto; extrae el JSON de forma
   defensiva (como hace [`evaluador/combinar.py`](../../evaluador/combinar.py)).

Ejemplo de salida que pedimos al juez:

```json
{
  "criterios": [
    { "nombre": "Claridad", "peso": 40, "puntuacion": 85, "justificacion": "…" }
  ],
  "puntuacion_global": 82,
  "comentario": "…"
}
```

## Guardar prompts en el repo: `.prompt.yml`

GitHub Models permite versionar prompts en archivos `.prompt.yml` (con `messages`,
`model`, `modelParameters`, plantillas `{{variable}}`, `testData` y `evaluators`).
Es útil para iterar y revisar prompts como código.

## Buenas prácticas y límites

- ⚠️ **Estocástico**: un LLM puede variar entre ejecuciones. Baja `temperature`,
  fija la rúbrica y trátalo como **señal complementaria**, no como verdad absoluta.
- ⚠️ **Sesgos**: los jueces LLM pueden favorecer respuestas largas o cierto estilo.
  Pesos y criterios claros lo mitigan.
- ⚠️ **Privacidad**: lo que envías al modelo sale de tu workflow hacia el servicio.
- ⚠️ **Límites de uso**: GitHub Models tiene cuotas; serializa llamadas
  (`max-parallel: 1`) y maneja fallos con `continue-on-error`.
- ✅ **Combina**: determinista (objetivo) + juez LLM (cualitativo) = evaluación de
  skills más completa. Eso es justo lo que hace este curso.

## Fuentes oficiales

- GitHub Models — https://docs.github.com/en/github-models
- Inicio rápido de GitHub Models — https://docs.github.com/en/github-models/quickstart
- `actions/ai-inference` — https://github.com/actions/ai-inference
- Guardar prompts (`.prompt.yml`) — https://docs.github.com/en/github-models/use-github-models/storing-prompts-in-github-repositories
- Permisos del job — https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs
