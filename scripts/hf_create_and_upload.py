import os
from huggingface_hub import HfApi, create_repo

def main():
    token = os.getenv('HF_TOKEN')
    repo_id = 'Beijuka/maternal-ultrasound-data-collection'
    api = HfApi()

    # Create the space
    try:
        create_repo(
            repo_id=repo_id,
            token=token,
            repo_type='space',
            space_sdk='docker',
            exist_ok=True,
            private=False
        )
        print('Space created or already exists')
    except Exception as e:
        print(f'Error creating space: {e}')

    # Upload the folder
    try:
        api.upload_folder(
            folder_path='.',
            repo_id=repo_id,
            repo_type='space',
            token=token,
            ignore_patterns=['.git*', '__pycache__', '*.pyc', '.github/', 'data/']
        )
        print('Successfully deployed to Hugging Face Spaces!')
    except Exception as e:
        print(f'Error during deployment: {e}')
        exit(1)

if __name__ == "__main__":
    main()
