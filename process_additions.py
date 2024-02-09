import yaml
import os
import subprocess

def load_projects(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file) or {}
            return data
    except Exception as e:
        print(f"Error loading projects from {file_path}: {e}")
    return None

def save_projects(file_path, projects):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(projects, file, sort_keys=False, default_flow_style=False)
    except Exception as e:
        print(f"Error saving projects to {file_path}: {e}")

def mirror_repository(project):
    name = project['name']
    source_url = project['source_url']
    mirror_url = project['mirror_url']
    print(f"Starting mirroring for {name} from {source_url} to {mirror_url}")
    
    try:
        subprocess.run(["git", "clone", "--bare", source_url, name], check=True)
        subprocess.run(["git", "remote", "add", "mirror", mirror_url], cwd=name, check=True)
        subprocess.run(["git", "push", "--mirror", mirror_url], cwd=name, check=True)
        print(f"Mirroring successful for {name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to mirror {name}. Error: {e}")
        return False
    finally:
        # Cleanup: remove the temporary clone
        subprocess.run(["rm", "-rf", name])

def append_to_global_config_and_record_success(project, global_config='repos_to_mirror.yml'):
    """Appends project to global config and records successful addition."""
    # Load or initialize the global projects list
    global_projects = load_projects(global_config) or {'projects': []}
    global_projects['projects'].append(project)
    save_projects(global_config, global_projects)
    
    # Record the successfully mirrored project
    with open('added_projects.txt', 'a') as added_projects_file:
        added_projects_file.write(project['name'] + '\n')

def process_project_additions(project_addition_dir='project_additions', global_config='repos_to_mirror.yml'):
    for file_name in os.listdir(project_addition_dir):
        file_path = os.path.join(project_addition_dir, file_name)
        if file_name.endswith('.yml'):
            project_config = load_projects(file_path)
            if project_config and 'projects' in project_config:
                for project in project_config['projects']:
                    if mirror_repository(project):
                        # Append to global config and record success only if mirroring was successful
                        append_to_global_config_and_record_success(project, global_config)
            os.remove(file_path)  # Remove processed file

def main():
    process_project_additions()

if __name__ == "__main__":
    main()
