import os
import gradio as gr

# Path to the user directories config file
USER_DIRS_FILE = os.path.expanduser("~/.config/user-dirs.dirs")

# Default directory configurations
DEFAULT_DIRS = {
    "XDG_DESKTOP_DIR": "$HOME/Desktop",
    "XDG_DOWNLOAD_DIR": "$HOME/Downloads",
    "XDG_TEMPLATES_DIR": "$HOME/Templates",
    "XDG_PUBLICSHARE_DIR": "$HOME/Public",
    "XDG_DOCUMENTS_DIR": "$HOME/Documents",
    "XDG_MUSIC_DIR": "$HOME/Music",
    "XDG_PICTURES_DIR": "$HOME/Pictures",
    "XDG_VIDEOS_DIR": "$HOME/Videos"
}

# Read the current folder configuration
def read_user_dirs():
    if not os.path.exists(USER_DIRS_FILE):
        return "Config file not found!", {}
    
    user_dirs = {}
    with open(USER_DIRS_FILE, "r") as file:
        for line in file:
            if line.startswith("XDG_") and "=" in line:
                key, value = line.strip().split("=")
                folder = value.strip('"')
                user_dirs[key] = folder
    return "Config loaded successfully!", user_dirs

# Save updated folder configuration
def save_user_dirs(updated_dirs):
    lines = []
    with open(USER_DIRS_FILE, "r") as file:
        for line in file:
            if line.startswith("XDG_") and "=" in line:
                key = line.split("=")[0]
                if key in updated_dirs:
                    lines.append(f'{key}="{updated_dirs[key]}"\n')
                else:
                    lines.append(line)
            else:
                lines.append(line)
    
    # Write updated config
    with open(USER_DIRS_FILE, "w") as file:
        file.writelines(lines)
    return "Changes saved successfully!"

# Function to handle the apply changes button
def apply_changes(*values, keys):
    """
    Handle applying changes from the Gradio interface
    values: tuple of values from the textboxes
    keys: list of directory keys in the same order as values
    """
    updated_dirs = dict(zip(keys, values))
    return save_user_dirs(updated_dirs)

# Function to apply default values
def apply_defaults(textboxes):
    """
    Apply default values to all textboxes and save changes
    textboxes: dictionary of Gradio textbox components
    """
    # Update the textboxes with default values
    save_user_dirs(DEFAULT_DIRS)
    return [DEFAULT_DIRS[key] for key in textboxes.keys()] + ["Default values applied successfully!"]

# Build Gradio interface
def main():
    status, user_dirs = read_user_dirs()

    with gr.Blocks() as app:
        gr.Markdown("# Default User Folders Configuration")
        
        inputs = {}
        for key, folder in user_dirs.items():
            inputs[key] = gr.Textbox(value=folder, label=key, interactive=True)
        
        status_output = gr.Textbox(label="Status", interactive=False)
        
        with gr.Row():
            update_btn = gr.Button("Apply Changes")
            defaults_btn = gr.Button("Apply Defaults")

        # Handle apply changes button
        update_btn.click(
            fn=lambda *values: apply_changes(*values, keys=list(user_dirs.keys())),
            inputs=list(inputs.values()),
            outputs=[status_output]
        )

        # Handle apply defaults button
        defaults_btn.click(
            fn=lambda: apply_defaults(inputs),
            outputs=list(inputs.values()) + [status_output]
        )

    # Launch the app and ensure the browser opens
    app.launch(inbrowser=True)

if __name__ == "__main__":
    main()
