#!/usr/bin/env python3
"""
Combina el resultado DETERMINISTA con el del JUEZ LLM y produce la nota final.

Uso:
    python evaluador/combinar.py \
        --criterios <ruta_criterios.json> \
        --determinista resultado-determinista.json \
        --juez respuesta-juez.txt \
        --salida nota-final.json

- `respuesta-juez.txt` contiene la respuesta cruda del modelo (salida `response`
  de la acción actions/ai-inference). Se espera que sea un JSON; lo extraemos de
  forma defensiva (tolerando bloques ```json ... ``` o texto alrededor).

Ponderación (configurable en criterios.json):
    peso_determinista  (def. 0.6)
    peso_juez          (def. 0.4)
    aprobado_min       (def. 70)   -> umbral de aprobación en %
"""

import argparse
import json
import os
import re
import sys

# Salida UTF-8 robusta (la consola de Windows usa cp1252 y rompe con emojis).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def extraer_json(texto):
    """Extrae el primer objeto JSON válido de un texto arbitrario."""
    if not texto:
        return None
    # Quitar vallas de código si las hay.
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", texto, re.DOTALL)
    if fence:
        try:
            return json.loads(fence.group(1))
        except json.JSONDecodeError:
            pass
    # Buscar el primer { ... } balanceado.
    inicio = texto.find("{")
    while inicio != -1:
        profundidad = 0
        for i in range(inicio, len(texto)):
            if texto[i] == "{":
                profundidad += 1
            elif texto[i] == "}":
                profundidad -= 1
                if profundidad == 0:
                    try:
                        return json.loads(texto[inicio:i + 1])
                    except json.JSONDecodeError:
                        break
        inicio = texto.find("{", inicio + 1)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--criterios", required=True)
    ap.add_argument("--determinista", required=True)
    ap.add_argument("--juez", required=True)
    ap.add_argument("--salida", default="nota-final.json")
    args = ap.parse_args()

    with open(args.criterios, encoding="utf-8") as f:
        criterios = json.load(f)
    with open(args.determinista, encoding="utf-8") as f:
        det = json.load(f)

    juez_texto = ""
    if os.path.exists(args.juez):
        with open(args.juez, encoding="utf-8") as f:
            juez_texto = f.read()
    juez = extraer_json(juez_texto) or {}

    peso_det = float(criterios.get("peso_determinista", 0.6))
    peso_juez = float(criterios.get("peso_juez", 0.4))
    aprobado_min = float(criterios.get("aprobado_min", 70))

    det_pct = float(det.get("porcentaje", 0))
    juez_pct = float(juez.get("puntuacion_global", 0)) if juez else 0.0
    juez_disponible = bool(juez)

    if juez_disponible:
        final = round(det_pct * peso_det + juez_pct * peso_juez, 1)
    else:
        # Si el juez no respondió (p.ej. GitHub Models no habilitado),
        # la nota usa solo la parte determinista, avisando del hecho.
        final = round(det_pct, 1)

    aprobado = final >= aprobado_min

    reporte = {
        "capitulo": criterios.get("capitulo"),
        "determinista_pct": det_pct,
        "juez_pct": juez_pct,
        "juez_disponible": juez_disponible,
        "peso_determinista": peso_det,
        "peso_juez": peso_juez,
        "nota_final": final,
        "aprobado_min": aprobado_min,
        "aprobado": aprobado,
        "juez_detalle": juez,
    }
    with open(args.salida, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    # --- Reporte legible (Markdown) ---
    L = []
    L.append(f"## 🏁 Nota final — Capítulo {criterios.get('capitulo')}")
    L.append("")
    estado = "✅ **APROBADO**" if aprobado else "❌ **NO APROBADO**"
    L.append(f"### {estado} — {final} / 100")
    L.append("")
    L.append("| Componente | Peso | Puntuación |")
    L.append("|------------|:----:|:----------:|")
    L.append(f"| Determinista (estructura) | {int(peso_det*100)} % | {det_pct} |")
    if juez_disponible:
        L.append(f"| Juez LLM (semántico) | {int(peso_juez*100)} % | {juez_pct} |")
    else:
        L.append(f"| Juez LLM (semántico) | — | ⚠️ no disponible |")
    L.append("")

    if juez_disponible and juez.get("criterios"):
        L.append("#### Detalle del juez LLM")
        L.append("")
        L.append("| Criterio | Peso | Puntuación | Justificación |")
        L.append("|----------|:----:|:----------:|---------------|")
        for c in juez["criterios"]:
            L.append(
                f"| {c.get('nombre','')} | {c.get('peso','')} | "
                f"{c.get('puntuacion','')} | {str(c.get('justificacion','')).replace(chr(10),' ')} |"
            )
        L.append("")
        if juez.get("comentario"):
            L.append(f"> 💬 **Comentario del juez:** {juez['comentario']}")
            L.append("")
    elif not juez_disponible:
        L.append("> ⚠️ El juez LLM no devolvió una respuesta válida. ")
        L.append("> Revisa que GitHub Models esté habilitado y que el job tenga `permissions: models: read`.")
        L.append("")

    texto_reporte = "\n".join(L)
    print(texto_reporte)

    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write(texto_reporte + "\n\n")

    # Guardar el cuerpo del comentario de PR.
    with open("comentario-pr.md", "w", encoding="utf-8") as f:
        f.write(texto_reporte + "\n")

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"nota_final={final}\n")
            f.write(f"aprobado={'true' if aprobado else 'false'}\n")

    # Salir con código !=0 si no aprueba (útil como gate de CI, opcional).
    if criterios.get("fallar_si_no_aprueba", False) and not aprobado:
        sys.exit(1)


if __name__ == "__main__":
    main()
