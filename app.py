from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import *
from database import *
from settings import *

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
s = db.session
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

def get_entries(folder,prefix):
    prefix += '-'
    folder.prefix = prefix
    folder.type = 'folder'
    entries = [folder]
    for child_folder in folder.child_folders:
        entries += get_entries(child_folder,prefix)
    for child_bookmark in folder.child_bookmarks:
        child_bookmark.prefix = prefix + '-'
        child_bookmark.type = 'bookmark'
        entries.append(child_bookmark)
    return entries

def set_choices(form_folder,form_bookmark,update_folder,update_bookmark):
    user = s.query(Users).filter(Users.name == session['username']).one()    
    entries = get_entries(user.folder[0],'')
    choices = []
    for entry in entries:
        if entry.type == 'folder':
            choices.append((str(entry.id),entry.prefix + entry.name))
    form_folder.folder_parent_folder.choices = choices
    update_folder.folder_parent_folder_update.choices = choices
    form_bookmark.bookmark_parent_folder.choices = choices
    update_bookmark.bookmark_parent_folder_update.choices = choices

@app.route('/')
def index(text=''):   
    if current_user.is_authenticated:
        return bookmarks()
    return render_template("index.html",text=text)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return bookmarks()
    else:
        form = RegisterForm()
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            if s.query(Users).filter(Users.name == username).count() == 0:                        
                user = Users(username,hashed_password)            
                user_folder = Folders(username,user)
                s.add(user)
                s.add(user_folder)
                s.commit()
                return index("Signed up!")            
            return render_template("signup.html", text="Username already in use.", form=form)
        return render_template("signup.html", form=form)
    
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return bookmarks()
    else:
        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            if s.query(Users).filter(Users.name == username).count() == 0:
                return index("User doesn't exist.")
            user = s.query(Users).filter(Users.name == username).one()
            if user.name == username and check_password_hash(user.password, password):
                login_user(user,remember=form.remember.data)            
                session['username'] = user.name                     
                return bookmarks()
            else:
                return render_template("login.html", text="Wrong password!", form=form)
        return render_template("login.html", form=form)

@app.route('/bookmarks')
@login_required
def bookmarks(text='',entries=[]):
    form_folder = AddFolderForm()
    form_bookmark = AddBookmarkForm()
    update_folder = UpdateFolderForm()
    update_bookmark = UpdateBookmarkForm()
    delete_folder = DeleteFolderForm()
    delete_bookmark = DeleteBookmarkForm()
    search = SearchForm()
    set_choices(form_folder,form_bookmark,update_folder,update_bookmark)
    user = s.query(Users).filter(Users.name == session['username']).one()
    user_folder = user.folder[0]
    if len(entries) == 0:
        entries = get_entries(user_folder,'') 
    return render_template("bookmarks.html",name=session['username'],
                            text=text,
                            form_folder=form_folder,
                            form_bookmark=form_bookmark,
                            delete_folder=delete_folder,
                            delete_bookmark=delete_bookmark,
                            update_folder=update_folder,
                            update_bookmark=update_bookmark,
                            search=search,
                            entries=entries
                          )

@app.route('/add_folder', methods=['GET','POST'])
@login_required
def add_folder():
    form_folder = AddFolderForm()     
    form_bookmark = AddBookmarkForm()
    update_folder = UpdateFolderForm()     
    update_bookmark = UpdateBookmarkForm()
    set_choices(form_folder,form_bookmark,update_folder,update_bookmark)
    user = s.query(Users).filter(Users.name == session['username']).one()
    if request.method == 'POST' and form_folder.validate_on_submit():
        name = form_folder.folder_name.data
        parent_folder = s.query(Folders).filter(Folders.id == 
                                                  form_folder.folder_parent_folder.data).one()
        if s.query(Folders).filter(Folders.name == name, 
                                     Folders.parent_folder == parent_folder).count() == 0:
            user = s.query(Users).filter(Users.name == session['username']).one()            
            folder = Folders(name,user,parent_folder)
            s.add(folder)
            s.commit()
            return bookmarks(' Added folder')
        else:
            return bookmarks(' Folder already exists')
    return bookmarks()

@app.route('/add_bookmark', methods=['GET','POST'])
@login_required
def add_bookmark():
    form_folder = AddFolderForm()     
    form_bookmark = AddBookmarkForm()     
    update_folder = UpdateFolderForm()     
    update_bookmark = UpdateBookmarkForm()
    set_choices(form_folder,form_bookmark,update_folder,update_bookmark)    
    if request.method == 'POST' and form_bookmark.validate_on_submit():
        name = form_bookmark.bookmark_name.data
        parent_folder = s.query(Folders).filter(Folders.id == 
                                                  form_bookmark.bookmark_parent_folder.data).one()
        link = form_bookmark.link.data
        description = form_bookmark.description.data

        if s.query(Bookmarks).filter(Bookmarks.name == name, 
                                              Bookmarks.parent_folder == parent_folder, 
                                              Bookmarks.link == link).count() == 0:
            bookmark = Bookmarks(name,link,description,parent_folder)
            s.add(bookmark)
            s.commit()
            return bookmarks(' Added bookmark')
        else:
            return bookmarks(' Bookmark already exists')
    return bookmarks()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return index("Logged out.")   

@app.route('/remove_folder', methods=['POST'])
@login_required
def remove_folder():
    form_folder = AddFolderForm()     
    form_bookmark = AddBookmarkForm()     
    update_folder = UpdateFolderForm()     
    update_bookmark = UpdateBookmarkForm()
    delete_folder = DeleteFolderForm()
    folder_id = delete_folder.folder_id.data
    folder = s.query(Folders).filter(Folders.id == folder_id).one()
    s.delete(folder)
    s.commit()
    set_choices(form_folder,form_bookmark,update_folder,update_bookmark)
    return bookmarks(' Folder deleted')

@app.route('/remove_bookmark', methods=['POST'])
@login_required
def remove_bookmark():
    delete_bookmark = DeleteBookmarkForm()
    bookmark_id = delete_bookmark.bookmark_id.data
    bookmark = s.query(Bookmarks).filter(Bookmarks.id == bookmark_id).one()
    s.delete(bookmark)
    s.commit()
    return bookmarks(' Bookmark deleted')

@app.route('/update_folder', methods=['POST'])
@login_required
def update_folder():
    form_folder = AddFolderForm()     
    form_bookmark = AddBookmarkForm()     
    update_folder = UpdateFolderForm()     
    update_bookmark = UpdateBookmarkForm()
    set_choices(form_folder,form_bookmark,update_folder,update_bookmark)
    folder = s.query(Folders).filter(Folders.id == update_folder.folder_id_update.data).one()
    parent_folder = s.query(Folders).filter(Folders.id == 
                                            update_folder.folder_parent_folder_update.data).one()
    if folder == parent_folder:
        return bookmarks(' Folder cannot contain itself')                                            
    folder.name = update_folder.folder_name_update.data
    folder.parent_folder = parent_folder    
    if s.query(Folders).filter(Folders.name == folder.name, 
                                     Folders.parent_folder == parent_folder).count() == 1:
        s.commit()
        return bookmarks(' Updated folder')
    else:
        s.rollback()
        return bookmarks(' Folder already exists')
    return bookmarks()

@app.route('/update_bookmark', methods=['POST'])
@login_required
def update_bookmark():    
    update_bookmark = UpdateBookmarkForm()
    bookmark = s.query(Bookmarks).filter(Bookmarks.id ==
                                         update_bookmark.bookmark_id_update.data).one()
    parent_folder = s.query(Folders).filter(Folders.id ==
                                           update_bookmark.bookmark_parent_folder_update.data).one()
    bookmark.name = update_bookmark.bookmark_name_update.data
    bookmark.parent_folder = parent_folder
    bookmark.link = update_bookmark.link_update.data
    bookmark.description = update_bookmark.description_update.data
    if s.query(Bookmarks).filter(Bookmarks.name == bookmark.name,   
                                 Bookmarks.parent_folder == parent_folder).count() == 1:
        s.commit()
        return bookmarks(' updated bookmark')
    else:
        s.rollback()
        return bookmarks(' Bookmark already exists')                                           
    return bookmarks()

@app.route('/search', methods=['POST'])
@login_required
def search():
    search = SearchForm()
    search_term = search.search_term.data
    user = s.query(Users).filter(Users.name == session['username']).one()
    user_folder = user.folder[0]
    entries = get_entries(user_folder,'')
    results = []
    for entry in entries:
        if entry.type == 'bookmark':
            if search_term in entry.name or search_term in entry.description:
                results.append(entry)
    if len(results) == 0:
        text = 'No results'
    else:
        text = 'Search results:'
    return bookmarks(text=text,entries=results)

if __name__ == '__main__':
    app.debug = True
    app.run()