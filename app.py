from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  


@app.before_request
def iniciar_sesion():
    if 'inscritos' not in session:
        session['inscritos'] = []

@app.route('/')
def index():
    return render_template('registro.html')


@app.route('/inscritos')
def inscritos():
    return render_template('listado.html', inscritos=session.get('inscritos', []))

@app.route('/inscribir', methods=['POST'])
def inscribir():
    
    fecha = request.form['fecha']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    turno = request.form['turno']
    

    seminarios = request.form.getlist('seminarios')
    seminarios_seleccionados = '; '.join(seminarios)  
    

    inscrito = {
        'fecha': fecha, 
        'nombre': nombre, 
        'apellido': apellido, 
        'turno': turno, 
        'seminarios': seminarios_seleccionados
    }
    
    session['inscritos'].append(inscrito)
    session.modified = True  

    
    return redirect(url_for('inscritos'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        
        session['inscritos'][id]['fecha'] = request.form['fecha']
        session['inscritos'][id]['nombre'] = request.form['nombre']
        session['inscritos'][id]['apellido'] = request.form['apellido']
        session['inscritos'][id]['turno'] = request.form['turno']
        
        seminarios = request.form.getlist('seminarios')
        session['inscritos'][id]['seminarios'] = '; '.join(seminarios)
        
        session.modified = True
        return redirect(url_for('inscritos'))
    
    inscrito = session['inscritos'][id]
    return render_template('editar.html', inscrito=inscrito, id=id)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    
    session['inscritos'].pop(id)
    session.modified = True
    return redirect(url_for('inscritos'))

@app.route('/reiniciar')
def reiniciar():
    session['inscritos'] = []
    return redirect(url_for('inscritos'))

if __name__ == '__main__':
    app.run(debug=True)