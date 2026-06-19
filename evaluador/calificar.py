#!/usr/bin/env python3
"""
Evaluador DETERMINISTA del curso de GitHub Actions.

Analiza estructuralmente la entrega del estudiante (un archivo de workflow YAML)
contra una lista de criterios definidos en `evaluacion/criterios.json` de cada
capítulo. No ejecuta el workflow: comprueba que esté bien construido.

Uso:
    python evaluador/calificar.py <ruta_criterios.json> [--salida resultado-determinista.json]

Salida:
    - Reporte legible por consola (y en $GITHUB_STEP_SUMMARY si existe).
    - JSON con el detalle y el puntaje, para combinarlo con el juez LLM.

Tipos de check soportados (campo "tipo" en criterios.json):
    name_present     -> el workflow tiene clave de nivel superior `name`
    trigger          -> "valor" (evento) está presente en `on`
    min_jobs         -> nº de jobs >= "valor"
    runs_on_regex    -> algún job tiene runs-on que casa con regex "valor"
    uses_action      -> algún step usa una acción que contiene la subcadena "valor"
    run_present      -> existe al menos un step con `run`
    permission       -> permisos declaran "valor" (formato "clave:nivel", p.ej. "contents:read")
    matrix_min       -> algún job define strategy.matrix con una clave de >= "valor" elementos
    needs_present    -> algún job declara `needs`
    if_present       -> algún job o step declara `if`
    outputs_present  -> algún job declara `outputs`
    env_present      -> hay `env` a nivel workflow, job o step
    concurrency      -> hay `concurrency` a nivel workflow o job
    workflow_call    -> `on` incluye `workflow_call` (workflow reutilizable)
    regex            -> el texto crudo del archivo casa con la regex "valor"
    not_regex        -> el texto crudo NO debe casar con la regex "valor"
    key_path         -> existe la ruta con puntos "ruta" (admite comodín *)
"""

import json
import os
import re
import sys

# Salida UTF-8 robusta (la consola de Windows usa cp1252 y rompe con emojis).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

try:
    import yaml
except ImportError:
    print("ERROR: falta PyYAML. Instala con: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# --- Utilidades --------------------------------------------------------------

def cargar_yaml(ruta):
    """Devuelve (dict, texto_crudo, error). error es None si todo fue bien."""
    if not os.path.exists(ruta):
        return None, "", f"No se encontró el archivo de entrega: {ruta}"
    with open(ruta, "r", encoding="utf-8") as f:
        texto = f.read()
    try:
        data = yaml.safe_load(texto)
    except yaml.YAMLError as e:
        return None, texto, f"El YAML no es válido: {e}"
    if not isinstance(data, dict):
        return None, texto, "El archivo no parece un workflow (no es un mapa YAML)."
    return data, texto, None


def get_on(data):
    """
    Devuelve el bloque `on` normalizado a lista de nombres de evento.
    OJO: PyYAML interpreta la clave `on:` como el booleano True (YAML 1.1),
    por eso buscamos tanto 'on' como True.
    """
    bloque = data.get("on", data.get(True))
    if bloque is None:
        return []
    if isinstance(bloque, str):
        return [bloque]
    if isinstance(bloque, list):
        return [str(x) for x in bloque]
    if isinstance(bloque, dict):
        return [str(k) for k in bloque.keys()]
    return []


def get_jobs(data):
    jobs = data.get("jobs")
    return jobs if isinstance(jobs, dict) else {}


def iter_steps(data):
    for job in get_jobs(data).values():
        if isinstance(job, dict):
            for step in job.get("steps", []) or []:
                if isinstance(step, dict):
                    yield step


def recolectar_permisos(data):
    """Devuelve un set de cadenas 'clave:nivel' a partir de permisos en cualquier nivel."""
    encontrados = set()

    def procesar(perms):
        if isinstance(perms, str):
            # p.ej. permissions: read-all  ó  write-all
            encontrados.add(perms.strip())
        elif isinstance(perms, dict):
            for k, v in perms.items():
                encontrados.add(f"{k}:{v}")

    procesar(data.get("permissions"))
    for job in get_jobs(data).values():
        if isinstance(job, dict):
            procesar(job.get("permissions"))
    return encontrados


def ruta_existe(data, ruta):
    """Comprueba una ruta con puntos. '*' casa con cualquier clave de un dict."""
    def buscar(nodo, partes):
        if not partes:
            return True
        parte, resto = partes[0], partes[1:]
        if parte == "*":
            if isinstance(nodo, dict):
                return any(buscar(v, resto) for v in nodo.values())
            if isinstance(nodo, list):
                return any(buscar(v, resto) for v in nodo)
            return False
        if isinstance(nodo, dict) and parte in nodo:
            return buscar(nodo[parte], resto)
        return False

    return buscar(data, ruta.split("."))


# --- Motor de checks ---------------------------------------------------------

def evaluar_check(check, data, texto):
    """Devuelve True/False según si el check se cumple."""
    tipo = check.get("tipo")
    valor = check.get("valor")

    if tipo == "name_present":
        return bool(data.get("name"))

    if tipo == "trigger":
        return str(valor) in get_on(data)

    if tipo == "min_jobs":
        return len(get_jobs(data)) >= int(valor)

    if tipo == "runs_on_regex":
        pat = re.compile(str(valor), re.IGNORECASE)
        for job in get_jobs(data).values():
            if isinstance(job, dict):
                ro = job.get("runs-on")
                if isinstance(ro, (list, dict)):
                    ro = json.dumps(ro)
                if ro and pat.search(str(ro)):
                    return True
        return False

    if tipo == "uses_action":
        for step in iter_steps(data):
            uses = step.get("uses", "")
            if isinstance(uses, str) and str(valor) in uses:
                return True
        return False

    if tipo == "run_present":
        return any("run" in step for step in iter_steps(data))

    if tipo == "permission":
        return str(valor) in recolectar_permisos(data)

    if tipo == "matrix_min":
        n = int(valor)
        for job in get_jobs(data).values():
            if not isinstance(job, dict):
                continue
            matrix = (job.get("strategy") or {}).get("matrix")
            if isinstance(matrix, dict):
                for k, v in matrix.items():
                    if k in ("include", "exclude"):
                        continue
                    if isinstance(v, list) and len(v) >= n:
                        return True
        return False

    if tipo == "needs_present":
        return any(isinstance(j, dict) and j.get("needs") for j in get_jobs(data).values())

    if tipo == "if_present":
        if any(isinstance(j, dict) and j.get("if") for j in get_jobs(data).values()):
            return True
        return any(step.get("if") for step in iter_steps(data))

    if tipo == "outputs_present":
        return any(isinstance(j, dict) and j.get("outputs") for j in get_jobs(data).values())

    if tipo == "env_present":
        if data.get("env"):
            return True
        for job in get_jobs(data).values():
            if isinstance(job, dict) and job.get("env"):
                return True
        return any(step.get("env") for step in iter_steps(data))

    if tipo == "concurrency":
        if data.get("concurrency"):
            return True
        return any(isinstance(j, dict) and j.get("concurrency") for j in get_jobs(data).values())

    if tipo == "workflow_call":
        return "workflow_call" in get_on(data)

    if tipo == "regex":
        return re.search(str(valor), texto, re.MULTILINE) is not None

    if tipo == "not_regex":
        return re.search(str(valor), texto, re.MULTILINE) is None

    if tipo == "key_path":
        return ruta_existe(data, str(check.get("ruta")))

    raise ValueError(f"Tipo de check desconocido: {tipo}")


# --- Programa principal ------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    ruta_criterios = sys.argv[1]
    salida = "resultado-determinista.json"
    if "--salida" in sys.argv:
        salida = sys.argv[sys.argv.index("--salida") + 1]

    with open(ruta_criterios, "r", encoding="utf-8") as f:
        criterios = json.load(f)

    base = os.path.dirname(os.path.abspath(ruta_criterios))
    # archivo_entrega se interpreta relativo a la raíz del repo
    entrega = criterios["archivo_entrega"]

    data, texto, error = cargar_yaml(entrega)

    resultados = []
    obtenidos = 0
    posibles = 0

    if error:
        # Entrega ausente o YAML inválido: 0 en todos los checks.
        for c in criterios["checks"]:
            posibles += c["puntos"]
            resultados.append({
                "id": c["id"], "desc": c["desc"], "puntos": c["puntos"],
                "obtenidos": 0, "ok": False, "nota": error,
            })
    else:
        for c in criterios["checks"]:
            posibles += c["puntos"]
            try:
                ok = evaluar_check(c, data, texto)
            except Exception as e:  # noqa: BLE001
                ok = False
                c = {**c, "_err": str(e)}
            pts = c["puntos"] if ok else 0
            obtenidos += pts
            resultados.append({
                "id": c["id"], "desc": c["desc"], "puntos": c["puntos"],
                "obtenidos": pts, "ok": ok, "nota": c.get("_err", ""),
            })

    porcentaje = round(100 * obtenidos / posibles, 1) if posibles else 0.0

    reporte = {
        "capitulo": criterios.get("capitulo"),
        "archivo_entrega": entrega,
        "error": error,
        "puntos_obtenidos": obtenidos,
        "puntos_posibles": posibles,
        "porcentaje": porcentaje,
        "checks": resultados,
    }

    with open(salida, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    # --- Reporte legible ---
    lineas = []
    lineas.append(f"## 🤖 Evaluación determinista — Capítulo {criterios.get('capitulo')}")
    lineas.append("")
    lineas.append(f"**Entrega:** `{entrega}`")
    if error:
        lineas.append("")
        lineas.append(f"> ⚠️ {error}")
    lineas.append("")
    lineas.append("| Criterio | Puntos | Resultado |")
    lineas.append("|----------|:------:|:---------:|")
    for r in resultados:
        icono = "✅" if r["ok"] else "❌"
        lineas.append(f"| {r['desc']} | {r['obtenidos']}/{r['puntos']} | {icono} |")
    lineas.append("")
    lineas.append(f"**Subtotal determinista: {obtenidos}/{posibles} ({porcentaje} %)**")
    texto_reporte = "\n".join(lineas)

    print(texto_reporte)

    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write(texto_reporte + "\n\n")

    # Exponer porcentaje como salida del step si corremos en Actions.
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"porcentaje={porcentaje}\n")


if __name__ == "__main__":
    main()
