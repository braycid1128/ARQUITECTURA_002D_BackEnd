from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:5555@localhost/db_elmirador'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# **Modelos para todas las tablas**
class Acceso(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    fechaCreacion = db.Column(db.DateTime, nullable=False)
    fechaultimoacceso = db.Column(db.DateTime, nullable=True)
    Rut = db.Column(db.String(12), nullable=False)
    Tipo = db.Column(db.String(20), nullable=False)

class Propietario(db.Model):
    RutProp = db.Column(db.String(12), primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    ApePat = db.Column(db.String(50), nullable=False)
    ApeMat = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Fono1 = db.Column(db.String(15), nullable=False)
    Fono2 = db.Column(db.String(15), nullable=True)
    Estado = db.Column(db.String(20), nullable=False)

class Arrendatario(db.Model):
    RutArre = db.Column(db.String(12), primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    ApePat = db.Column(db.String(50), nullable=False)
    ApeMat = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Fono1 = db.Column(db.String(15), nullable=False)
    Fono2 = db.Column(db.String(15), nullable=True)
    Estado = db.Column(db.String(20), nullable=False)

class Personal(db.Model):
    RutPersonal = db.Column(db.String(12), primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    ApePat = db.Column(db.String(50), nullable=False)
    ApeMat = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Fono1 = db.Column(db.String(15), nullable=False)
    Fono2 = db.Column(db.String(15), nullable=True)
    Estado = db.Column(db.String(20), nullable=False)
    IDCargo = db.Column(db.Integer, nullable=False)
    HoraInicioJ = db.Column(db.Time, nullable=False)
    HoraFinJ = db.Column(db.Date, nullable=True)

class Edificio(db.Model):
    Cod = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Direccion = db.Column(db.String(200), nullable=False)
    Inmobiliaria = db.Column(db.String(100), nullable=False)
    Lat = db.Column(db.Float, nullable=False)
    Log = db.Column(db.Float, nullable=False)
    Estado = db.Column(db.String(20), nullable=False)
    NPisos = db.Column(db.Integer, nullable=False)
    ValorGastoComun = db.Column(db.Float, nullable=False)

class Departamento(db.Model):
    CodDepto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codEdificio = db.Column(db.Integer, db.ForeignKey('edificio.Cod'), nullable=False)
    Piso = db.Column(db.Integer, nullable=False)
    Numero = db.Column(db.Integer, nullable=False)
    Arrendado = db.Column(db.Boolean, nullable=False)
    RutProp = db.Column(db.String(12), db.ForeignKey('propietario.RutProp'), nullable=True)
    Estado = db.Column(db.String(20), nullable=False)
    RutArre = db.Column(db.String(12), db.ForeignKey('arrendatario.RutArre'), nullable=True)
    FechaIniC = db.Column(db.Date, nullable=True)
    FechaFinC = db.Column(db.Date, nullable=True)
    Observacion = db.Column(db.Text, nullable=True)
    NumHab = db.Column(db.Integer, nullable=False)
    NumBaños = db.Column(db.Integer, nullable=False)

class Reclamo(db.Model):
    IDReclamo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FechaReclamo = db.Column(db.Date, nullable=False)
    TextoReclamo = db.Column(db.Text, nullable=False)
    IdTipoReclamo = db.Column(db.Integer, db.ForeignKey('tipos_reclamo.IDTipoReclamo'), nullable=False)
    RutArre = db.Column(db.String(12), db.ForeignKey('arrendatario.RutArre'), nullable=False)
    visto = db.Column(db.Boolean, nullable=False, default=False)
    fechavisto = db.Column(db.Date, nullable=True)
    estado = db.Column(db.String(20), nullable=False)

class CuotaGC(db.Model):
    IdCuotaGC = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Mes = db.Column(db.String(10), nullable=False)
    Año = db.Column(db.Integer, nullable=False)
    ValorPagado = db.Column(db.Float, nullable=False)
    FechaPago = db.Column(db.Date, nullable=True)
    Atrazado = db.Column(db.Boolean, nullable=False)
    CodDepto = db.Column(db.Integer, db.ForeignKey('departamento.CodDepto'), nullable=False)
    Rut = db.Column(db.String(12), nullable=False)
    Nombre = db.Column(db.String(50), nullable=False)
    Telefono = db.Column(db.String(15), nullable=False)

class Proyecto(db.Model):
    IdProy = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Motivo = db.Column(db.Text, nullable=False)
    Valor = db.Column(db.Float, nullable=False)
    FechaInicioCobros = db.Column(db.Date, nullable=False)
    FechaFinCobros = db.Column(db.Date, nullable=True)
    estado = db.Column(db.String(20), nullable=False)

class ProyectoDepto(db.Model):
    IdProy = db.Column(db.Integer, db.ForeignKey('proyecto.IdProy'), primary_key=True)
    CodDepto = db.Column(db.Integer, db.ForeignKey('departamento.CodDepto'), primary_key=True)
    IdCuota = db.Column(db.Integer, db.ForeignKey('cuota_gc.IdCuotaGC'), primary_key=True)
    FechaPago = db.Column(db.Date, nullable=True)
    ValorPagado = db.Column(db.Float, nullable=True)

class Cargo(db.Model):
    IDCargo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NombreCargo = db.Column(db.String(50), nullable=False)

class TiposReclamo(db.Model):
    IDTipoReclamo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descripcion = db.Column(db.String(100), nullable=False)






# ** CRUD para cada tabla **

# acceso
@app.route('/accesos', methods=['GET'])
def get_accesos():
    accesos = Acceso.query.all()
    return jsonify([{
        'username': acceso.username,
        'password': acceso.password,
        'fechaCreacion': acceso.fechaCreacion,
        'fechaultimoacceso': acceso.fechaultimoacceso,
        'Rut': acceso.Rut,
        'Tipo': acceso.Tipo
    } for acceso in accesos])

@app.route('/accesos', methods=['POST'])
def create_acceso():
    data = request.get_json()
    nuevo_acceso = Acceso(
        username=data['username'],
        password=data['password'],
        fechaCreacion=data['fechaCreacion'],
        fechaultimoacceso=data.get('fechaultimoacceso'),
        Rut=data['Rut'],
        Tipo=data['Tipo']
    )
    db.session.add(nuevo_acceso)
    db.session.commit()
    return jsonify({'message': 'Acceso creado exitosamente'})

@app.route('/accesos/<string:username>', methods=['PUT'])
def update_acceso(username):
    acceso = Acceso.query.get(username)
    if not acceso:
        return jsonify({'message': 'Acceso no encontrado'}), 404
    data = request.get_json()
    acceso.password = data['password']
    acceso.fechaultimoacceso = data.get('fechaultimoacceso')
    acceso.Rut = data['Rut']
    acceso.Tipo = data['Tipo']
    db.session.commit()
    return jsonify({'message': 'Acceso actualizado exitosamente'})

@app.route('/accesos/<string:username>', methods=['DELETE'])
def delete_acceso(username):
    acceso = Acceso.query.get(username)
    if not acceso:
        return jsonify({'message': 'Acceso no encontrado'}), 404
    db.session.delete(acceso)
    db.session.commit()
    return jsonify({'message': 'Acceso eliminado exitosamente'})

#propietario
@app.route('/propietarios', methods=['GET'])
def get_propietarios():
    propietarios = Propietario.query.all()
    return jsonify([{
        'RutProp': propietario.RutProp,
        'Nombre': propietario.Nombre,
        'ApePat': propietario.ApePat,
        'ApeMat': propietario.ApeMat,
        'Email': propietario.Email,
        'Fono1': propietario.Fono1,
        'Fono2': propietario.Fono2,
        'Estado': propietario.Estado
    } for propietario in propietarios])

@app.route('/propietarios', methods=['POST'])
def create_propietario():
    data = request.get_json()
    nuevo_propietario = Propietario(
        RutProp=data['RutProp'],
        Nombre=data['Nombre'],
        ApePat=data['ApePat'],
        ApeMat=data['ApeMat'],
        Email=data['Email'],
        Fono1=data['Fono1'],
        Fono2=data.get('Fono2'),
        Estado=data['Estado']
    )
    db.session.add(nuevo_propietario)
    db.session.commit()
    return jsonify({'message': 'Propietario creado exitosamente'})

@app.route('/propietarios/<string:RutProp>', methods=['PUT'])
def update_propietario(RutProp):
    propietario = Propietario.query.get(RutProp)
    if not propietario:
        return jsonify({'message': 'Propietario no encontrado'}), 404
    data = request.get_json()
    propietario.Nombre = data['Nombre']
    propietario.ApePat = data['ApePat']
    propietario.ApeMat = data['ApeMat']
    propietario.Email = data['Email']
    propietario.Fono1 = data['Fono1']
    propietario.Fono2 = data.get('Fono2')
    propietario.Estado = data['Estado']
    db.session.commit()
    return jsonify({'message': 'Propietario actualizado exitosamente'})

@app.route('/propietarios/<string:RutProp>', methods=['DELETE'])
def delete_propietario(RutProp):
    propietario = Propietario.query.get(RutProp)
    if not propietario:
        return jsonify({'message': 'Propietario no encontrado'}), 404
    db.session.delete(propietario)
    db.session.commit()
    return jsonify({'message': 'Propietario eliminado exitosamente'})


#arrendatarios
@app.route('/arrendatarios', methods=['GET'])
def get_arrendatarios():
    arrendatarios = Arrendatario.query.all()
    return jsonify([{
        'RutArre': arrendatario.RutArre,
        'Nombre': arrendatario.Nombre,
        'ApePat': arrendatario.ApePat,
        'ApeMat': arrendatario.ApeMat,
        'Email': arrendatario.Email,
        'Fono1': arrendatario.Fono1,
        'Fono2': arrendatario.Fono2,
        'Estado': arrendatario.Estado
    } for arrendatario in arrendatarios])

@app.route('/arrendatarios', methods=['POST'])
def create_arrendatario():
    data = request.get_json()
    nuevo_arrendatario = Arrendatario(
        RutArre=data['RutArre'],
        Nombre=data['Nombre'],
        ApePat=data['ApePat'],
        ApeMat=data['ApeMat'],
        Email=data['Email'],
        Fono1=data['Fono1'],
        Fono2=data.get('Fono2'),
        Estado=data['Estado']
    )
    db.session.add(nuevo_arrendatario)
    db.session.commit()
    return jsonify({'message': 'Arrendatario creado exitosamente'})

@app.route('/arrendatarios/<string:RutArre>', methods=['PUT'])
def update_arrendatario(RutArre):
    arrendatario = Arrendatario.query.get(RutArre)
    if not arrendatario:
        return jsonify({'message': 'Arrendatario no encontrado'}), 404
    data = request.get_json()
    arrendatario.Nombre = data['Nombre']
    arrendatario.ApePat = data['ApePat']
    arrendatario.ApeMat = data['ApeMat']
    arrendatario.Email = data['Email']
    arrendatario.Fono1 = data['Fono1']
    arrendatario.Fono2 = data.get('Fono2')
    arrendatario.Estado = data['Estado']
    db.session.commit()
    return jsonify({'message': 'Arrendatario actualizado exitosamente'})

@app.route('/arrendatarios/<string:RutArre>', methods=['DELETE'])
def delete_arrendatario(RutArre):
    arrendatario = Arrendatario.query.get(RutArre)
    if not arrendatario:
        return jsonify({'message': 'Arrendatario no encontrado'}), 404
    db.session.delete(arrendatario)
    db.session.commit()
    return jsonify({'message': 'Arrendatario eliminado exitosamente'})


#Personal
@app.route('/personal', methods=['GET'])
def get_personales():
    personales = Personal.query.all()
    return jsonify([{
        'RutPersonal': personal.RutPersonal,
        'Nombre': personal.Nombre,
        'ApePat': personal.ApePat,
        'ApeMat': personal.ApeMat,
        'Email': personal.Email,
        'Fono1': personal.Fono1,
        'Fono2': personal.Fono2,
        'Estado': personal.Estado,
        'IDCargo': personal.IDCargo,
        'HoraInicioJ': personal.HoraInicioJ,
        'HoraFinJ': personal.FechaFinJ
    } for personal in personales])

@app.route('/personal', methods=['POST'])
def create_personal():
    data = request.get_json()
    nuevo_personal = Personal(
        RutPersonal=data['RutPersonal'],
        Nombre=data['Nombre'],
        ApePat=data['ApePat'],
        ApeMat=data['ApeMat'],
        Email=data['Email'],
        Fono1=data['Fono1'],
        Fono2=data.get('Fono2'),
        Estado=data['Estado'],
        IDCargo=data['IDCargo'],
        HoraInicioJ=data['HoraInicioJ'],
        HoraFinJ=data.get('HoraFinJ')
    )
    db.session.add(nuevo_personal)
    db.session.commit()
    return jsonify({'message': 'Personal creado exitosamente'})

@app.route('/personal/<string:RutPersonal>', methods=['PUT'])
def update_personal(RutPersonal):
    personal = Personal.query.get(RutPersonal)
    if not personal:
        return jsonify({'message': 'Personal no encontrado'}), 404
    data = request.get_json()
    personal.Nombre = data['Nombre']
    personal.ApePat = data['ApePat']
    personal.ApeMat = data['ApeMat']
    personal.Email = data['Email']
    personal.Fono1 = data['Fono1']
    personal.Fono2 = data.get('Fono2')
    personal.Estado = data['Estado']
    personal.IDCargo = data['IDCargo']
    personal.HoraInicioJ = data['HoraInicioJ']
    personal.HoraFinJ = data.get('HoraFinJ')
    db.session.commit()
    return jsonify({'message': 'Personal actualizado exitosamente'})

@app.route('/personal/<string:RutPersonal>', methods=['DELETE'])
def delete_personal(RutPersonal):
    personal = Personal.query.get(RutPersonal)
    if not personal:
        return jsonify({'message': 'Personal no encontrado'}), 404
    db.session.delete(personal)
    db.session.commit()
    return jsonify({'message': 'Personal eliminado exitosamente'})


#Edificios
@app.route('/edificios', methods=['GET'])
def get_edificios():
    edificios = Edificio.query.all()
    return jsonify([{
        'Cod': edificio.Cod,
        'Nombre': edificio.Nombre,
        'Direccion': edificio.Direccion,
        'Inmobiliaria': edificio.Inmobiliaria,
        'Lat': edificio.Lat,
        'Log': edificio.Log,
        'Estado': edificio.Estado,
        'NPisos': edificio.NPisos,
        'ValorGastoComun': edificio.ValorGastoComun
    } for edificio in edificios])

@app.route('/edificios', methods=['POST'])
def create_edificio():
    data = request.get_json()
    nuevo_edificio = Edificio(
        Cod=data['Cod'],
        Nombre=data['Nombre'],
        Direccion=data['Direccion'],
        Inmobiliaria=data['Inmobiliaria'],
        Lat=data['Lat'],
        Log=data['Log'],
        Estado=data['Estado'],
        NPisos=data['NPisos'],
        ValorGastoComun=data['ValorGastoComun']
    )
    db.session.add(nuevo_edificio)
    db.session.commit()
    return jsonify({'message': 'Edificio creado exitosamente'})

@app.route('/edificios/<string:Cod>', methods=['PUT'])
def update_edificio(Cod):
    edificio = Edificio.query.get(Cod)
    if not edificio:
        return jsonify({'message': 'Edificio no encontrado'}), 404
    data = request.get_json()
    edificio.Nombre = data['Nombre']
    edificio.Direccion = data['Direccion']
    edificio.Inmobiliaria = data['Inmobiliaria']
    edificio.Lat = data['Lat']
    edificio.Log = data['Log']
    edificio.Estado = data['Estado']
    edificio.NPisos = data['NPisos']
    edificio.ValorGastoComun = data['ValorGastoComun']
    db.session.commit()
    return jsonify({'message': 'Edificio actualizado exitosamente'})

@app.route('/edificios/<string:Cod>', methods=['DELETE'])
def delete_edificio(Cod):
    edificio = Edificio.query.get(Cod)
    if not edificio:
        return jsonify({'message': 'Edificio no encontrado'}), 404
    db.session.delete(edificio)
    db.session.commit()
    return jsonify({'message': 'Edificio eliminado exitosamente'})


#Departamentos
@app.route('/departamentos', methods=['GET'])
def get_departamentos():
    departamentos = Departamento.query.all()
    return jsonify([{
        'CodDepto': depto.CodDepto,
        'codEdificio': depto.codEdificio,
        'Piso': depto.Piso,
        'Numero': depto.Numero,
        'Arrendado': depto.Arrendado,
        'RutProp': depto.RutProp,
        'Estado': depto.Estado,
        'RutArre': depto.RutArre,
        'FechaIniC': depto.FechaIniC,
        'FechaFinC': depto.FechaFinC,
        'Observacion': depto.Observacion,
        'NumHab': depto.NumHab,
        'NumBaños': depto.NumBaños
    } for depto in departamentos])

@app.route('/departamentos', methods=['POST'])
def create_departamento():
    data = request.get_json()
    nuevo_depto = Departamento(
        CodDepto=data['CodDepto'],
        codEdificio=data['codEdificio'],
        Piso=data['Piso'],
        Numero=data['Numero'],
        Arrendado=data['Arrendado'],
        RutProp=data['RutProp'],
        Estado=data['Estado'],
        RutArre=data['RutArre'],
        FechaIniC=data['FechaIniC'],
        FechaFinC=data.get('FechaFinC'),
        Observacion=data['Observacion'],
        NumHab=data['NumHab'],
        NumBaños=data['NumBaños']
    )
    db.session.add(nuevo_depto)
    db.session.commit()
    return jsonify({'message': 'Departamento creado exitosamente'})

@app.route('/departamentos/<string:CodDepto>', methods=['PUT'])
def update_departamento(CodDepto):
    depto = Departamento.query.get(CodDepto)
    if not depto:
        return jsonify({'message': 'Departamento no encontrado'}), 404
    data = request.get_json()
    depto.Piso = data['Piso']
    depto.Numero = data['Numero']
    depto.Arrendado = data['Arrendado']
    depto.RutProp = data['RutProp']
    depto.Estado = data['Estado']
    depto.RutArre = data['RutArre']
    depto.FechaIniC = data['FechaIniC']
    depto.FechaFinC = data.get('FechaFinC')
    depto.Observacion = data['Observacion']
    depto.NumHab = data['NumHab']
    depto.NumBaños = data['NumBaños']
    db.session.commit()
    return jsonify({'message': 'Departamento actualizado exitosamente'})

@app.route('/departamentos/<string:CodDepto>', methods=['DELETE'])
def delete_departamento(CodDepto):
    depto = Departamento.query.get(CodDepto)
    if not depto:
        return jsonify({'message': 'Departamento no encontrado'}), 404
    db.session.delete(depto)
    db.session.commit()
    return jsonify({'message': 'Departamento eliminado exitosamente'})


#reclamos
@app.route('/reclamos', methods=['GET'])
def get_reclamos():
    reclamos = Reclamo.query.all()
    return jsonify([{
        'IDReclamo': reclamo.IDReclamo,
        'FechaReclamo': reclamo.FechaReclamo,
        'TextoReclamo': reclamo.TextoReclamo,
        'IdTipoReclamo': reclamo.IdTipoReclamo,
        'RutArre': reclamo.RutArre,
        'Visto': reclamo.visto,
        'FechaVisto': reclamo.fechavisto,
        'Estado': reclamo.estado
    } for reclamo in reclamos])

@app.route('/reclamos', methods=['POST'])
def create_reclamo():
    data = request.get_json()
    nuevo_reclamo = Reclamo(
        FechaReclamo=data['FechaReclamo'],
        TextoReclamo=data['TextoReclamo'],
        IdTipoReclamo=data['IdTipoReclamo'],
        RutArre=data['RutArre'],
        visto=data.get('visto', False),
        fechavisto=data.get('FechaVisto'),
        estado=data['estado']
    )
    db.session.add(nuevo_reclamo)
    db.session.commit()
    return jsonify({'message': 'Reclamo creado exitosamente'})

@app.route('/reclamos/<int:IDReclamo>', methods=['PUT'])
def update_reclamo(IDReclamo):
    reclamo = Reclamo.query.get(IDReclamo)
    if not reclamo:
        return jsonify({'message': 'Reclamo no encontrado'}), 404
    data = request.get_json()
    reclamo.FechaRechamo = data['FechaReclamo']
    reclamo.TextoReclamo = data['TextoReclamo']
    reclamo.IdTipoReclamo = data['IdTipoReclamo']
    reclamo.RutArre = data['RutArre']
    reclamo.visto = data.get('visto', reclamo.visto)
    reclamo.fechavisto = data.get('FechaVisto', reclamo.fechavisto)
    reclamo.estado = data['estado']
    db.session.commit()
    return jsonify({'message': 'Reclamo actualizado exitosamente'})

@app.route('/reclamos/<int:IDReclamo>', methods=['DELETE'])
def delete_reclamo(IDReclamo):
    reclamo = Reclamo.query.get(IDReclamo)
    if not reclamo:
        return jsonify({'message': 'Reclamo no encontrado'}), 404
    db.session.delete(reclamo)
    db.session.commit()
    return jsonify({'message': 'Reclamo eliminado exitosamente'})


#cuotas
@app.route('/cuotas_gc', methods=['GET'])
def get_cuotas_gc():
    cuotas = CuotaGC.query.all()
    return jsonify([{
        'IdCuotaGC': cuota.IdCuotaGC,
        'Mes': cuota.Mes,
        'Año': cuota.Año,
        'ValorPagado': cuota.ValorPagado,
        'FechaPago': cuota.FechaPago,
        'Atrazado': cuota.Atrazado,
        'CodDepto': cuota.CodDepto,
        'Rut': cuota.Rut,
        'Nombre': cuota.Nombre,
        'Telefono': cuota.Telefono
    } for cuota in cuotas])

@app.route('/cuotas_gc', methods=['POST'])
def create_cuota_gc():
    data = request.get_json()
    nueva_cuota = CuotaGC(
        Mes=data['Mes'],
        Año=data['Año'],
        ValorPagado=data['ValorPagado'],
        FechaPago=data['FechaPago'],
        Atrazado=data['Atrazado'],
        CodDepto=data['CodDepto'],
        Rut=data['Rut'],
        Nombre=data['Nombre'],
        Telefono=data['Telefono']
    )
    db.session.add(nueva_cuota)
    db.session.commit()
    return jsonify({'message': 'Cuota de Gasto Común creada exitosamente'})

@app.route('/cuotas_gc/<int:IdCuotaGC>', methods=['PUT'])
def update_cuota_gc(IdCuotaGC):
    cuota = CuotaGC.query.get(IdCuotaGC)
    if not cuota:
        return jsonify({'message': 'Cuota de Gasto Común no encontrada'}), 404
    data = request.get_json()
    cuota.Mes = data['Mes']
    cuota.Año = data['Año']
    cuota.ValorPagado = data['ValorPagado']
    cuota.FechaPago = data['FechaPago']
    cuota.Atrazado = data['Atrazado']
    cuota.CodDepto = data['CodDepto']
    cuota.Rut = data['Rut']
    cuota.Nombre = data['Nombre']
    cuota.Telefono = data['Telefono']
    db.session.commit()
    return jsonify({'message': 'Cuota de Gasto Común actualizada exitosamente'})

@app.route('/cuotas_gc/<int:IdCuotaGC>', methods=['DELETE'])
def delete_cuota_gc(IdCuotaGC):
    cuota = CuotaGC.query.get(IdCuotaGC)
    if not cuota:
        return jsonify({'message': 'Cuota de Gasto Común no encontrada'}), 404
    db.session.delete(cuota)
    db.session.commit()
    return jsonify({'message': 'Cuota de Gasto Común eliminada exitosamente'})


#proyecto
@app.route('/proyectos', methods=['GET'])
def get_proyectos():
    proyectos = Proyecto.query.all()
    return jsonify([{
        'IdProy': proyecto.IdProy,
        'Motivo': proyecto.Motivo,
        'Valor': proyecto.Valor,
        'FechaInicioCobros': proyecto.FechaInicioCobros,
        'FechaFinCobros': proyecto.FechaFinCobros,
        'Estado': proyecto.estado
    } for proyecto in proyectos])

@app.route('/proyectos', methods=['POST'])
def create_proyecto():
    data = request.get_json()
    nuevo_proyecto = Proyecto(
        Motivo=data['Motivo'],
        Valor=data['Valor'],
        FechaInicioCobros=data['FechaInicioCobros'],
        FechaFinCobros=data['FechaFinCobros'],
        Estado=data['Estado']
    )
    db.session.add(nuevo_proyecto)
    db.session.commit()
    return jsonify({'message': 'Proyecto creado exitosamente'})

@app.route('/proyectos/<int:IdProy>', methods=['PUT'])
def update_proyecto(IdProy):
    proyecto = Proyecto.query.get(IdProy)
    if not proyecto:
        return jsonify({'message': 'Proyecto no encontrado'}), 404
    data = request.get_json()
    proyecto.Motivo = data['Motivo']
    proyecto.Valor = data['Valor']
    proyecto.FechaInicioCobros = data['FechaInicioCobros']
    proyecto.FechaFinCobros = data['FechaFinCobros']
    proyecto.Estado = data['Estado']
    db.session.commit()
    return jsonify({'message': 'Proyecto actualizado exitosamente'})

@app.route('/proyectos/<int:IdProy>', methods=['DELETE'])
def delete_proyecto(IdProy):
    proyecto = Proyecto.query.get(IdProy)
    if not proyecto:
        return jsonify({'message': 'Proyecto no encontrado'}), 404
    db.session.delete(proyecto)
    db.session.commit()
    return jsonify({'message': 'Proyecto eliminado exitosamente'})


#proyectoDepto
@app.route('/proyecto_depto', methods=['GET'])
def get_proyectos_depto():
    proyectos_depto = ProyectoDepto.query.all()
    return jsonify([{
        'IdProy': proyecto_depto.IdProy,
        'CodDepto': proyecto_depto.CodDepto,
        'IdCuota': proyecto_depto.IdCuota,
        'FechaPago': proyecto_depto.FechaPago,
        'ValorPagado': proyecto_depto.ValorPagado
    } for proyecto_depto in proyectos_depto])

@app.route('/proyecto_depto', methods=['POST'])
def create_proyecto_depto():
    data = request.get_json()
    nuevo_proyecto_depto = ProyectoDepto(
        IdProy=data['IdProy'],
        CodDepto=data['CodDepto'],
        IdCuota=data['IdCuota'],
        FechaPago=data['FechaPago'],
        ValorPagado=data['ValorPagado']
    )
    db.session.add(nuevo_proyecto_depto)
    db.session.commit()
    return jsonify({'message': 'ProyectoDepartamento creado exitosamente'})

@app.route('/proyecto_depto/<int:IdProy>', methods=['PUT'])
def update_proyecto_depto(IdProy):
    proyecto_depto = ProyectoDepto.query.get(IdProy)
    if not proyecto_depto:
        return jsonify({'message': 'ProyectoDepartamento no encontrado'}), 404
    data = request.get_json()
    proyecto_depto.CodDepto = data['CodDepto']
    proyecto_depto.IdCuota = data['IdCuota']
    proyecto_depto.FechaPago = data['FechaPago']
    proyecto_depto.ValorPagado = data['ValorPagado']
    db.session.commit()
    return jsonify({'message': 'ProyectoDepartamento actualizado exitosamente'})

@app.route('/proyecto_depto/<int:IdProy>', methods=['DELETE'])
def delete_proyecto_depto(IdProy):
    proyecto_depto = ProyectoDepto.query.get(IdProy)
    if not proyecto_depto:
        return jsonify({'message': 'ProyectoDepartamento no encontrado'}), 404
    db.session.delete(proyecto_depto)
    db.session.commit()
    return jsonify({'message': 'ProyectoDepartamento eliminado exitosamente'})


#Cargos
@app.route('/cargos', methods=['GET'])
def get_cargos():
    cargos = Cargo.query.all()
    return jsonify([{
        'IDCargo': cargo.IDCargo,
        'NombreCargo': cargo.NombreCargo
    } for cargo in cargos])

@app.route('/cargos', methods=['POST'])
def create_cargo():
    data = request.get_json()
    nuevo_cargo = Cargo(
        NombreCargo=data['NombreCargo']
    )
    db.session.add(nuevo_cargo)
    db.session.commit()
    return jsonify({'message': 'Cargo creado exitosamente'})

@app.route('/cargos/<int:IDCargo>', methods=['PUT'])
def update_cargo(IDCargo):
    cargo = Cargo.query.get(IDCargo)
    if not cargo:
        return jsonify({'message': 'Cargo no encontrado'}), 404
    data = request.get_json()
    cargo.NombreCargo = data['NombreCargo']
    db.session.commit()
    return jsonify({'message': 'Cargo actualizado exitosamente'})

@app.route('/cargos/<int:IDCargo>', methods=['DELETE'])
def delete_cargo(IDCargo):
    cargo = Cargo.query.get(IDCargo)
    if not cargo:
        return jsonify({'message': 'Cargo no encontrado'}), 404
    db.session.delete(cargo)
    db.session.commit()
    return jsonify({'message': 'Cargo eliminado exitosamente'})

#tipos reclamos
@app.route('/tipos_reclamo', methods=['GET'])
def get_tipos_reclamo():
    tipos_reclamo = TiposReclamo.query.all()
    return jsonify([{
        'IDTipoReclamo': tipo_reclamo.IDTipoReclamo,
        'Descripcion': tipo_reclamo.Descripcion
    } for tipo_reclamo in tipos_reclamo])

@app.route('/tipos_reclamo', methods=['POST'])
def create_tipo_reclamo():
    data = request.get_json()
    nuevo_tipo_reclamo = TiposReclamo(
        Descripcion=data['Descripcion']
    )
    db.session.add(nuevo_tipo_reclamo)
    db.session.commit()
    return jsonify({'message': 'Tipo de Reclamo creado exitosamente'})

@app.route('/tipos_reclamo/<int:IDTipoReclamo>', methods=['PUT'])
def update_tipo_reclamo(IDTipoReclamo):
    tipo_reclamo = TiposReclamo.query.get(IDTipoReclamo)
    if not tipo_reclamo:
        return jsonify({'message': 'Tipo de Reclamo no encontrado'}), 404
    data = request.get_json()
    tipo_reclamo.Descripcion = data['Descripcion']
    db.session.commit()
    return jsonify({'message': 'Tipo de Reclamo actualizado exitosamente'})

@app.route('/tipos_reclamo/<int:IDTipoReclamo>', methods=['DELETE'])
def delete_tipo_reclamo(IDTipoReclamo):
    tipo_reclamo = TiposReclamo.query.get(IDTipoReclamo)
    if not tipo_reclamo:
        return jsonify({'message': 'Tipo de Reclamo no encontrado'}), 404
    db.session.delete(tipo_reclamo)
    db.session.commit()
    return jsonify({'message': 'Tipo de Reclamo eliminado exitosamente'})




# **Función para convertir objetos a diccionarios**
def record_to_dict(record):
    return {column.name: getattr(record, column.name) for column in record.__table__.columns}

# **Ejecuta la aplicación**
if __name__ == '__main__':
    app.run(debug=True)
