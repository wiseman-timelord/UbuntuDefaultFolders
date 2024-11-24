import os
import gradio as gr

# Path to the user directories config file
USER_DIRS_FILE = os.path.expanduser("~/.config/user-dirs.dirs")

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

# Build Gradio interface
def main():
    status, user_dirs = read_user_dirs()

    with gr.Blocks() as app:
        gr.Markdown("# Default User Folders Configuration")
        
        inputs = {}
        for key, folder in user_dirs.items():
            inputs[key] = gr.Textbox(value=folder, label=key, interactive=True)
        
        status_output = gr.Textbox(label="Status", interactive=False)
        update_btn = gr.Button("Apply Changes")

        # Handle button click - pass the directory keys as additional argument
        update_btn.click(
            fn=lambda *values: apply_changes(*values, keys=list(user_dirs.keys())),
            inputs=list(inputs.values()),
            outputs=[status_output]
        )

    # Launch the app and ensure the browser opens
    app.launch(inbrowser=True)

if __name__ == "__main__":
    main()
