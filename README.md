# Guía de Trabajo No. 4 — CRUD de Productos y Calidad de Código

Proyecto desarrollado en Python para la asignatura **Aplicaciones y servicios web (ITM)**.

## Estructura del proyecto
- `src/models.py`: Entidad `Producto` y validaciones de negocio.
- `src/repository.py`: Almacenamiento en memoria y persistencia en JSON.
- `src/service.py`: Operaciones CRUD (Crear, Leer, Actualizar y Eliminar).
- `tests/`: Pruebas unitarias con `pytest` (casos exitosos, de error, fixtures y mocks).
- `features/productos.feature`: Escenarios BDD en sintaxis Gherkin.

## Ejecución
    python main.py

## Pruebas unitarias y cobertura
    python -m pytest -v --cov=src --cov-report=term-missing