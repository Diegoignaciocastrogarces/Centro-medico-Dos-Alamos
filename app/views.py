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

    if resultado:
        doc = resultado[0]
        data = doc.to_dict()
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
                paciente_data = paciente_doc.to_dict()
                pacientes_list.append(paciente_data)

        return render_template('listado-pacientes.html', nombre=nombre, pacientes=pacientes_list)
    else:
        return render_template('404.html')
    
    
@bp.route('/listadoPacientes/historialClinico/<rut>')
def historial_clinico_paciente(rut):
    ref_historial = db.collection('Historial Clinico')
    query_historial = ref_historial.where('RutPaciente', '==', rut)
    historial_resultado = query_historial.get()
    
    data = {}
    
    for historial_doc in historial_resultado:
        historial_data = historial_doc.to_dict()
        
        #Obtener los datos de patient(ObjectReference) de Cloud Firestore
        paciente_ref = historial_data['patient']
        paciente_doc = paciente_ref.get()
        paciente_resultado = paciente_doc.to_dict()
    
        
        historial_dict = {
            'Rut_paciente': historial_data['RutPaciente'],
            'Paciente': paciente_resultado,
            'Antecedentes': historial_data['Antecedentes medicos'],
            'Consultas': historial_data['Consultas tratamiento'],
            'Medicamentos': historial_data['Medicamentos'],
            'Resultados_pruebas': historial_data['Resultado pruebas'],
            'Notas_medico': historial_data['Notas medico']
        }
        
        data = historial_dict
        
   
    return render_template('historial-clinico-paciente.html', rut = rut, historial_data = data)

