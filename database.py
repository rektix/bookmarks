from app import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True)
    password = db.Column(db.String)

    def __init__(self,name,password):
        self.name = name
        self.password = password

class Folders(db.Model):
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref = db.backref('folder',
                                                         uselist=True,cascade='delete,all'))
    parent_folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'))
    parent_folder = db.relationship("Folders", remote_side=[id], 
                                    backref = db.backref('child_folders',
                                                         uselist=True,cascade='delete,all',
                                                         order_by="Folders.id"))

    def __init__(self,name,user,folder = None):
        self.name = name
        self.user = user
        self.parent_folder = folder

class Bookmarks(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    link = db.Column(db.Text)
    description = db.Column(db.Text)    
    parent_folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'))
    parent_folder = db.relationship("Folders", 
                                    backref = db.backref('child_bookmarks',
                                                         uselist=True,cascade='delete,all',
                                                         order_by="Bookmarks.id"))

    def __init__(self,name,link,description,folder = None):
        self.name = name
        self.parent_folder = folder
        self.link = link
        self.description = description