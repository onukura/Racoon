from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from racoon.extensions import db


# モデルに関する設定
class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    group_id = db.Column(db.Integer, nullable=True, default=0)

    # モデルからインスタンスを生成するときに使います。(利便性を高めるため)
    # passwordの暗号化も自動で行うことができるので、安全性も高めることができます。
    @classmethod
    def from_args(cls, name: str, email: str, password: str):
        instance = cls()
        instance.name = name
        instance.email = email
        if password is not None:
            # passwordがあれば暗号化します。
            instance.hash_password(password)
        return instance

    # 暗号化するためのメソッド。
    def hash_password(self, clean_password):
        self.password = generate_password_hash(str(clean_password), method="sha256")

    # 登録したpasswordとユーザーがログインフォームで入力したパスワードが正しいかどうかのチェックを行うメソッド
    def check_password(self, clean_password):
        return check_password_hash(self.password, clean_password)


class Group(db.Model):
    __tablename__ = "group"
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String, nullable=False)
