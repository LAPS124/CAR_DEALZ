from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

db = 'cars1'


class Car:

    db = 'cars1'

    def __init__ (self,db_data):
        self.id= db_data['id']
        self.price= db_data['price']
        self.model= db_data['model']
        self.make= db_data['make']
        self.year= db_data['year']
        self.description= db_data['description']
        self.created_at= db_data['created_at']
        self.updated_at= db_data['updated_at']
        self.user_id= db_data['user_id']
        self.owners=[]

    @classmethod
    def save(cls,data):
        query = "INSERT INTO cars (price, model, make, year, description, user_id) Values (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM cars;'
        results = connectToMySQL(cls.db).query_db(query)
        cars = []
        for row in results:
            cars.append(cls(row))
        return cars

    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM cars  WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update(cls,data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s,  updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query= "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_owner(cls,data):
        query = """SELECT * FROM user JOIN cars on user.id
                = cars.user_id ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        owners = []
        for owner in results:
            car_owner = cls(owner)
            owner_data = {
                "id" : owner['id'],
                "first_name": owner['first_name'],
                "last_name" : owner['last_name'],
                "email" : owner['email'],
                "password": owner['password'],
                "created_at": owner['created_at'],
                "updated_at": owner['updated_at']
            }
            car_owner.customer = User(owner_data)
            owners.append(car_owner)
            print('owner_data')
        return owners

    @staticmethod
    def validate_car(car):
        is_valid=True
        if len(car['price']) == 0:
            is_valid = False
            flash("price must be more than 0", "car")
        if len(car['model']) < 3:
            is_valid = False
            flash("model must be at least 3 characters", "car")
        if len(car['make']) < 3:
            is_valid = False
            flash("make must be at least 3 characters", "car")
        if len(car['year']) == 0 :
            is_valid = False
            flash("Cars were not sold in production than, 0", "car")
        if len(car['description']) < 3:
            is_valid = False
            flash("description must be at least 3 characters", "car")
        return is_valid