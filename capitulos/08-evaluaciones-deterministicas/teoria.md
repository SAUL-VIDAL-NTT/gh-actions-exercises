# Capítulo 08 · Evaluaciones deterministas (gates de CI)

Una **evaluación determinista** comprueba **hechos verificables**: o se cumplen o
no. Misma entrada → mismo resultado, siempre. Son la columna vertebral de cualquier
CI y la base objetiva de una evaluación de _skills_.

## Qué evalúa un gate determinista

- **Lint / formato**: el código sigue el estilo (eslint, ruff, gofmt…). Para los
  propios workflows existe la herramienta comunitaria
  [`actionlint`](https://github.com/rhysd/actionlint).
- **Tests**: unitarios, integración (pytest, jest, go test…).
- **Aserciones**: condiciones explícitas (¿existe el archivo?, ¿la salida contiene X?,
  ¿el JSON tiene tal campo?).
- **Cobertura, tamaño de bundle, vulnerabilidades**, etc.

## El mecanismo: el código de salida

En Actions, **un step falla si su comando devuelve un código de salida ≠ 0**, y un
job falla si falla un step. Por eso los gates se construyen sobre `exit`:

```yaml
- name: Aserción simple
  run: |
    set -e                       # aborta al primer error
    test -f dist/app.js          # falla si no existe
    grep -q "versión 1.4" CHANGELOG.md   # falla si no encuentra el texto
```

`set -e` hace que el script aborte (y el step falle) en cuanto un comando falla.

## Reportar resultados: `$GITHUB_STEP_SUMMARY`

Escribe Markdown en el archivo `$GITHUB_STEP_SUMMARY` para mostrar un resumen
bonito en la pestaña del run:

```yaml
- name: Resumen
  run: |
    echo "## Resultado de la evaluación" >> "$GITHUB_STEP_SUMMARY"
    echo "- Tests: ✅" >> "$GITHUB_STEP_SUMMARY"
    echo "- Lint: ✅" >> "$GITHUB_STEP_SUMMARY"
```

## Anotaciones en el código

Con _workflow commands_ puedes anotar líneas concretas (aparecen en la pestaña
Files de un PR):

```yaml
- run: echo "::error file=src/app.py,line=10::Falta validar la entrada"
- run: echo "::warning::Esto es solo una advertencia"
```

## Convertir el gate en obligatorio

En GitHub, un workflow que falla **bloquea** el merge si lo configuras como
**required status check** en las reglas de protección de rama (Settings → Branches
→ Branch protection rules). Así, "pasar la evaluación" se vuelve condición para
integrar.

## Cómo lo hace este curso

El evaluador del curso ([`evaluador/calificar.py`](../../evaluador/calificar.py)) es
exactamente esto: parsea tu workflow y comprueba aserciones estructurales
(`trigger`, `permission`, `uses_action`…), asignando puntos. Es **100 % determinista
y reproducible**. En el próximo capítulo añadiremos la capa **semántica** (juez LLM)
para lo que las reglas no capturan bien.

> ⚖️ **Determinista vs semántico**: lo determinista es preciso pero rígido (solo
> mide lo que programaste). Lo semántico (cap. 09) es flexible pero estocástico.
> Una buena evaluación de skills combina ambos.

## Fuentes oficiales

- Comandos de workflow (anotaciones, summary) — https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
- Resúmenes de job — https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#adding-a-job-summary
- Reglas de protección de rama / status checks — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
