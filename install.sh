#!/bin/bash

# Get the current working directory
read -p "Enter the path for the downloaded content | (This can be changed in config.ini) | " user_path
read -p "Where is you Senpwai folder located | (This can be changed in config.ini) | " senpath
read -p "Do you want dub or sub | (This can be changed in config.ini) | " sub_or_dub


# Your INI file path
ini_file="config.ini"
# Update the INI file with the user-provided path
sed -i "s|^path =.*|path = $user_path|" "$ini_file"
sed -i "s|^sub_or_dub =.*|sub_or_dub = $sub_or_dub|" "$ini_file"

# Update the C file with the current directory
c_file="senfetch.c"

# Use a simpler approach to update directory_path
sed -i "s|const char \*directory_path = \".*\";|const char *directory_path = \"$senpath\\/src\";|g" "$c_file"

gcc senfetch.c -o sencli

sudo mv senm /bin
