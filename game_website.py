from flask import Flask

app = Flask(__name__)


@app.route("/")
def menu():
    return items()


@app.route("/user/<name>/")
def intro(name):
    return "hey there %s" % name


def items():
    print("hi")
    print("does")
    print("this work???")
    return "dumpster fire\nbut if i can do this \nit might be ok?"
