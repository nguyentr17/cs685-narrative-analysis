import os
import subprocess
import time


def main():
    script_to_run = "clinical-extractions/chatgpt.py"

    while True:
        try:
            print("Running the script...")
            subprocess.run(["python", script_to_run], check=True)
            break
        except subprocess.CalledProcessError as e:
            print(
                f"Script crashed with return code {e.returncode}, restarting...")

    # if retries == max_retries:
    #     print("Maximum retries reached. Exiting.")


if __name__ == "__main__":
    main()
