import configparser
import os
import re

IN=input("Whats the name of the anime | ")

output_string = os.popen("python -m scrapers.test search --site pahe --V --title " + IN).read()

# Your output string
# Use regular expression to extract the content between square brackets
match = re.search(r"Search results were: \[(.*?)\]", output_string, re.DOTALL)
if match:
    results_string = match.group(1)
    # Convert the string to a list of tuples
    search_results = eval(results_string)

    # Extract and display only the names of the anime
    for idx, result in enumerate(search_results, start=1):
        anime_name = result[0]
        print("{}. {}".format(idx, anime_name))
else:
    print("No search results found.")

NB = input("Select the number of the anime | ")

# Ensure NB is a valid integer
try:
    NB = int(NB)
except ValueError:
    print("Invalid input. Please enter a valid number.")
    exit(1)

# Check if the selected number is within the valid range
if 1 <= NB <= len(search_results):
    selected_anime_name = search_results[NB - 1][0]
    selected_anime_name_quoted = f'"{selected_anime_name}"' 
else:
    print("Invalid selection. Please enter a valid number.")
    exit(1)

# Now you can use `selected_anime_name` in your second query
output_string_second = os.system("python -m scrapers.test all --site pahe --quality 1080p --sub_or_dub dub --path /home/server/nas1/Plexser/tv/sen -V --title " + selected_anime_name_quoted)
