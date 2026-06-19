# Ejercicio 07 · Endurecer un workflow

## Objetivo

Aplicar menor privilegio, preparar OIDC y fijar acciones por SHA.

## Tarea

Crea **`.github/workflows/cap07-seguro.yml`** que:

1. Tenga `name` y se dispare en `push`.
2. Declare `permissions` a nivel workflow con **`contents: read`**.
3. Tenga un job (p.ej. `deploy`) que añada **`id-token: write`** (preparado para OIDC).
4. Use al menos una acción **fijada por SHA de commit completo** (40 hex).
   Puedes fijar `actions/checkout` a un SHA conocido.
5. **No** use referencias de rama móviles (`@main` / `@master`) en ninguna acción.

> No necesitas un proveedor cloud real: basta con declarar el permiso `id-token: write`
> y, opcionalmente, un step que muestre que el OIDC estaría disponible.

## Cómo obtener el SHA de una acción

En el repo de la acción (p.ej. `actions/checkout`), pestaña **Tags/Releases** →
abre el commit de la versión → copia el SHA de 40 caracteres. Añade un comentario
con la versión legible al lado.

## Criterios de evaluación

**Deterministas (60 %)**

- `name` y disparo en `push`.
- `permissions` con `contents: read`.
- Un job con `id-token: write`.
- Al menos una acción fijada por SHA (`@<40-hex>`).
- No usa `@main` / `@master`.

**Juez LLM (40 %)** — menor privilegio real (permisos ajustados por job),
justificación implícita del `id-token`, y ausencia de patrones de inyección.

> Solución: `solucion/cap07-seguro.yml`.
