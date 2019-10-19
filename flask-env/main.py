from flask import Flask, request
from caesar import rotate_string

app = Flask(__name__)
app.config['DEBUG'] = True

form ="""       
<!DOCTYPE html>

<html>

    <head>
    
        
        <style>
            form {{
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
            }}
            textarea {{
                margin: 10px 0;
                width: 540px;
                height: 120px;
            }}
        </style>
    </head>
    <body>
      <form method="POST">
        <div>
        <label for="rot">Rotate by:</label>
        <input type="text" name="rot" id="rot" value="0">
        </div>
        <textarea name="text" placeholder="0"> 

      </form>
      <form>
        <input type="submit" value="Submit Query">
      </form>
    </body>
</html>
"""
        

@app.route("/")
def index():
    return form.format("")

@app.route("/")
def encrypt():
    encrypt = int(request.form['rot'])

    text = request.form['text']

    caesar = rotate_string(text, encrypt)

    return form.format(caesar)

app.run()