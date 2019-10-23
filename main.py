from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:practice@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'blahblahblah'

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.String(1000))
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

def not_valid(field):
    if len(field) < 3 or len(field) > 20 or field.find(" ") != -1:
        return True
    else:
        return False

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'list_blogs', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def list_blogs():
    if request.args:        

        blog_id = request.args.get('id')
        blogger_id = request.args.get('user')    

        if blogger_id:
            ind_blogger = Blog.query.filter_by(owner_id=blogger_id)

            return render_template('singleUser.html', title="This Blogger's Page", blogs=ind_blogger)
        
        else:
            ind_blog = Blog.query.filter_by(id=blog_id)

            return render_template('blog.html', title="Specific Post", blogs=ind_blog)       

    else:
        all_blogs = Blog.query.all()
        return render_template('allblogs.html', title="All the Blogs!", blogs=all_blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def posting():    
    if request.method == 'POST':
       newpost_title = request.form['title']
       newpost_post = request.form["body"]
       username = session['username']
       
       owner = User.query.filter_by(username=username).first()

       newblog = Blog(newpost_title, newpost_post, owner)
       db.session.add(newblog)
       db.session.commit()
               
       return redirect('/blog')

    if request.method == 'GET':
        return render_template('newpost.html', title="Your New Post!")

@app.route('/login', methods=['POST', 'GET'])#WORKS! DONT TOUCH!
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        elif user and user.password != password:
            flash('Incorrect password', 'error')
        else:
            flash('Username does not exist', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])#WORKS! DONT TOUCH!
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        username_error = ""
        password_error = ""
        email_error = ""

        if not_valid(username):
            username_error = "That is not a valid username"
    
        if not_valid(password) or not_valid(verify):
            password_error = "That is not a valid password"
            password = ""
            verify = ""
        elif password != verify:
            password_error = "Passwords must match"
            password1 = ""
            verify = ""
    
        if len(username_error) >=1 or len(password_error) >= 1:
            return render_template("signup.html", username_error=username_error, password_error=password_error, username=username)
        else:
            pass

            existing_user = User.query.filter_by(username=username).first()
            existing_user_pw = User.query.filter_by(password=password).first()

            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()

                session['username'] = username

                return redirect('/newpost')
            elif existing_user and not existing_user_pw:
                flash('Username already exists', 'error')
            else:
                flash('User already exists', 'error')
                return redirect('/login')

    return render_template('signup.html')

@app.route('/', methods=['POST', 'GET'])
def index():   
    all_blogs = User.query.all()
    return render_template('index.html', title="blog users!", users=all_blogs)
  
    
if __name__ == '__main__':
    app.run()