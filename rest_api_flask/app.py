from flask import Flask, request
import db_interactions
import json

app = Flask(__name__)

db_interactions.initdb()

@app.route('/api/kids')
def get_kids():
    kids = json.dumps(db_interactions.get_kids())
    return kids

@app.route('/api/kids/<int:id>')
def get_kid(id):
    return json.dumps(db_interactions.get_kid(id))

@app.route('/api/kids/<int:id>', methods=['PUT'])
def update_kid(id):
    if not db_interactions.get_kid(id):
        return 'False input'
    user_data = json.loads(request.data)
    return json.dumps(db_interactions.update_item('kids', user_data))


@app.route('/api/kids/<int:id>', methods=['DELETE'])
def delete_kid(id):
    if not db_interactions.get_kid(id):
        return 'False input'
    return db_interactions.delete_kid(id)


@app.route('/api/kids', methods=['POST'])
def create_kid():
    user_data = json.loads(request.data)
    print(user_data)
    return json.dumps(db_interactions.create_kid(user_data))

@app.route('/api/logs', methods=['POST'])
def create_kid():
    user_data = json.loads(request.data)
    print(user_data)
    return json.dumps(db_interactions.create_kid(user_data))

if __name__ == '__main__':
    app.debug = True
    app.run()
