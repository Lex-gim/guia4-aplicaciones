from pathlib import Path

from src.repository import RepositorioProductos
from src.service import ServicioProductos


def ejecutar_demo() -> None:
    """Ejecuta una demostración de las operaciones CRUD con persistencia JSON."""
    repositorio = RepositorioProductos(Path("data/productos.json"))
    servicio = ServicioProductos(repositorio)

    # Crear
    producto = servicio.crear_producto(
        producto_id="P001",
        nombre="Teclado Mecánico",
        descripcion="Teclado mecánico compacto con switches táctiles",
        precio=280000,
        cantidad=15,
    )
    print("Creado:", producto)

    # Leer
    print("Consultado:", servicio.obtener_producto("P001"))

    # Actualizar
    actualizado = servicio.actualizar_producto("P001", precio=265000, cantidad=12)
    print("Actualizado:", actualizado)

    # Listar
    print("Listado actual:", servicio.listar_productos())

    # Eliminar
    servicio.eliminar_producto("P001")
    print("Listado tras eliminar:", servicio.listar_productos())


if __name__ == "__main__":
    ejecutar_demo()