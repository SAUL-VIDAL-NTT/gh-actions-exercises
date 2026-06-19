#!/usr/bin/env python3
"""
Prepara el mensaje de usuario (user prompt) para el juez LLM.

Combina la rúbrica del capítulo (campo `rubrica_llm` de criterios.json) con el
contenido de la entrega del estudiante, y lo escribe en un archivo de texto que
luego se pasa a la acción actions/ai-inference vía su input `prompt-file`.

Uso:
    python evaluador/preparar_juez.py <criterios.json> <salida.md>
"""

import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def main():
    criterios_path, salida = sys.argv[1], sys.argv[2]
    with open(criterios_path, encoding="utf-8") as f:
        criterios = json.load(f)

    entrega = criterios["archivo_entrega"]
    contenido = ""
    if os.path.exists(entrega):
        with open(entrega, encoding="utf-8") as f:
            contenido = f.read()

    rubrica = criterios.get("rubrica_llm", [])
    lineas = ["## RÚBRICA", ""]
    for r in rubrica:
        lineas.append(f"- **{r.get('nombre')}** (peso {r.get('peso')}): {r.get('guia')}")
    lineas.append("")
    lineas.append(f"## ENUNCIADO DEL EJERCICIO (capítulo {criterios.get('capitulo')})")
    lineas.append("")
    lineas.append(criterios.get("enunciado_juez", "Evalúa la calidad general del workflow."))
    lineas.append("")
    lineas.append("## ENTREGA DEL ESTUDIANTE")
    lineas.append("")
    lineas.append("```yaml")
    lineas.append(contenido if contenido else "# (entrega vacía o no encontrada)")
    lineas.append("```")
    lineas.append("")
    lineas.append("Devuelve tu evaluación SOLO como el objeto JSON especificado.")

    with open(salida, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"Prompt del juez escrito en {salida} ({len(rubrica)} criterios de rúbrica).")


if __name__ == "__main__":
    main()
