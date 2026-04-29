import subprocess
import os

def run_publisher():
    # --field=...:DIR creates a folder picker
    # --field=...:ENTRY creates a text box
    cmd = [
        "yad", "--title=ErmAI Publisher",
        "--form", "--width=500",
        "--field=Project Directory:DIR", os.getcwd(),
        "--field=PyPI API Token", "",
        "--field=Build & Upload:CHK", "TRUE",
        "--button=Launch:0", "--button=Cancel:1"
    ]

    try:
        result = subprocess.check_output(cmd, encoding="utf-8")
        # Split the output from YAD
        project_dir, api_token, run_all, _ = result.split("|")

        if not project_dir or not os.path.isdir(project_dir):
            print("Error: Invalid directory.")
            return

        # Move to the project directory
        os.chdir(project_dir)

        if run_all == "TRUE":
            print(f"--- Building in {project_dir} ---")
            subprocess.run(["python3", "-m", "build"], check=True)

            if api_token:
                print("--- Uploading with Token ---")
                # Set the TWINE_PASSWORD env var so twine doesn't prompt you
                env = os.environ.copy()
                env["TWINE_USERNAME"] = "__token__"
                env["TWINE_PASSWORD"] = api_token
                
                subprocess.run(
                    ["python3", "-m", "twine", "upload", "dist/*"], 
                    env=env, 
                    check=True
                )
            else:
                print("Error: API Token is required for upload.")

    except subprocess.CalledProcessError:
        print("User cancelled the operation.")

if __name__ == "__main__":
    run_publisher()
