from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///aksh.db"
db = SQLAlchemy()
db.init_app(app)

# CREATING MODEL
# Subclass db.Model to define a model class.
# The db object makes the names in sqlalchemy and sqlalchemy.orm available for convenience,
# such as db.Column. The model will generate a table name by converting the CamelCase class name to snake_case.


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    # yaha pe dt.utcnow() me error tha kyunki utcnow() datetime(1) ke andar module datetime(2) ke andar hai not in datetime(1)
    date = db.Column(db.DateTime, default=dt.datetime.utcnow())


# Repr shows what do you want to display from task
#  repr method represents how one object of this datatable
    # will look like
def __repr__(self):
    return f'{self.id} + {self.title}'

#READ
@app.route('/')
def hello_world():
    # if(request.method=='POST'):

    allTask = Task.query.all()
    # for x in allTask:
    #    print(x.title)
    return render_template("index.html", allTasks=allTask)
    

# CREATE
@app.route('/add_task')
def add_task():
    return render_template("form.html")

@app.route('/add', methods=['POST'])
def home_f():
    title = request.form.get('title')
    description = request.form.get('description')
    if (title != '' and description != ''):
        task = Task(title=title, desc=description)
        db.session.add(task)
        db.session.commit()

    else:
        flash("Please fill out both fields")

    return redirect('/')

# DELETE
@app.route('/delete/<int:id>')
def erase(id):

    # deletes the data on the basis of unique id and
    # directs to home page
    data = Task.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

#UPDATE
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
   data=Task.query.get(id)
   if request.method == "POST":
       title=request.form.get('title')
       description=request.form.get('description')
       data.title=title
       data.desc=description
       db.session.add(data)
       db.session.commit()
       return redirect('/')
#    print(data.title)
   return render_template("update.html",task=data)
#    return redirect('/')


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    # yaha pe jo port likha wo apne mann se likha hai,by default it is 5000
    app.run(debug=True, port=8000)
