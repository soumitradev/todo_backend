import flask
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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
        if id:
            return str(list(filter(lambda x: x['id'] == int(id), data)))
        else:
            return "Error: Bad Request"
        
        return json.dumps(results)
    else:
        with open("./todo.json", "r") as f:
            data = json.load(f)

        id = len(data)

        print(data)

        title = flask.request.form['title']
        text = flask.request.form['text']

        res = {"id" : id, "title" : title, "text" : text}
        data.append(res)

        with open("./todo.json", "w") as f:
            json.dump(data, f)

        return json.dumps(res)


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template("404.html"), 404

app.run()