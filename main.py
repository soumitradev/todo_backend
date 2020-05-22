import flask
import json
import random
import string

app = flask.Flask(__name__)
app.config["DEBUG"] = True

InvalidID = {
  "error": {
    "status": 400,
    "message": "Bad Request: invalid id"
  }
}

EmptyText = {
  "error": {
    "status": 400,
    "message": "Bad Request: empty request"
  }
}

@app.route('/', methods=['GET'])
def home():
    return "<h1>ToDo++</h1><p>This site is a prototype API for an ToDo app.</p>"

@app.route('/api/v1/todo/all', methods=['GET'])
def todo_all():
    with open("./todo.json", "r") as f:
        return f.read()

@app.route('/api/v1/todo', methods=['GET', 'POST'])
def todo_id():
    if flask.request.method == 'GET':
        with open("./todo.json", "r") as f:
            data = json.load(f)

        results = []

        id = flask.request.args.get('id')
        if id in get_taken_ids():
            return str(list(filter(lambda x: x['id'] == id, data)))
        else:
            return InvalidID, 400
        
    else:
        if flask.request.form['id']:
            with open("./todo.json", "r") as f:
                data = json.load(f)

            id = flask.request.form['id']
            if id in get_taken_ids():
                title = flask.request.form['title']
                text = flask.request.form['text']

                for i in data:
                    if i['id'] == id:
                        i['title'] = title
                        i['text'] = text
                        res = i
                        break

                with open("./todo.json", "w") as f:
                    json.dump(data, f)

                return json.dumps(res)
            else:
                return InvalidID, 400
        else:
            with open("./todo.json", "r") as f:
                data = json.load(f)

            id = get_random_alphaNumeric_string(11)
            while id in get_taken_ids():
                id = get_random_alphaNumeric_string(11)

            title = flask.request.form['title']
            text = flask.request.form['text']

            if title and text:
                res = {"id" : id, "title" : title, "text" : text}
                data.append(res)

                with open("./todo.json", "w") as f:
                    json.dump(data, f)

                return json.dumps(res)
            else:
                return EmptyText, 400

@app.route('/api/v1/delete', methods=['POST'])
def delete_id():
    with open("./todo.json", "r") as f:
        data = json.load(f)

    id = flask.request.form['id']

    removed_note = ""
    for i in data:
        if i['id'] == id:
            removed_note = i
            break
    
    if removed_note:
        data.remove(removed_note)
    else:
        return InvalidID, 400

    with open("./todo.json", "w") as f:
        json.dump(data, f)

    return json.dumps(removed_note)

def get_taken_ids():
    with open("./todo.json", "r") as f:
        data = json.load(f)

    return map(lambda x: x['id'], data)

def get_random_alphaNumeric_string(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template("404.html"), 404

app.run()