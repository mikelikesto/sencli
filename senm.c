#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
    
    // Set the desired working directory
    const char *directory_path = "";

    // Use chdir to change the working directory
    if (chdir(directory_path) != 0) {
        perror("chdir");
        return 1; // Return an error code if chdir fails
    }

    // Your code for the desired directory goes here

    char command[500];
    strcpy(command, "python -m venv ../.venv && source ../.venv/bin/activate && python /home/server/senpi/Senm.py" );
    system(command);

    return 0; // Return success code
}
