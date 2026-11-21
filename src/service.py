from typing import Optional

from src.models import Producto
from src.repository import RepositorioProductos

ERROR_PRODUCTO_NO_ENCONTRADO = "No existe un producto con el ID especificado."
ERROR_PRODUCTO_DUPLICADO = "Ya existe un producto registrado con ese ID."


class ServicioProductos:
    """Implementa las operaciones CRUD para la gestión de productos."""

    def __init__(self, repositorio: RepositorioProductos) -> None:
        self._repositorio = repositorio

    def crear_producto(
        self,
        producto_id: str,
        nombre: str,
        descripcion: str,
        precio: float,
        cantidad: int,
    ) -> Producto:
        """Crea un nuevo producto validando que su ID sea único."""
        producto = Producto(
            id=producto_id,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad=cantidad,
        )
        if self._repositorio.obtener_por_id(producto.id) is not None:
            raise ValueError(ERROR_PRODUCTO_DUPLICADO)
        return self._repositorio.guardar(producto)

    def obtener_producto(self, producto_id: str) -> Producto:
        """Consulta un producto existente por su ID."""
        producto = self._repositorio.obtener_por_id(producto_id)
        if producto is None:
            raise KeyError(ERROR_PRODUCTO_NO_ENCONTRADO)
        return producto

    def listar_productos(self) -> list[Producto]:
        """Lista todos los productos registrados."""
        return self._repositorio.listar_todos()

    def actualizar_producto(
        self,
        producto_id: str,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        precio: Optional[float] = None,
        cantidad: Optional[int] = None,
    ) -> Producto:
        """Actualiza los campos proporcionados de un producto existente."""
        existente = self.obtener_producto(producto_id)
        actualizado = Producto(
            id=existente.id,
            nombre=existente.nombre if nombre is None else nombre,
            descripcion=existente.descripcion if descripcion is None else descripcion,
            precio=existente.precio if precio is None else precio,
            cantidad=existente.cantidad if cantidad is None else cantidad,
        )
        return self._repositorio.guardar(actualizado)

    def eliminar_producto(self, producto_id: str) -> None:
        """Elimina un producto existente por su ID."""
        if not self._repositorio.eliminar(producto_id):
            raise KeyError(ERROR_PRODUCTO_NO_ENCONTRADO)