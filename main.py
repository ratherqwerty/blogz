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

#@app.route("/signup", methods=["POST"])
#def validate():
   
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'list_blogs', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog', methods=['POST','GET'])
def list_bloggers_blogs():
    guys_blogs = Blog.query.get('owner_id')
    return render_template('blog.html', title="This Person's Blog", id=guys_blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def posting():    
    if request.method == 'POST':
       newpost_title = request.form['title']
       newpost_post = request.form["body"]
       owner = request.args.get('id')

       newblog = Blog(newpost_title, newpost_post, owner)
       db.session.add(newblog)
       db.session.commit()

       #return redirect('/blog')
            
       return render_template('newpost.html', title="Your New Post!")

    if request.method == 'GET':
        return render_template('newpost.html', title="Your New Post!")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password is incorrect, or user does not exist', 'error')
            
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
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
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()

                session['username'] = username

                return redirect('/')
            else:
                flash('User already exists', 'error')
                return redirect('/login')

    return render_template('signup.html')

@app.route('/', methods=['POST', 'GET'])
#def list_blogs():
    #if request.args:
     #   blogger = request.args.get('id')
     #   ind_blogger = Blog.query.get(blogger)
      
      #  return render_template('allblogs.html',title="Blogger Page", blogs=ind_blogger)
   # else:
def index():   

   # if request.args:
      #  blog_id = request.args.get('id')
     #   ind_blog = Blog.query.get(blog_id)
     #   get_username = User.query.get('username')
     #   return render_template('allblogs.html',title="Build a Blog!", blog=ind_blog, users=get_username)
    #else:
    if request.method=='GET':
        blogger_page = request.args.get('id')
        #return redirect('/blog')
        return render_template('index.html', title="Someone's Blogs!", id=blogger_page)

    else:
        all_blogs = User.query.all()
        return render_template('index.html', title="blog users!", users=all_blogs)
  
    
if __name__ == '__main__':
    app.run()