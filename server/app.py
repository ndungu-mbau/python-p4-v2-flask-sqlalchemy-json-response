# server/app.py
#!/usr/bin/env python3
import os
from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    res = {'message': 'Welcome to the pet directory!'}
    return make_response(res, 200)


@app.route('/demo_json')
def demo_json():
    pet_json = {"id": 1, "name" : "Fido", "species" : "Dog"}
    return make_response(pet_json, 200)


@app.route('/pets/<int:id>')
def get_pet(id):
    pet = Pet.query.get(id)
    if pet:
        res = {
            'id': pet.id,
            'name': pet.name,
            'species': pet.species
        }
        status = 200
    else:
        res = { 'message': f'Pet with id {id} not found' }
        status = 404

    return make_response(res, status)

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = []  # array to store a dictionary for each pet
    for pet in Pet.query.filter_by(species=species).all():
        pet_dict = {'id': pet.id,
                    'name': pet.name,
                    'species': pet.species
                    }
        pets.append(pet_dict)
    body = {'count': len(pets),
            'pets': pets
            }
    return make_response(body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
