import os
import json
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
DATABASE = "irish_recipes"

mongo = PyMongo(app)


# function for home page
@app.route('/')
@app.route("/get_recipes")
def base2():
    return render_template("base2.html")


# function to go to add.html
@app.route('/add')
def add():
    return render_template("add.html", food_type=mongo.db.food_type.find())


# function to inserts the recipes from mongo db
@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for("recipes"))


# function to go to recipes.html
@app.route('/recipes')
def recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())


# function to create the top.html page with the data from restaurants.json
@app.route('/top')
def top():
    data = []
    with open("data/restaurants.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("top.html", restaurants=data)


# function to edit recipes and add them to the mongo db
@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_food_type = mongo.db.food_type.find()
    return render_template("edit-recipe.html", recipe=the_recipe, food_type=all_food_type)


# function to update the recipes
@app.route("/edit_recipe/<id>/update", methods=["POST"])
def update_recipe(id):
    print("Posting DB update")
    mongo.db.recipes.update_one({"_id": ObjectId(id)},
                                {"$set":
                                 {
                                     "food": request.form.get("food"),
                                     "dish_name": request.form.get("dish_name"),
                                     "ingredients": request.form.get("ingredients"),
                                     "cooking_method": request.form.get("cooking_method")
                                 }})
    return redirect(url_for("recipes"))


# function to delete recipes from the web application and mongodb
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    return redirect(url_for("recipes"))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
