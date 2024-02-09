import subprocess
import yaml
import os

def clone_and_mirror(repo_config):
    name = repo_config['name']
    source_url = repo_config['source_url']
    mirror_url = repo_config['mirror_url']
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

def main(config_file='repos_to_mirror.yml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
        for project in config['projects']:
            try:
                clone_and_mirror(project)
            except subprocess.CalledProcessError as e:
                print(f"Error mirroring {project['name']}: {e}")

if __name__ == "__main__":
    main()
