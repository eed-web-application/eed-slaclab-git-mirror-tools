import yaml
import os
import subprocess

def load_projects(file_path):
    """Load projects from a YAML file with enhanced error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            if data is None:  # In case the file is empty or only contains comments
                return {'projects': []}
            return data
    except yaml.YAMLError as e:
        print(f"YAML parsing error in {file_path}: {e}")
    except Exception as e:
        print(f"Error loading projects from {file_path}: {e}")
    return None

def save_projects(file_path, projects):
    """Save projects to a YAML file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(projects, file, sort_keys=False, default_flow_style=False)
    except Exception as e:
        print(f"Error saving projects to {file_path}: {e}")

def append_to_global_config(project_file, global_config='repos_to_mirror.yml'):
    """Append project configuration from a file to the global configuration."""
    project_config = load_projects(project_file)
    if project_config is None:
        return  # Exit if the project configuration could not be loaded
    if 'projects' not in project_config:
        print(f"Missing 'projects' key in {project_file}")
        return

    if os.path.exists(global_config):
        global_projects = load_projects(global_config)
        if global_projects is None:
            return
    else:
        global_projects = {'projects': []}

    global_projects['projects'].extend(project_config['projects'])
    save_projects(global_config, global_projects)

    # Write the names of added projects to a temporary file for commit message
    with open('added_projects.txt', 'a') as added_projects_file:
        for project in project_config['projects']:
            added_projects_file.write(project['name'] + '\n')

def process_project_additions(project_addition_dir='project_additions'):
    """Process all project addition files in the specified directory."""
    for file_name in os.listdir(project_addition_dir):
        file_path = os.path.join(project_addition_dir, file_name)
        if file_name.endswith('.yml'):
            append_to_global_config(file_path)
            os.remove(file_path)  # Remove processed file after appending

def main():
    """Main function to process project additions."""
    process_project_additions()

if __name__ == "__main__":
    main()
