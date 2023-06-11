from flask import Flask, render_template
from views import bp 


app=Flask(__name__)

app.register_blueprint(bp)

def pagina_no_encontrada(error):
    return render_template('404.html'), 404

if __name__=='__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000) 