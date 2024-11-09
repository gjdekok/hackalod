from flask import Flask, render_template, request, jsonify, abort
import requests
import os
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/kaart')
def kaart():
    return render_template('kaart.html')

@app.route('/annokaart')
def annokaart():
    return render_template('annokaart.html')

@app.route('/details')
def details():
    place = request.args.get('place')
    return render_template('details.html', place=place)

@app.route('/person/<int:person_id>')
def person(person_id):
    # Determine the place based on the current request (for example, via query string)
    place = request.args.get('place')  # Adjust as needed
    file_path = os.path.join('static', 'details', f'{place}.csv')
    
    if os.path.exists(file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                if int(row["id"]) == person_id:
                    person_data = {
                        "id": row["id"],
                        "naam": row["naam"],
                        "adres": row["adres"],
                        "owner_voornaam": row["owner_voornaam"].strip(),
                        "owner_achternaam": row["owner_achternaam"].strip(),
                        "Wardregister_index": row["Wardregister_index"],
                        "Kaart_Id": row["Kaart_Id"],
                        "iiif": row["iiif"]
                    }
                    return render_template('person.html', person=person_data, place=place)
    
    # If person not found, return 404 error
    abort(404, description="Person not found")

@app.route('/fetch_persons/<place>')
def fetch_persons(place):
    file_path = os.path.join('static', 'details', f'{place}.csv')
    if os.path.exists(file_path):
        persons = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            
            # Debug: Print fieldnames to check for discrepancies
            print("CSV Header Fields:", reader.fieldnames)  # Add this line to see field names in the output
            
            for row in reader:
                persons.append({
                    "id": row["id"].strip(),
                    "naam": row["naam"].strip(),
                    "adres": row["adres"].strip(),
                })
        return jsonify(persons)
    else:
        return jsonify({"error": "File not found"}), 404
    

@app.route('/fetch_wikidata_query/<place>')
def fetch_wikidata_query(place):
    file_path = os.path.join('static', 'details', f'{place}_query.txt')
    if os.path.exists(file_path):
        print("YES")
        with open(file_path, 'r') as file:
            query = file.read()
        return jsonify({"query": query})
    else:
        return jsonify({"error": "Query file not found"}), 404
    
@app.route('/fetch_wikidata')
def fetch_wikidata():
    url = "https://query.wikidata.org/sparql"
  
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    

    params = {
        'query': query,
        'format': 'json'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        data = response.json()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify(data)

@app.route('/fetch_images/<place>')
def fetch_images(place):
    file_path = os.path.join('static', 'details', f'{place}.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            image_urls = file.readlines()
        return jsonify([url.strip() for url in image_urls])
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
