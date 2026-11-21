from pathlib import Path

from src.models import Producto
from src.repository import RepositorioProductos


def test_persistencia_json_guardar_y_recargar(tmp_path: Path) -> None:
    archivo_json = tmp_path / "productos.json"
    repo_inicial = RepositorioProductos(archivo_json)
    producto = Producto(
        id="P010",
        nombre="Disco SSD 1TB",
        descripcion="Unidad de estado sólido NVMe",
        precio=310000,
        cantidad=10,
    )
    repo_inicial.guardar(producto)

    repo_recargado = RepositorioProductos(archivo_json)
    recuperado = repo_recargado.obtener_por_id("P010")
    assert recuperado == producto


def test_persistencia_json_eliminar_producto(tmp_path: Path) -> None:
    archivo_json = tmp_path / "productos.json"
    repo = RepositorioProductos(archivo_json)
    repo.guardar(
        Producto(
            id="P011",
            nombre="Memoria RAM 16GB",
            descripcion="DDR4 3200MHz",
            precio=190000,
            cantidad=6,
        )
    )
    assert repo.eliminar("P011") is True
    assert repo.eliminar("P011") is False

    repo_verificacion = RepositorioProductos(archivo_json)
    assert repo_verificacion.listar_todos() == []


def test_persistencia_json_archivo_vacio_no_falla(tmp_path: Path) -> None:
    archivo_vacio = tmp_path / "vacio.json"
    archivo_vacio.write_text("", encoding="utf-8")

    repo = RepositorioProductos(archivo_vacio)
    assert repo.listar_todos() == []