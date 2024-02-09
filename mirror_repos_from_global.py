import subprocess
import yaml
import os

def clone_and_mirror(repo_config):
    name = repo_config['name']
    source_url = repo_config['source_url']
    mirror_url = repo_config['mirror_url']
    
    print(f"Mirroring {name}...")
    print(f"Source URL: {source_url}")
    print(f"Mirror URL: {mirror_url}")
    
    # Clone the source repository
    subprocess.run(["git", "clone", "--mirror", source_url, name], check=True)
    os.chdir(name)
    # Add the mirror repository as a remote
    subprocess.run(["git", "remote", "add", "mirror", mirror_url], check=True)
    # Push to the mirror repository
    subprocess.run(["git", "push", "--mirror", mirror_url], check=True)
    os.chdir("..")
    # Remove the cloned repository to clean up
    subprocess.run(["rm", "-rf", name], check=True)
    print(f"{name} successfully mirrored.")

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
