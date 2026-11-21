from dataclasses import asdict, dataclass


@dataclass
class Producto:
    """Representa un producto dentro del registro de inventario."""

    id: str
    nombre: str
    descripcion: str
    precio: float
    cantidad: int

    def __post_init__(self) -> None:
        self.validar()
        self.id = self.id.strip()
        self.nombre = self.nombre.strip()
        self.descripcion = self.descripcion.strip()
        self.precio = float(self.precio)

    def validar(self) -> None:
        """Valida las reglas de negocio de los atributos del producto."""
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("El ID del producto debe ser un texto no vacío.")
        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not isinstance(self.descripcion, str) or not self.descripcion.strip():
            raise ValueError("La descripción del producto no puede estar vacía.")
        if (
            isinstance(self.precio, bool)
            or not isinstance(self.precio, (int, float))
            or self.precio <= 0
        ):
            raise ValueError("El precio debe ser un número mayor que cero.")
        if (
            isinstance(self.cantidad, bool)
            or not isinstance(self.cantidad, int)
            or self.cantidad < 0
        ):
            raise ValueError(
                "La cantidad debe ser un número entero mayor o igual a cero."
            )

    def a_diccionario(self) -> dict[str, str | float | int]:
        """Convierte el producto en un diccionario serializable a JSON."""
        return asdict(self)