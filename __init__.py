from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)  

@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2
                                                                                                                                       
@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")
  
# Route pour extraire les minutes d'une date string (comme donné dans l'exercice)
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return {'minutes': minutes}

# Route pour générer l'image du graphique des commits
@app.route('/commits-image/')
def commits_image():
    # URL de l'API GitHub pour récupérer les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    # Faire une requête GET à l'API GitHub
    response = requests.get(url)
    commits_data = response.json()

    # Extraire les minutes de chaque commit
    minutes_list = []
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        minutes_list.append(date_object.minute)

    # Compter le nombre de commits par minute
    minutes_count = {minute: minutes_list.count(minute) for minute in range(60)}

    # Créer le graphique avec matplotlib
    plt.bar(minutes_count.keys(), minutes_count.values(), color='skyblue')
    plt.title('Commits par minute')
    plt.xlabel('Minute')
    plt.ylabel('Nombre de commits')

    # Enregistrer le graphique dans un buffer pour l'afficher en tant qu'image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()  # Fermer le graphique pour libérer la mémoire

    return send_file(img, mimetype='image/png')

# Route pour afficher la page HTML qui contient le graphique
@app.route('/commits/')
def show_commits():
    return render_template('commits.html')

@app.route('/commits-image/')
def commits_image():
    # L'URL de l'API GitHub pour récupérer les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    # Faire une requête GET à l'API GitHub
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifier que la requête s'est bien passée
        commits_data = response.json()
        
        # Afficher les données reçues dans la console Flask pour vérification
        print(commits_data)

        # Tester la génération du graphique avec des données fictives
        minutes_list = [i % 60 for i in range(len(commits_data))]  # Générer des minutes fictives
        minutes_count = {minute: minutes_list.count(minute) for minute in range(60)}

        # Créer le graphique avec matplotlib
        plt.bar(minutes_count.keys(), minutes_count.values(), color='skyblue')
        plt.title('Commits par minute (données fictives)')
        plt.xlabel('Minute')
        plt.ylabel('Nombre de commits')

        # Enregistrer le graphique dans un buffer pour l'afficher en tant qu'image
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return send_file(img, mimetype='image/png')

    except Exception as e:
        print(f"Erreur lors de la récupération ou du traitement des données: {e}")
        return f"Erreur : {e}", 500

if __name__ == "__main__":
  app.run(debug=True)
