class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://adminAutonhuolto:Autonhuolto10%25@srvautonhuolto.database.windows.net:1433/autonhuolto?driver=ODBC+Driver+17+for+SQL+Server&encrypt=yes&trustservercertificate=no"
        # "mssql+pyodbc://@DESKTOP-L26Q33J\\SQLEXPRESS/autonhuolto"
        # "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False