from flask import Flask, request
from bs4 import BeautifulSoup
import requests
import json
import random

app = Flask(__name__)

def get_recipe_info(url):
    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, 'html.parser')

    title = soup.find(id="article-heading_2-0").text.strip()
    if soup.video:
        image = soup.video['poster']
    elif soup.find("img", class_="primary-image__image"):
        image = soup.find("img", class_="primary-image__image")['src']
    else:
        print("\033[91m" + "No image found" + "\033[0m")
        image = None
    # recipe_details includes items like prep time, cook time, servings, etc.
    recipe_details = soup.find_all(class_="mntl-recipe-details__label")
    parsed_recipe_details = {}
    for label in recipe_details:
        # label: "Prep time", "Cook time", "Servings", etc.
        # value: "10 minutes", "30 minutes", "4 servings", etc.
        value = label.find_next_sibling().text.strip()
        label = label.text.strip()
        # print(label, value)
        parsed_recipe_details[label] = value

    # check if ingredients are sectioned by headers.
    # if not, simply list them all
    parsed_ingredients = {}
    ingredient_headers = soup.find_all(
        "p", class_="mntl-structured-ingredients__list-heading")
    if(ingredient_headers):
        for header in ingredient_headers:
            formatted_header = header.text.strip().replace(":", "")
            parsed_ingredients[formatted_header] = []
            ul = header.find_next_sibling("ul")
            ingredients = ul.find_all("li")
            for item in ingredients:
                parsed_ingredients[formatted_header].append(item.text.strip())
    else:
        ingredient_ul = soup.find(
            "ul", class_="mntl-structured-ingredients__list")
        ingredients = ingredient_ul.find_all("li")
        parsed_ingredients["All"] = []
        for item in ingredients:
            parsed_ingredients["All"].append(item.text.strip())

    # directions will be sent as a list of strings (in order)
    directions = []
    direction_ol = soup.find(
        "ol", id="mntl-sc-block_2-0").findChildren("li", recursive=False)
    for li in direction_ol:
        directions.append(li.findChild("p").text.strip())

    nutrition_facts = soup.find_all(
        "tr", class_="mntl-nutrition-facts-summary__table-row")
    parsed_nutrition_facts = {}
    for value in nutrition_facts:
        label = value.td.find_next_sibling().text.strip()
        value = value.td.text.strip()
        # print(label, value)
        parsed_nutrition_facts[label] = value
    # print(parsed_nutrition_facts)

    return {
        "title": title,
        "image": image,
        "recipe_details": parsed_recipe_details,
        "ingredients": parsed_ingredients,
        "directions": directions,
        "nutrition_facts": parsed_nutrition_facts
    }


f = open("./src/recipes.json")
recipes = json.load(f)

# pseudo test cases just to see if the parser works
# tests all the following links in the urls list
# urls = recipes["breakfast"]["regular"] + \
#     recipes["breakfast"]["vegan"] + \
#     recipes["lunch"]["regular"] + \
#     recipes["lunch"]["vegan"] + \
#     recipes["dinner"]["regular"] + \
#     recipes["dinner"]["vegan"] + \
#     recipes["dessert"]["regular"] + \
#     recipes["dessert"]["vegan"]
# try:
#     for url in urls:
#         print(get_recipe_info(url), "\n")
# except:
#     print("\033[91m" + "Error on url: " + url + "\033[0m")


@app.route('/breakfast')  # Flask uses GET method by default
def get_breakfast():
    meal_type = "breakfast"
    # if vegan param is missing or equals anything
    # other than "true", then it is false
    if(request.args.get('vegan') == "true"):
        return get_recipe_info(random.choice(recipes[meal_type]["vegan"]))
    else:
        return get_recipe_info(random.choice(recipes[meal_type]["regular"]))


@app.route('/lunch')
def get_lunch():
    meal_type = "lunch"
    if(request.args.get('vegan') == "true"):
        return get_recipe_info(random.choice(recipes[meal_type]["vegan"]))
    else:
        return get_recipe_info(random.choice(recipes[meal_type]["regular"]))


@app.route('/dinner')
def get_dinner():
    meal_type = "dinner"
    if(request.args.get('vegan') == "true"):
        return get_recipe_info(random.choice(recipes[meal_type]["vegan"]))
    else:
        return get_recipe_info(random.choice(recipes[meal_type]["regular"]))


@app.route('/dessert')
def get_dessert():
    meal_type = "dessert"
    if(request.args.get('vegan') == "true"):
        return get_recipe_info(random.choice(recipes[meal_type]["vegan"]))
    else:
        return get_recipe_info(random.choice(recipes[meal_type]["regular"]))
