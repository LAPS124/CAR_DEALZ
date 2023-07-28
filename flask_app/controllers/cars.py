from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models.car import Car
from flask_app.models.user import User

#dashboard 
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        user_data={
            "id":id
        }
        theUser = User.getOne(data)
        car= Car.get_all()
        customer = Car.get_owner(user_data)
        return render_template('dashboard.html', user=theUser, cars=car, owners=customer)

    # return render_template("dashboard.html")

#new
@app.route('/new/car/')
def new_car():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            "id":session['user_id']
        }
    return render_template('new_car.html', user=User.getOne(data))
#create
@app.route('/create/car/', methods= ['POST'])
def create_car():
    if 'user_id' not in session:
        return redirect ('/logout')
    if not Car.validate_car(request.form):
        return redirect ('/new/car')
    data = {
        "price":request.form["price"],
        "model":request.form["model"],
        "make":request.form["make"],
        "year":request.form['year'],
        "description":request.form["description"],
        "user_id":session["user_id"]
    }
    Car.save(data)
    print(Car)
    return redirect('/dashboard')
#edit
@app.route('/edit/car/<int:id>')
def edit_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id" :session['user_id']
    }
    return render_template("edit.html", edit=Car.get_one(data), user=User.getOne(user_data))
#update
@app.route('/update/car', methods=["POST"])
def update_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_car(request.form):
        return redirect('/new/car/')
    data = {
        "price":request.form['price'],
        "model":request.form["model"],
        "make":request.form["make"],
        "year":request.form["year"],
        "description":request.form["description"],
        "id":request.form["id"],
        "user_id":session["user_id"]
        }
    Car.update(data)
    return redirect('/dashboard')
#view
@app.route('/view/<int:id>')
def view_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id": session['user_id']
    }
    customer = Car.get_owner(data)
    return render_template('view.html', car=Car.get_one(data), user=User.getOne(user_data), owners=customer)
#destroy
@app.route('/destroy/<int:id>')
def destroy_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Car.delete(data)
    print(data)
    return redirect('/dashboard')

