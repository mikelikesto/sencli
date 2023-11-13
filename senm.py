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
    for result in search_results:
        anime_name = result[0]
        print(anime_name)
else:
    print("No search results found.")
