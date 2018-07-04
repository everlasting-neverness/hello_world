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
    return db_interactions.delete_item('kids', id)


@app.route('/api/kids', methods=['POST'])
def create_kid():
    user_data = json.loads(request.data)
    print(user_data)
    return json.dumps(db_interactions.create_item(user_data))

@app.route('/api/logs')
def get_logs():
    logs = json.dumps(db_interactions.get_logs())
    return logs

@app.route('/api/logs', methods=['POST'])
def create_log_entry():
    user_data = json.loads(request.data)
    return json.dumps(db_interactions.create_log_entry(user_data))

@app.route('/api/logs/<int:id>')
def get_log(id):
    log = json.dumps(db_interactions.get_log(id))
    return log

@app.route('/api/logs/<int:id>', methods=['PUT'])
def update_log(id):
    if not db_interactions.get_log(id):
        return {'False input': 'False input'}
    user_data = json.loads(request.data)
    return json.dumps(db_interactions.update_log(user_data, id))


@app.route('/api/logs/<int:id>', methods=['DELETE'])
def delete_log(id):
    if not db_interactions.get_log(id):
        return 'False input'
    return db_interactions.delete_item('logs', id)


if __name__ == '__main__':
    app.debug = True
    app.run()
