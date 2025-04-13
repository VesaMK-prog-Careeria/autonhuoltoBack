class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://@DESKTOP-L26Q33J\\SQLEXPRESS/autonhuolto"
        "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False