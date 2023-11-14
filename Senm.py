import configparser
import os
import re
os.system("clear")
IN = input("What's the name of the anime | ")

output_string = os.popen("python -m scrapers.test download_size --site pahe --V --title " + IN).read()

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

output_string2 = os.popen("python -m scrapers.test metadata --site pahe --title " + selected_anime_name_quoted + " -v").read()

# Use a more specific regular expression to capture the episode count
Ep = re.search(r"Episode Count: (\d+)", output_string2)
if Ep:
    episode_count = Ep.group(1)
    print("Episode Count:", episode_count)
else:
    print("Episode count not found.")

config = configparser.ConfigParser()
config.read("")

site = config.get("Sen", "site")
quality = config.get("Sen", "quality")
sub_or_dub = config.get("Sen", "sub_or_dub")
path = config.get("Sen", "path")


#output_string_second = os.system("python -m scrapers.test all --site " + site " --quality " + quality" --sub_or_dub " + sub_or_dub" --path " + path " -v --title " + selected_anime_name_quoted + " -se 1 -ee " + episode_count )
output_string_second = os.system(
    "python -m scrapers.test all --site " + site +
    " --quality " + quality +
    " --sub_or_dub " + sub_or_dub +
    " --path " + path +
    " -v --title " + selected_anime_name_quoted +
    " -se 1 -ee " + episode_count
)
