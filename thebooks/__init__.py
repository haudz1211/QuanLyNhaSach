from cgitb import text

from cloudinary import uploader
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import cloudinary
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
app = Flask(__name__)
app.secret_key = '1@##JDO($E(_(*E)(ƯEd90sw8đUIDF*&F$rjWR@$2424DASDQW'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin%40123@localhost/thebooks?charset=utf8mb4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config["PAGE_SIZE"] = 12

cloudinary.config(cloud_name='dgeyq5bpg',
                  api_key='124191785282462',
                  api_secret='-FwQxZuQW-YziPfCZ3ktdIkqeug')

def upload_image_to_cloudinary(image_file):
    """
    Tải hình ảnh lên Cloudinary và trả về URL an toàn.
    :param image_file: Tệp hình ảnh
    :return: URL của hình ảnh đã tải lên hoặc None nếu có lỗi
    """
    try:
        # Tải lên hình ảnh và nhận kết quả
        upload_result = cloudinary.uploader.upload(image_file)
        return upload_result['secure_url']  # Trả về URL an toàn
    except Exception as e:
        print(f"Có lỗi xảy ra khi tải lên Cloudinary: {e}")
        return None


db = SQLAlchemy(app=app)
login_manager = LoginManager(app=app)

admin = Admin(app=app, name='Quản trị BOOKSTORE', template_mode='bootstrap4')
def create_database_if_not_exists():
    engine = create_engine('mysql+pymysql://root:Admin%40123@localhost/?charset=utf8mb4')
    with engine.connect() as connection:
        connection.execute(text("CREATE DATABASE IF NOT EXISTS thebooks"))
    print("Database 'thebooks' created or already exists.")

create_database_if_not_exists()
