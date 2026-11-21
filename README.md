# Monitor de estabilidad de la aplicación APP-02

Programa de menú que analiza las descargas y las caídas semanales de una aplicación móvil
publicada: listado, resumen, estabilidad de cada semana, búsqueda por umbral, mejor racha,
previsión de crecimiento, consulta de una semana y comprobación de los datos.

**Módulo:** IC44 — Fundamentos de programación en Python
**Unidad:** 2 — Estructuras de control, depuración y excepciones
**Pareja:** 2
**Autores:** Iker Alcolea Mateos · David Raúl Rus Almaján

## Aplicación analizada

| Dato | Valor |
|---|---|
| Código | APP-02 |
| Nombre | Lista de la Compra |
| Semanas | 12 |

## Ejecución desde Docker Hub

No hace falta descargar el repositorio ni tener Python instalado. Solo Docker. El programa
pide datos por teclado, así que se ejecuta con `-it`.

```bash
docker run --rm -it --pull always [usuario]/monitor-app-02:1.0.0
```

Página de la imagen: https://hub.docker.com/r/[usuario]/monitor-app-02

## Ejecución en local

Requiere Python 3.10 o superior.

```bash
python3 -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
python monitor_app.py
```

## Construir la imagen

```bash
docker build -t monitor-app-02 .
docker run --rm -it monitor-app-02
```

## Estructura del proyecto

```
.
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
└── monitor_app.py
```
