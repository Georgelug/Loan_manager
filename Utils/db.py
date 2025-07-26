from imports import *

class DB:
    database_url: str
    session_db: sessionmaker


    def __init__(self) -> None:
        with open("../config/db_cfg.json") as f:
            config = json.load(f)["database"]
        
        dialect = config["dialect"]
        driver = config["driver"]
        user = config["user"]
        password = config["password"]
        host = config["host"]
        port = config["port"]
        name = config["name"]

        self.database_url = f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{name}"

        self.session_db = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=create_engine(self.database_url)
        )
    
    







