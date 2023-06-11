from flask import Blueprint, render_template, request, redirect, url_for
from config import db

bp = Blueprint('views', __name__)


@bp.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['user_password']
    
        ref_usuario = db.collection('Usuarios')
        query = ref_usuario.where('Username', '==', username).where('Password', '==', password)
        resultado = query.get()
        
        if resultado:
            return redirect(url_for('views.inicio_medico', nombre = username))
        else:
            return 'Credenciales de inicio de sesión inválidas'
        
    return render_template('login.html')

@bp.route('/inicioMedico/<nombre>')
def inicio_medico(nombre):
    ref_usuario = db.collection('Usuarios')
    query = ref_usuario.where('Username', '==', nombre)
    resultado = query.get()
    
    doc = resultado[0]   
    data = doc.to_dict()
    print(data)
    
    
    user_data = {
        'Username' : data['Username'],
        'FirstName': data['FirstName'],
        'LastName': data['LastName'],
        'Rol': data['Rol'],
        'Sexo': data['Sexo']
    }
    
    if resultado:
        return render_template('inicio-medico.html', nombre = nombre, userData = user_data)
    else:
        return render_template('404.html')
    
@bp.route('/inicioMedico/<nombre>/listadoPacientes')
def listado_pacientes(nombre):
    ref_usuario = db.collection('Usuarios')
    query = ref_usuario.where('Username', '==', nombre)
    resultado = query.get()
    
    doc = resultado[0]   
    data = doc.to_dict()
    print(data)
    
    medic_name = data['Username']
    
    ref_atencion_medica = db.collection('Atencion Medica')
    query_atencion = ref_atencion_medica.where('MedicUserName', '==', medic_name)
    atencion_resultado = query_atencion.get()
    
    pacientes_list = []
    
    for atencion_doc in atencion_resultado:
        atencion_data = atencion_doc.to_dict()
        paciente_id = atencion_data['RutPaciente']
        
        ref_paciente = db.collection('Pacientes')
        query_paciente = ref_paciente.where('RUT', '==', paciente_id).get()
        
        for paciente_doc in query_paciente:
            if paciente_doc.exists:
                
                paciente_data = paciente_doc.to_dict()
                pacientes_list.append(paciente_data)
    
    if resultado:
        return render_template('listado-pacientes.html', nombre = nombre, pacientes = pacientes_list)
    else:
        return render_template('404.html')
    
    

