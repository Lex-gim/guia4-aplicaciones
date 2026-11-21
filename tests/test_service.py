from unittest.mock import MagicMock

import pytest

from src.models import Producto
from src.repository import RepositorioProductos
from src.service import (
    ERROR_PRODUCTO_DUPLICADO,
    ERROR_PRODUCTO_NO_ENCONTRADO,
    ServicioProductos,
)


@pytest.fixture
def servicio_con_datos() -> ServicioProductos:
    """Fixture que inicializa el servicio con un producto base en memoria."""
    repositorio = RepositorioProductos()
    servicio = ServicioProductos(repositorio)
    servicio.crear_producto(
        producto_id="P001",
        nombre="Monitor 24 pulgadas",
        descripcion="Monitor IPS Full HD",
        precio=650000,
        cantidad=8,
    )
    return servicio


# -------------------- CREATE (Crear) --------------------


def test_crear_producto_exitoso(servicio_con_datos: ServicioProductos) -> None:
    nuevo = servicio_con_datos.crear_producto(
        producto_id="P002",
        nombre="Audífonos",
        descripcion="Audífonos inalámbricos con cancelación de ruido",
        precio=320000,
        cantidad=20,
    )
    assert nuevo.id == "P002"
    assert nuevo.nombre == "Audífonos"
    assert nuevo.precio == pytest.approx(320000.0)
    assert nuevo.cantidad == 20


def test_crear_producto_id_duplicado_lanza_error(
    servicio_con_datos: ServicioProductos,
) -> None:
    with pytest.raises(ValueError, match=ERROR_PRODUCTO_DUPLICADO):
        servicio_con_datos.crear_producto(
            producto_id="P001",
            nombre="Otro producto",
            descripcion="Descripción duplicada",
            precio=10000,
            cantidad=1,
        )


@pytest.mark.parametrize(
    "producto_id,nombre,descripcion,precio,cantidad",
    [
        ("", "Mouse", "Mouse USB", 50000, 5),
        ("P003", "   ", "Mouse USB", 50000, 5),
        ("P003", "Mouse", "", 50000, 5),
        ("P003", "Mouse", "Mouse USB", 0, 5),
        ("P003", "Mouse", "Mouse USB", -100, 5),
        ("P003", "Mouse", "Mouse USB", True, 5),
        ("P003", "Mouse", "Mouse USB", 50000, -1),
        ("P003", "Mouse", "Mouse USB", 50000, False),
    ],
)
def test_crear_producto_datos_invalidos_lanza_error(
    servicio_con_datos: ServicioProductos,
    producto_id: str,
    nombre: str,
    descripcion: str,
    precio: float,
    cantidad: int,
) -> None:
    with pytest.raises(ValueError):
        servicio_con_datos.crear_producto(
            producto_id=producto_id,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad=cantidad,
        )


# -------------------- READ (Leer) --------------------


def test_obtener_producto_exitoso(servicio_con_datos: ServicioProductos) -> None:
    producto = servicio_con_datos.obtener_producto("P001")
    assert producto.id == "P001"
    assert producto.nombre == "Monitor 24 pulgadas"


def test_listar_productos_exitoso(servicio_con_datos: ServicioProductos) -> None:
    productos = servicio_con_datos.listar_productos()
    assert len(productos) == 1
    assert productos[0].id == "P001"


def test_obtener_producto_inexistente_lanza_error(
    servicio_con_datos: ServicioProductos,
) -> None:
    with pytest.raises(KeyError, match=ERROR_PRODUCTO_NO_ENCONTRADO):
        servicio_con_datos.obtener_producto("P999")


# -------------------- UPDATE (Actualizar) --------------------


def test_actualizar_producto_exitoso(servicio_con_datos: ServicioProductos) -> None:
    actualizado = servicio_con_datos.actualizar_producto(
        producto_id="P001",
        nombre="Monitor 27 pulgadas",
        precio=790000,
        cantidad=5,
    )
    assert actualizado.nombre == "Monitor 27 pulgadas"
    assert actualizado.descripcion == "Monitor IPS Full HD"
    assert actualizado.precio == pytest.approx(790000.0)
    assert actualizado.cantidad == 5


def test_actualizar_producto_inexistente_lanza_error(
    servicio_con_datos: ServicioProductos,
) -> None:
    with pytest.raises(KeyError, match=ERROR_PRODUCTO_NO_ENCONTRADO):
        servicio_con_datos.actualizar_producto(producto_id="P999", precio=50000)


def test_actualizar_producto_con_valor_invalido_lanza_error(
    servicio_con_datos: ServicioProductos,
) -> None:
    with pytest.raises(ValueError):
        servicio_con_datos.actualizar_producto(producto_id="P001", precio=-500)


# -------------------- DELETE (Eliminar) --------------------


def test_eliminar_producto_exitoso(servicio_con_datos: ServicioProductos) -> None:
    servicio_con_datos.eliminar_producto("P001")
    assert servicio_con_datos.listar_productos() == []


def test_eliminar_producto_inexistente_lanza_error(
    servicio_con_datos: ServicioProductos,
) -> None:
    with pytest.raises(KeyError, match=ERROR_PRODUCTO_NO_ENCONTRADO):
        servicio_con_datos.eliminar_producto("P999")


# -------------------- PRUEBA AISLADA CON MOCK --------------------


def test_crear_producto_verifica_interaccion_con_mock() -> None:
    """Verifica con un Mock que el servicio delega correctamente al repositorio."""
    repositorio_mock = MagicMock(spec=RepositorioProductos)
    repositorio_mock.obtener_por_id.return_value = None
    esperado = Producto(
        id="P100",
        nombre="Webcam HD",
        descripcion="Cámara 1080p con micrófono",
        precio=180000,
        cantidad=4,
    )
    repositorio_mock.guardar.return_value = esperado

    servicio = ServicioProductos(repositorio_mock)
    resultado = servicio.crear_producto(
        producto_id="P100",
        nombre="Webcam HD",
        descripcion="Cámara 1080p con micrófono",
        precio=180000,
        cantidad=4,
    )

    assert resultado == esperado
    repositorio_mock.obtener_por_id.assert_called_once_with("P100")
    repositorio_mock.guardar.assert_called_once_with(esperado)