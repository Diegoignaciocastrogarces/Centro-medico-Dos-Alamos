from flask import Flask, render_template
from views import bp 
import firebase_admin
from firebase_admin import credentials

app=Flask(__name__)


#Conexión a base de datos Firebase
cred = credentials.Certificate("app/firebase_key.json")
firebase_admin.initialize_app(cred)

app.register_blueprint(bp)

if __name__=='__main__':
    app.run(debug=True, port=5000) 