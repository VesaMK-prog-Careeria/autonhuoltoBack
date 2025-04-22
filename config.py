import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# class Config:
#     SQLALCHEMY_DATABASE_URI = (
#         "postgresql://autonhuolto_user:Q8iBgQXBXkfF2ZQT4JfQsjbMfwfef2xG@dpg-d03nf8ali9vc73frn3j0-a/autonhuolto"
#         # "mssql+pyodbc://@DESKTOP-L26Q33J\\SQLEXPRESS/autonhuolto"
#         # "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False