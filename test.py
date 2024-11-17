from crud_operaciones import create_record

# Datos a insertar en la tabla "Cargos"
data = {"NombreCargo": "Administrador"}

# Llamada a la función para insertar
create_record("Cargos", data)
