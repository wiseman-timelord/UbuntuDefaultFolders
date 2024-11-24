#!/bin/bash

# Clear screen and display the menu
function show_menu() {
    clear
    echo "================================================================================"
    echo "    UbuntuDefaultFolders-Launcher"
    echo "================================================================================"
    echo ""
    echo "    1. Install Requirements to VENV"
    echo "    2. Run UbuntuDefaultFolders"
    echo ""
    echo "--------------------------------------------------------------------------------"
    echo -n "Selection; Menu Option = 1-2, Exit Program = X: "
}

# Install Python requirements in a virtual environment
function install_requirements() {
    echo "Installing requirements..."
    
    # Ensure Python3 and venv module are installed
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python3 is not installed. Please install it and try again."
        return
    fi

    if ! python3 -m venv --help &> /dev/null; then
        echo "Error: The Python3 venv module is not installed. Installing it..."
        sudo apt update && sudo apt install -y python3-venv
    fi

    # Create a virtual environment in the current directory
    VENV_DIR="./venv"
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment in $VENV_DIR..."
        python3 -m venv "$VENV_DIR"
    fi

    # Activate the virtual environment and install gradio
    source "$VENV_DIR/bin/activate"
    echo "Installing gradio in the virtual environment..."
    pip install --upgrade pip >/dev/null 2>&1
    pip install gradio >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Requirements installed successfully!"
    else
        echo "Error installing requirements. Please check the output for details."
    fi
    deactivate

    read -n 1 -s -r -p "Press any key to return to the menu..."
}

# Run the Python script using the virtual environment
function run_script() {
    VENV_DIR="./venv"
    if [ ! -d "$VENV_DIR" ]; then
        echo "Error: Virtual environment not found. Please run 'Install Requirements' first."
        read -n 1 -s -r -p "Press any key to return to the menu..."
        return
    fi

    if [ -f "ubuntu_default_folders.py" ]; then
        echo "Running UbuntuDefaultFolders..."
        # Use the Python interpreter from the virtual environment directly
        "$VENV_DIR/bin/python3" ./ubuntu_default_folders.py
    else
        echo "Error: 'ubuntu_default_folders.py' not found in the current directory."
        read -n 1 -s -r -p "Press any key to return to the menu..."
    fi

    # Pause before returning to the menu
    read -n 1 -s -r -p "Press any key to return to the menu..."
}

# Main menu logic
while true; do
    show_menu
    read choice
    case $choice in
        1)
            install_requirements
            ;;
        2)
            run_script
            ;;
        X|x)
            echo "Exiting program. Goodbye!"
            break
            ;;
        *)
            echo "Invalid selection! Please choose 1, 2, or X."
            read -n 1 -s -r -p "Press any key to return to the menu..."
            ;;
    esac
done
