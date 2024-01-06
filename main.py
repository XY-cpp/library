import toml
from library import app

config = toml.load("config.toml")

app.config["host"]=config["db"]["host"]
app.config["port"]=config["db"]["port"]
app.config["username"]=config["db"]["username"]
app.config["password"]=config["db"]["password"]
app.config["database"]=config["db"]["database"]

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port="9003",
        debug=True
    )
