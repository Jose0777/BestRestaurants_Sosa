from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

restaurants_url = "https://recruiting-datasets.s3.us-east-2.amazonaws.com/data_melp.json"

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ.get("APP_CONFIG_SECRET_KEY")
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6bb'
Bootstrap(app)


class FindRestaurantForm(FlaskForm):
    name = StringField("Where? (Enter a State):", validators=[DataRequired()], render_kw={"placeholder": "Name of the State (i.e. Colima):"})
    submit = SubmitField("Find Restaurant")


@app.route('/', methods=["GET", "POST"])
def home():
    form = FindRestaurantForm()
    if form.validate_on_submit():
        # Looking restaurants by state
        restaurant_byState = form.name.data.title()
        response = requests.get(url=restaurants_url)
        data = response.json()
        options = []
        for restaurant in data:
            if restaurant['address']['state'] == restaurant_byState:
                options.append(restaurant)
        if not options:
            flash("We couldn't find a restaurant in that State")
            return render_template("index.html", form=form, options=options)
        # Sorting restaurants by name
        new_data = []
        for i in options:
            new_data.append(i['name'])
        new_data.sort(reverse=False)
        print(new_data)
        new_list = []
        for restaurantInState in new_data:
            for j in data:
                if j['name'] == restaurantInState:
                    new_list.append(j)
                    break
        return render_template("select.html", options=new_list)

    return render_template("index.html", form=form)


@app.route('/select', methods=["GET", "POST"])
def track_restaurant():
    if request.method == "POST":
        # Find id of the chosen restaurant
        form = request.form
        chosen_id = form['my_id']
        chosen_id = chosen_id[:-1]
        # Get data of restaurants
        data_restaurants = requests.get(url=restaurants_url).json()
        # Get results of the chosen restaurant
        for restaurant in data_restaurants:
            if restaurant['id'] == chosen_id:
                selected_restaurant = restaurant
                break
        return render_template("find.html", restaurant=selected_restaurant)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
