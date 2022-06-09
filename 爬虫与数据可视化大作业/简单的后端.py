from flask import Flask, render_template
from GetData类 import GetData

app = Flask(__name__)


def outer():
    obj = GetData()
    data = obj.handle_data()

    def inner():
        return data
    return inner


@app.route("/")
def index():
    out = outer()
    data = out().to_dict(orient="records")
    return render_template("index.html", data=data)  # 此时会自动找到template文件夹的index.html


@app.route("/home")
def home():
    out = outer()
    item = out()
    name = item["name"].to_list()
    value = item["value"].to_list()
    return render_template("home.html", name=name, value=value)  # 此时会自动找到template文件夹的index.html


@app.route("/排序")
def sort():
    out = outer()
    item = out()
    data = item.values.tolist()
    return render_template("排序.html", data=data)


if __name__ == '__main__':
    app.run(debug=False)
