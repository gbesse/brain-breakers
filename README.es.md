# BrainBreakers

[Français](README.md) · [English](README.en.md)

**Mutar la memoria, repetir la búsqueda, mostrar lo que sigue mal y reducir el caso.**

Eliminar una fuente, corregir un hecho y aislar espacios debe cambiar lo que el sistema recupera. Una respuesta correcta puede ocultar una fuente eliminada aún indexada. En cambio, retirar una fuente no invalida una respuesta con apoyo independiente.

## Probar

Python 3.11+; sin modelo, clave ni descarga de embeddings.

```sh
git clone https://github.com/gbesse/brain-breakers
cd brain-breakers
python3 -m brain_breakers serve --lang es
```

Abrir `http://127.0.0.1:8772/?lang=es`. La página muestra **pruebas guardadas de tres motores**, versiones, resultados y casos reducidos. El botón SQLite ejecuta pruebas locales nuevas, no muestra simplemente el archivo guardado. El JSON exportado incluye trazas y casos minimizados ejecutables.

```sh
python3 -m brain_breakers demo > prueba-sqlite.json
pip install '.[engines]'
python3 -m brain_breakers suite --backends sqlite_fts5,chroma,qdrant_local > prueba-tres-motores.json
python3 -m brain_breakers trial caso.json
python3 -m brain_breakers minimize caso.json
```

`pip install .` instala también `brain-breakers`. Interfaz y errores FR/EN/ES; identificadores y valores de casos siguen siendo datos sintéticos sin modificar.

![Caso de fuga](docs/preview-fr.png)

## Cuatro casos, tres motores reales

| Caso             | Control defectuoso inyectado                            | Integración corregida                             |
| ---------------- | ------------------------------------------------------- | ------------------------------------------------- |
| Fuente eliminada | El cliente omite eliminarla del índice                  | Sin fuente, respuesta desconocida                 |
| Corrección       | El cliente omite actualizar una entrada existente       | `30 days` pasa a `14 days`, mismo identificador   |
| Aislamiento      | El cliente omite el filtro de espacio                   | El canario del otro espacio queda inaccesible     |
| Apoyo redundante | La fuente borrada sigue apareciendo con igual respuesta | Misma respuesta, solo fuente independiente válida |

Matriz publicada: **12 parejas defectuoso/corregido, 24 pruebas**, más repeticiones del reductor; 12 fallos inyectados detectados y 12 integraciones corregidas conformes. SQLite FTS5 **3.40.1**, Chroma **1.5.9**, cliente Qdrant local **1.19.1**. Versiones del ensayo guardado; SQLite puede diferir en CI. Los cuatro casos se ejecutan en los tres motores en CI.

**Los fallos se crean en nuestra capa cliente. No son doce errores descubiertos ni reproducidos del código Chroma, Qdrant o SQLite.** Cada motor ejecuta operaciones reales de upsert, borrado y recuperación filtrada. Chroma y Qdrant reciben vectores deterministas de palabras, sin modelo ni comparación de pertinencia semántica. Telemetría anonimizada Chroma desactivada; Qdrant usa `:memory:`.

## Oráculo y reducción

Un registro fuente independiente aplica cada mutación. El oráculo selecciona la revisión declarada más alta del espacio solicitado; hechos contradictorios igual de actuales obligan a abstenerse. Comprueba respuesta, revisión exacta, fuentes recuperadas y aislamiento, no solo citas. Recuperar un canario es un fallo aunque el texto final parezca correcto.

El reductor elimina ruido, repite el motor real y conserva **éxito inicial + misma firma de fallo tras la mutación**. Protege los documentos afectados por operaciones. Repite hasta un punto fijo: mínimo local respecto a eliminar un documento no protegido, no mínimo global de texto u operaciones.

Casos JSON limitados a 24 documentos y 12 operaciones. `brain_breakers.adapters` define `upsert(document)`, `delete(id)`, `retrieve(query, scope=True)`, `close()` y `version`. Registrar una clase en `ADAPTERS` permite repetir los casos en otro motor; los adaptadores incluidos ejecutan las API reales. Sin adaptador GBrain/Hindsight incluido o validado.

## Trabajos previos y límites

[brain-ci](https://github.com/gbesse/brain-ci) ya compara contratos entre revisiones. [GBrain Evals](https://github.com/garrytan/gbrain-evals) y [tbench](https://github.com/compresh/tbench) ya diagnostican memoria. El enfoque es **mutación → documentos recuperados realmente → defecto de integración → caso reducido → reparación**, no una clasificación general.

Las API [update](https://docs.trychroma.com/docs/collections/update-data) y [delete](https://docs.trychroma.com/docs/collections/delete-data) Chroma proporcionan contratos. El [incidente Hindsight #3912](https://github.com/vectorize-io/hindsight/issues/3912) describe otro defecto de consolidación: motivó la investigación pero **esta matriz no lo reproduce**.

Valores declarados y estructurados, no respuestas naturales generadas por un agente. Sin atribución causal de LLM, evaluación general de recuperación, borrado físico de copias, cumplimiento jurídico, fallo de disco o validación distribuida. Canarios sintéticos. No se deduce adopción humana ni superioridad SOTA.

## Verificar

```sh
pip install '.[engines]'
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Doce pruebas incluyen matrices Chroma y Qdrant; esas dos se omiten explícitamente sin dependencias opcionales. CI instala ambas y las ejecuta. Navegador FR/EN/ES: pruebas guardadas, SQLite en vivo, filtros, redundancia, exportación y móvil. CI Python 3.11/3.12, construcción y rueda fuera de fuentes. MIT; alfa pública.
