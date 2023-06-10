from flask import Blueprint, render_template, request

bp = Blueprint('views', __name__)


@bp.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['user_password']
        return f'Nombre de usuario: {username}, Contraseña: {password}'
    return render_template('login.html')
