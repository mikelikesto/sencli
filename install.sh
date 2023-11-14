#!/bin/bash

# Get the current working directory
current_directory=$(pwd)

# Prompt the user for input
read -p "Enter the path for the downloaded content | (This can be changed in config.ini) | " user_path
read -p "Where is your Senpwai folder located | (This can be changed in config.ini) | " senpath
read -p "Do you want dub or sub | (This can be changed in config.ini) | " sub_or_dub

# Your INI file path
ini_file="config.ini"
# Update the INI file with the user-provided path
sed -i "s|^path =.*|path = $user_path|" "$ini_file"
sed -i "s|^sub_or_dub =.*|sub_or_dub = $sub_or_dub|" "$ini_file"

# Update the C file with the current directory
c_file="senfetch.c"
sed -i "s|const char \*directory_path = \".*\";|const char \*directory_path = \"$senpath\\/src\";|g" "$c_file"

# Update the Python script with the current directory
python_script="Senm.py"
sed -i "s|config.read(\"\")|config.read(\"$current_directory\/config.ini\")|" "$python_script"

# Run your Python script with the current directory

gcc senfetch.c -o sencli

sudo mv sencli /bin

sencli
