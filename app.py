from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np
app = Flask(__name__)
app.secret_key = 'secret_key'  # Assurez-vous de changer cela dans un environnement de production


# fonction pour load le model
def getBestModel():
    with open('bestModel.h5', 'rb') as file:
        model = pickle.load(file)
    return model


bestModel=getBestModel()


# cette fonction prend en parametre l'age et salaire et retourne la prediction 
def getPrediction(age, salary):
    data = np.array([[age, salary]])
    prediction = bestModel.predict(data)
    return prediction[0]

# Liste d'utilisateurs pour la démo (en cas professionel on peut une base de données)
users = {'amina': 'amina123', 'djo': '123'}

# route pour l'authentification
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifie si l'utilisateur et le mot de passe sont valides
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect('predict_purchase')
        else:
            error = 'Identifiants incorrects. Veuillez réessayer.'

    return render_template('login.html', error=error)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/predict_purchase', methods=['GET', 'POST'])
def prediction_form():
    if request.method == 'POST':
        age = float(request.form['age'])
        salary = float(request.form['salary'])
        prediction = getPrediction(age, salary)
        print(prediction)
        if prediction == 1:
            result = "L'utilisateur est susceptible d'acheter le produit"
        else:
            result = "L'utilisateur n'est probablement pas susceptible d'acheter le produit"
        return render_template('prediction_result.html', result=result)
    return render_template('prediction_form.html')


if __name__ == '__main__':
    app.run(debug=True)
