from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import CollectionRecipes, Recipe, User, Collection
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def homePage():
    if request.method == 'POST': 
        recipe_name = request.form.get('recipe_name')#Gets the note from the HTML 
        rData = request.form.get('data')#Gets the note from the HTML 
        #favourites = request.form.get('favourites')#Gets the note from the HTML 
        
        favourites = request.form.get('favourites') == 'Favourites'

        if len(recipe_name) < 1:
            flash('recipe_name is too short!', category='error') 
        else:
            new_note = Recipe(recipe_name=recipe_name,data=rData,favourites=favourites, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/recipe', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        recipe_name = request.form.get('recipe_name')#Gets the note from the HTML 
        rData = request.form.get('data')#Gets the note from the HTML 
        #favourites = request.form.get('favourites')#Gets the note from the HTML 
        
        favourites = request.form.get('favourites') == 'Favourites'

        if len(recipe_name) < 1:
            flash('recipe_name is too short!', category='error') 
        else:
            new_note = Recipe(recipe_name=recipe_name,data=rData,favourites=favourites, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("recipe.html", user=current_user)


@views.route('/delete-recipe', methods=['POST'])
def delete_note():  
    recipe = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    recipeId = recipe['recipeId']
    note = Recipe.query.get(recipeId)
    if note:
        db.session.delete(note)
        db.session.commit()
        flash('Recipe deleted!', category='success')
    return render_template("recipe.html", user=current_user)



@views.route('/user', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        data = request.form
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    elif request.method == 'GET':
        users = User.query.all()
        return render_template('users.html', users=users)

@views.route('/user/<int:user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200



@views.route('/collection', methods=['GET', 'POST'])
def manage_collections():
    if request.method == 'POST':
        data = request.form
        collection_name = request.form.get('collection_name')
        new_collection = Collection(collection_name=collection_name,user_id=current_user.id)
        db.session.add(new_collection)
        db.session.commit()
        
        # Add selected recipes to CollectionRecipes
        if 'recipes' in data:
            for recipe_id in data.getlist('recipes'):
                collection_recipe = CollectionRecipes(collection_id=new_collection.id, recipe_id=recipe_id)
                db.session.add(collection_recipe)
            db.session.commit()
        collections = Collection.query.filter_by(user_id=current_user.id)
        return render_template('collections.html', collections=collections, recipes=Recipe.query.filter_by(user_id=current_user.id))
    elif request.method == 'GET':
        collections = Collection.query.filter_by(user_id=current_user.id)
        return render_template('collections.html', collections=collections, recipes=Recipe.query.filter_by(user_id=current_user.id))

@views.route('/collection/<int:collection_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_collection(collection_id):
    collection = Collection.query.get(collection_id)
    db.session.delete(collection)
    db.session.commit()
    collections = Collection.query.filter_by(user_id=current_user.id)
    return render_template('collections.html', collections=collections, recipes=Recipe.query.filter_by(user_id=current_user.id))