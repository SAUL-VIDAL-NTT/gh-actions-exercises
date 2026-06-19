#!/usr/bin/env python3
"""
Descubre qué capítulos hay que evaluar.

Recorre `capitulos/*/evaluacion/criterios.json` y selecciona aquellos cuyo
`archivo_entrega` YA EXISTE en el repo (es decir, el estudiante hizo su entrega).

Si la variable de entorno CAP_FILTRO está definida (p.ej. "03"), solo incluye
los capítulos cuyo nombre de carpeta empiece por ese prefijo.

Escribe en $GITHUB_OUTPUT una variable `lista` con un array JSON de rutas de
carpeta de capítulo, lista para usar como matriz en el workflow evaluador.
"""

import glob
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def main():
    filtro = os.environ.get("CAP_FILTRO", "").strip()
    seleccionados = []

    for criterios_path in sorted(glob.glob("capitulos/*/evaluacion/criterios.json")):
        cap_dir = os.path.dirname(os.path.dirname(criterios_path))
        nombre = os.path.basename(cap_dir)
        if filtro and not nombre.startswith(filtro):
            continue
        try:
            with open(criterios_path, encoding="utf-8") as f:
                criterios = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        entrega = criterios.get("archivo_entrega", "")
        if entrega and os.path.exists(entrega):
            seleccionados.append(cap_dir.replace("\\", "/"))

    print("Capítulos a evaluar:", seleccionados or "(ninguno: aún no hay entregas)")

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"lista={json.dumps(seleccionados)}\n")
            f.write(f"hay={'true' if seleccionados else 'false'}\n")


if __name__ == "__main__":
    main()
