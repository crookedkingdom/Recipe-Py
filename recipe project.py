import requests


def get_exclusions():
    """
    Ask the user if they want to exclude any ingredients from the search and collect those exclusions.
    """
    exclusions = []
    ask_restrictions = input("Do you want to exclude any ingredients from the search? yes/no ").strip().lower()

    if ask_restrictions == "yes":
        while True:
            exclusion = input("Please enter an ingredient you want to exclude: ")
            exclusions.append(exclusion)
            add_more = input("Do you want to exclude another ingredient? yes/no ")
            if add_more != "yes":
                break

    # print(exclusions)  # Print the list of exclusions
    return exclusions


def get_cuisine_type():
    """
    Ask the user for their preferred cuisine type.
    """
    return input("Enter a cuisine type (e.g., American, Chinese, Italian etc.) or leave blank for no preference: ").strip().lower()


def get_calorie_range():
    """
    Ask the user for their preferred calorie range.
    """
    return input("Enter calorie range (e.g., 100-300) or leave blank for no preference: ").strip().lower()


def recipe_search(ingredient, exclusions, cuisine, calories):
    """
    Search for recipes based on the user's criteria.
    """
    app_id = '2494b7d1'
    app_key = 'd2a8cae7c64ff1a4b653baf56db8f217'
    base_url = f'https://api.edamam.com/api/recipes/v2?type=public&q={ingredient}&app_id={app_id}&app_key={app_key}'

    # Add exclusions to the URL
    for exclusion in exclusions:
        base_url += f"&excluded={exclusion}"

    # Add cuisine type to the URL
    if cuisine:
        base_url += f"&cuisineType={cuisine}"

    # Add calorie range to the URL
    if calories:
        base_url += f"&calories={calories}"
    print(f"URL with all filters: {base_url}")  # Print the URL for debugging
    result = requests.get(base_url)  # Send a request to the API
    data = result.json()  # Convert the response to JSON
    return data.get('hits', [])  # Return the list of recipes


def print_recipe_details(recipe, file):
    """
    Print details of a recipe, including title, URL, total time, servings, and ingredients.
    """
    print(f"Title: {recipe['label']}")
    print(f"URL: {recipe['url']}")
    file.write(f"Title: {recipe['label']}\n")
    file.write(f"URL: {recipe['url']}\n")

    total_time = recipe.get('totalTime')
    if total_time is not None:
        if total_time > 0:
            hours = total_time // 60
            minutes = total_time % 60
            print(f"Total Time: {hours} hours and {minutes} minutes")
            file.write(f"Total Time: {hours} hours and {minutes} minutes \n")
        else:
            print("Total Time: Not available")
            file.write(f"Total Time: Not available\n")
    else:
        print("Total Time: Not available")
        file.write(f"Total Time: Not available\n")

    servings = recipe.get('yield')
    if servings is not None:
        file.write(f"Servings: {servings}\n")
        print(f"Servings: {servings}")
    else:
        print("Servings: Not available")
        file.write(f"Servings: Not available\n")

    ingredients = recipe.get('ingredients', [])
    if ingredients:
        print("Shopping List:")
        file.write(f'Shopping List: \n')                            # Changed heading from Ingredients to Shopping List
        for ingredient in ingredients:
            print(f"- {ingredient['food'].lower()}")
            file.write(f"- {ingredient['food'].lower()}\n")
    else:
        print("No ingredients found.")
        file.write(f"No ingredients found.\n")

    print()  # Print a blank line for readability
    file.write('\n')


def run():
    """
    Main function to run the recipe search and display results.
    """
    ingredient = input('Enter an ingredient or several ingredients separated by comma: ')
    exclusions = get_exclusions()
    cuisine = get_cuisine_type()
    calories = get_calorie_range()
    # allergies = get_allergies()
    results = recipe_search(ingredient, exclusions, cuisine, calories)

    if len(results) == 0:  # Check if there are no recipes found
        print("No results found. Please try again.")
    else:
        print(f'Found {len(results)} recipes matching your criteria: \n')

        with open("recipes search.txt", "w", encoding="utf-8") as file:
            """ 
            Open file for writing before the loop, with UTF-8 encoding
            """
            for i, result in enumerate(results, start=1):
                recipe = result['recipe']
                print(f"Recipe {i}:")
                file.write(f"Recipe {i}:\n")  # Write recipe index to file
                print_recipe_details(recipe, file)  # Pass the file to the function to write details
        print("Results have been written to recipes search.txt")


run()