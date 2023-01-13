from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'mysecretkey'


todos = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, bread, eggs",
        "status": "incomplete"
    },
    {
        "id": 2,
        "title": "Learn Python",
        "description": "Learn the basics of Python programming",
        "status": "incomplete"
    },
    {
        "id": 3,
        "title": "Write a book",
        "description": "Write a novel about a young wizard",
        "status": "incomplete"
    },
]


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if valid_user(username, password):
            session["username"] = username
            flash("Successfully logged in!")
            return redirect("/")
        else:
            flash("Invalid username or password!")
            return redirect("/login")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Successfully logged out!")
    return redirect("/")


def valid_user(username, password):
    if username == "user1" and password == "user1":
        return True
    return False


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "username" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect("/login")
    return wrap


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", todos=todos)


@app.route('/add_todo')
def add_todo():
    return render_template("create_todo.html")


@app.route('/edit_todo/<todo_id>')
def edit_todo(todo_id):
    todo = next((todo for todo in todos if todo["id"] == int(todo_id)), None)
    return render_template("edit_todo.html", todo=todo)


@app.route('/delete_todo/<todo_id>')
def delete_todo(todo_id):
    todo = next((todo for todo in todos if todo["id"] == int(todo_id)), None)
    if todo:
        todos.remove(todo)
        flash("Todo deleted successfully!")
    else:
        flash("Todo not found!")
    return redirect(url_for("index"))


@app.route('/handle_todos', methods=['POST'])
def handle_todos():
    todo_id = request.form.get('todo_id')
    todo = next((todo for todo in todos if todo["id"] == int(todo_id)), None)
    if todo:
        todos.remove(todo)
        flash("Todo deleted successfully!")
    else:
        flash("Todo not found!")
    return redirect(url_for("index"))


@app.route('/handle_todo/<int:todo_id>', methods=["POST"])
def handle_todo(todo_id):
    title = request.form["title"]
    description = request.form["description"]
    # validate form data
    if not title or not description:
        flash("Title and description are required!")
        return redirect("/edit_todo/{}".format(todo_id))
    # update todo
    for i in range(len(todos)):
        if todos[i]["id"] == todo_id:
            todos[i]["title"] = title
            todos[i]["description"] = description
            flash("Todo updated!")
            return redirect("/")
    flash("Todo not found!")
    return redirect("/")


@app.route('/handle_form', methods=['POST'])
def handle_form():
    title = request.form.get("title")
    description = request.form.get("description")
    todo_id = request.form.get("todo_id")
    if todo_id:
        todo = next(
            (todo for todo in todos if todo["id"] == int(todo_id)), None)
        if todo:
            todo["title"] = title
            todo["description"] = description
            flash("Todo updated successfully!")
        else:
            flash("Todo not found!")
    else:
        new_id = max([todo["id"] for todo in todos]) + 1 if todos else 1
        todos.append({
            "id": new_id,
            "title": title,
            "description": description,
            "status": "incomplete"
        })
        flash("Todo created successfully!")
    return redirect(url_for("index"))


@app.route('/handle_create_form', methods=["POST"])
def handle_create_form():
    title = request.form["title"]
    description = request.form["description"]
    # validate form data
    if not title or not description:
        flash("Title and description are required!")
        return redirect("/create_todo")
    # create todo
    todo = {"id": len(todos)+1, "title": title, "description": description}
    todos.append(todo)
    flash("Todo created!")
    return redirect("/")


@app.route('/create_todo', methods=['GET', 'POST'])
def create_todo():
    if request.method == 'POST':
        title = request.form["title"]
        description = request.form["description"]
        if not title or not description:
            flash("Title and description are required!")
            return redirect("/create_todo")
        todo = {"id": len(todos) + 1, "title": title,
                "description": description}
        todos.append(todo)
        flash("Todo created!")
        return redirect("/")
    return render_template("create_todo.html")


if __name__ == '__main__':
    app.run(debug=True)
