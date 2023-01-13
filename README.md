# Todo App

A simple Todo app built using Flask, a web framework for Python.

## Features
- Users can login and logout
- Users can view their Todos
- Users can create new Todos
- Users can edit and delete existing Todos

## Installation

1. Clone the repository
```shell
git clone https://github.com/<your-username>/todo-app.git
```

2. Create a virtual environment and activate it
```shell
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies
```shell
pip install -r requirements.txt
```
4. Run the app
```shell
export FLASK_APP=app.py
flask run
```

## Usage
1. Open a web browser and go to `http://localhost:5000`
2. Click on the Login button, enter the username and password
3. You will be redirected to the index page where you can see your Todos
4. You can add new Todos, edit or delete existing ones
5. You can logout by clicking on the Logout button

## Configuration
You can configure the app by editing the `config.py` file.

## License
This project is licensed under the MIT License.

## Author
The author of this project is Jonathan

## Note
This code is only an example, and should not be used in production, it has security vulnerabilities and is not suitable for production use.
