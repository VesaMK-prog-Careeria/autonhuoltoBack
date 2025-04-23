import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "salainenavain123")

# class Config:
#     SQLALCHEMY_DATABASE_URI = (
#         "postgresql://autonhuolto_user:Q8iBgQXBXkfF2ZQT4JfQsjbMfwfef2xG@dpg-d03nf8ali9vc73frn3j0-a/autonhuolto"
#         # "mssql+pyodbc://@DESKTOP-L26Q33J\\SQLEXPRESS/autonhuolto"
#         # "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False