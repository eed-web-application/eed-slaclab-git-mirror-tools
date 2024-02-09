import yaml
import os
import subprocess

def load_projects(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def save_projects(file_path, projects):
    with open(file_path, 'w') as file:
        yaml.dump(projects, file, sort_keys=False, default_flow_style=False)

def append_to_global_config(project_file, global_config='repos_to_mirror.yml'):
    project_config = load_projects(project_file)
    if os.path.exists(global_config):
        global_projects = load_projects(global_config)
    else:
        global_projects = {'projects': []}
    
    global_projects['projects'].extend(project_config['projects'])
    save_projects(global_config, global_projects)

    # Write the names of added projects to a temporary file
    with open('added_projects.txt', 'a') as added_projects_file:
        for project in project_config['projects']:
            added_projects_file.write(project['name'] + '\n')

def process_project_additions(project_addition_dir='project_additions', completed_dir='completed'):
    for file_name in os.listdir(project_addition_dir):
        file_path = os.path.join(project_addition_dir, file_name)
        if file_name.endswith('.yml'):
            append_to_global_config(file_path)
            os.remove(file_path)  # Remove processed file

def main():
    process_project_additions()

if __name__ == "__main__":
    main()
