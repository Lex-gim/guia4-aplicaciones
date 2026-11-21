import json
from pathlib import Path
from typing import Optional

from src.models import Producto


class RepositorioProductos:
    """Gestiona el almacenamiento de productos en memoria y opcionalmente en JSON."""

    def __init__(self, ruta_archivo: Optional[Path] = None) -> None:
        self._ruta_archivo = ruta_archivo
        self._productos: dict[str, Producto] = {}
        if self._ruta_archivo and self._ruta_archivo.exists():
            self._cargar_desde_archivo()

    def _cargar_desde_archivo(self) -> None:
        if not self._ruta_archivo:
            return
        contenido = self._ruta_archivo.read_text(encoding="utf-8").strip()
        if not contenido:
            return
        datos = json.loads(contenido)
        for item in datos:
            producto = Producto(**item)
            self._productos[producto.id] = producto

    def _guardar_en_archivo(self) -> None:
        if not self._ruta_archivo:
            return
        self._ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        datos = [producto.a_diccionario() for producto in self._productos.values()]
        with self._ruta_archivo.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)

    def guardar(self, producto: Producto) -> Producto:
        """Inserta o actualiza un producto en el repositorio."""
        self._productos[producto.id] = producto
        self._guardar_en_archivo()
        return producto

    def obtener_por_id(self, producto_id: str) -> Optional[Producto]:
        """Retorna el producto asociado al ID o None si no existe."""
        return self._productos.get(producto_id)

    def listar_todos(self) -> list[Producto]:
        """Retorna una lista con todos los productos almacenados."""
        return list(self._productos.values())

    def eliminar(self, producto_id: str) -> bool:
        """Elimina un producto por ID. Retorna True si existía."""
        if producto_id not in self._productos:
            return False
        del self._productos[producto_id]
        self._guardar_en_archivo()
        return True