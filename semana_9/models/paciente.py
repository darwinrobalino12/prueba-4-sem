class Paciente:
    def __init__(self, id_paciente=None, nombre=None, apellido=None, cedula=None, telefono=None, email=None):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.telefono = telefono
        self.email = email