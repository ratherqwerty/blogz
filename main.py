from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:practice@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['GET'])
def index():

    if request.args:
        blog_id = request.args.get('id')
        ind_blog = Blog.query.get(blog_id)
        return render_template('blog.html',title="Build a Blog!", blog=ind_blog)
    else:
        all_blogs = Blog.query.all()
        return render_template('allblogs.html', title="All the Blogs!", blogs=all_blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def posting():
    
    if request.method == 'POST':
       newpost_title = request.form['title']
       newpost_post = request.form["body"]

       newblog = Blog(newpost_title, newpost_post)
       db.session.add(newblog)
       db.session.commit()

       return redirect('/blog')
            
       return render_template('newpost.html', title="Your New Post!")

    if request.method == 'GET':
        return render_template('newpost.html', title="Your New Post!")
    #else:



if __name__ == '__main__':
    app.run()