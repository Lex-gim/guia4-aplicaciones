Feature: Gestión CRUD de productos

  Scenario: Registro exitoso de un producto
    Given que no existe un producto registrado con el ID "P001"
    When el usuario registra el producto "P001" con nombre "Mouse", descripción "Mouse óptico", precio 85000 y cantidad 10
    Then el producto queda almacenado y disponible para consulta

  Scenario: Error al actualizar un producto inexistente
    Given que no existe un producto registrado con el ID "P999"
    When el usuario intenta actualizar el precio del producto "P999" a 50000
    Then el sistema rechaza la operación indicando que el producto no existe