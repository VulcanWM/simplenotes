from flask import Flask, render_template, request, redirect
import os
from functions import get_notes, add_note, delete_note

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

@app.route('/')
def index():
  if request.headers['X-Replit-User-Id']:
    return redirect("/dashboard")
  else:
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    print(request.headers)
    user_id = request.headers['X-Replit-User-Id']
    user_name=request.headers['X-Replit-User-Name']
    if user_id:
      msg = request.args.get("msg", False)
      return render_template(
        'dashboard.html',
        user_id=user_id,
        user_name=user_name,
        notes=get_notes(user_id),
        text=msg
      )
    else:
      return redirect("/login")
      
@app.route("/login")
def login():
  if request.headers['X-Replit-User-Id']:
    return redirect("/dashboard")
  else:
    return render_template("login.html")

@app.route("/addnote", methods=['POST', 'GET'])
def add_note_page():
  if request.method == 'POST':
    user_id = request.headers['X-Replit-User-Id']
    if user_id:
      desc = request.form['desc']
      func = add_note(user_id, desc)
      if func == True:
        return redirect("/dashboard")
      else:
        return redirect(f"/dashboard?msg={func}")
    else:
      return redirect("/login")
  else:
    return redirect("/login")

@app.route("/delete/<noteid>")
def delete_note_page(noteid):
  user_id = request.headers['X-Replit-User-Id']
  if user_id:
    func = delete_note(user_id, noteid)
    if func == True:
      return redirect("/dashboard")
    else:
      return redirect(f"/dashboard?msg={func}")
  else:
    return redirect("/login")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
