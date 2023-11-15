import configparser
import os
import re
import subprocess
import time






os.system("clear")



config = configparser.ConfigParser()
config.read("/home/server/senpi/config.ini")

site = config.get("Sen", "site")
quality = config.get("Sen", "quality")
sub_or_dub = config.get("Sen", "sub_or_dub")
path = config.get("Sen", "path")



I = input("What's the name of the anime | ")
IN = f'"{I + "1"}"'

output_string = os.popen("python -m scrapers.test download_size -site pahe -v --title " + IN).read()

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
   print("No Anime with that name can be found!")



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


print("Fetching metadata.....")
output_string2 = os.popen("python -m scrapers.test metadata download_size --site " + site + " --title " + selected_anime_name_quoted + " -v --quality " + quality + " --sub_or_dub " + sub_or_dub + " -se 1 ").read()

# Use a more specific regular expression to capture the episode count
Ep = re.search(r"Episode Count: (\d+)", output_string2)


if Ep:
    episode_count = Ep.group(1)
    print("Episode Count:", episode_count)
else:
    print("Episode count not found.")



print("Calculating size.....")
output_string3 = os.popen("python -m scrapers.test metadata download_size --site " + site + " --title " + selected_anime_name_quoted + " -v --quality " + quality + " --sub_or_dub " + sub_or_dub + " -se 1 -ee " + episode_count + " ").read()




Dw = re.search(r"Total download size is: (\d+)", output_string3)




if Dw:
    download_size = Dw.group(1)
    print("Total download size is:", download_size)
else:
    print("Total download size count not found.")



print("Downloading...")

#output_string_second = os.system("python -m scrapers.test all --site " + site " --quality " + quality" --sub_or_dub " + sub_or_dub" --path " + path " -v --title " + selected_anime_name_quoted + " -se 1 -ee " + episode_count )
cmd = [
    "python", "-m", "scrapers.test", "all",
    "--site", site,
    "--quality", quality,
    "--sub_or_dub", sub_or_dub,
    "--path", path,
    "-v", "--title", selected_anime_name_quoted,
    "-se", "1", "-ee", episode_count
]

print("fetching links, Please wait a minute, this may take long")
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)

download_folder_path = '/home/server/senpi/testfolder'  # Update with the actual path

# Convert the expected download size from string to integer
expected_download_size = int(download_size) * (1024 ** 2)

# Create a custom progress bar
def update_progress_bar(current_size, total_size):
    progress_percentage = (current_size / total_size) * 100
    print(f"\rProgress: [{'#' * int(progress_percentage // 2)}{' ' * (50 - int(progress_percentage // 2))}] {progress_percentage:.2f}%", end='', flush=True)

# Check if the folder exists
if os.path.exists(download_folder_path):
    # Get the initial size of the folder
    current_size = sum(os.path.getsize(os.path.join(download_folder_path, file)) for file in os.listdir(download_folder_path))

    # Print the initial progress bar
    update_progress_bar(current_size, expected_download_size)

    # Enter a loop to continuously update the progress bar
if os.path.exists(download_folder_path):
    # Get the initial size of the folder
    current_size = sum(os.path.getsize(os.path.join(download_folder_path, file)) for file in os.listdir(download_folder_path))

    # Print the initial progress bar
    update_progress_bar(current_size, expected_download_size)

    # Enter a loop to continuously update the progress bar
    while current_size < expected_download_size:
        # Sleep for a few seconds before checking again
        time.sleep(5)

        # Get the current size of the folder
        current_size = sum(os.path.getsize(os.path.join(download_folder_path, file)) for file in os.listdir(download_folder_path))

        # Update the progress bar
        update_progress_bar(current_size, expected_download_size)

        # Check if the subprocess has finished
        if process.poll() is not None:
            break



    print("\nDownload complete!")
else:
    print(f"The specified folder '{download_folder_path}' does not exist.")


process.communicate()

print("Download complete!")

