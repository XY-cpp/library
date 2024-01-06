import toml
import library

config = toml.load("config.toml")

library.init_db(
    host=config["db"]["host"],
    port=config["db"]["port"],
    username=config["db"]["username"],
    password=config["db"]["password"],
    database=config["db"]["database"],
)

if __name__ == "__main__":
    library.app.run(
        host="0.0.0.0",
        port="9003",
        debug=True
    )
