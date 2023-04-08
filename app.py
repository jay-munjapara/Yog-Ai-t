from flask import Flask, render_template, url_for, request, session, redirect, flash,Response
import cv2
import mediapipe as mp
import numpy as np
import time
from flask_pymongo import PyMongo
import bcrypt
import pymongo
from datetime import datetime
from datetime import date
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mongodb'
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['yogait']

@app.route("/")
@app.route("/main")
def main():
    return render_template('signin.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        collection = db['users']
        signup_user = collection.find_one({'username': request.form['username']})

        if signup_user:
            flash(request.form['username'] + ' username is already exist')
            return redirect(url_for('signup'))

        hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        collection.insert_one({'username': request.form['username'], 
                               'password': hashed,
                               'email': request.form['email'], 
                               'gender': request.form['gender'],
                               'height': request.form['height'],
                               'weight': request.form['weight'],
                               'birthdate': request.form['birthdate']                               
                               })
        return redirect(url_for('signin'))

    return render_template('signup.html')

@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])

    return render_template('signin.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        collection = db['users']
        signin_user = collection.find_one({'username': request.form['username']})

        if signin_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), signin_user['password']) == \
                    signin_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))

        flash('Username and password combination is wrong')
        return render_template('signin.html')

    return render_template('signin.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
    app.run()
