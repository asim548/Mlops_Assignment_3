import subprocess
import os


def git_commit_dvc_metadata(**context):
    """
    Commit DVC metadata file to Git repository.
    Ensures data versioning is tracked in version control.
    """
    # Get DVC file path from XCom
    ti = context['ti']
    dvc_file_path = ti.xcom_pull(task_ids='dvc_track_data', key='dvc_file_path')
    
    if not dvc_file_path:
        raise ValueError("DVC file path not found in XCom")
    
    # Change to airflow directory
    os.chdir('/opt/airflow')
    
    try:
        # Configure git user if not already configured
        subprocess.run(['git', 'config', 'user.email', 'airflow@mlops.local'], check=False)
        subprocess.run(['git', 'config', 'user.name', 'Airflow Pipeline'], check=False)
        
        # Stage the DVC metadata file
        result = subprocess.run(
            ['git', 'add', dvc_file_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Git add warning: {result.stderr}")
        
        # Check if there are changes to commit
        status = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True
        )
        
        if not status.stdout.strip():
            print("No changes to commit. DVC metadata already synced.")
            return
        
        # Commit the changes
        commit_result = subprocess.run(
            ['git', 'commit', '-m', f'Update DVC metadata: {dvc_file_path}'],
            capture_output=True,
            text=True
        )
        
        if commit_result.returncode == 0:
            print("Git Commit Step Completed!")
            print(f"Committed: {dvc_file_path}")
            print(commit_result.stdout)
        else:
            print(f"Git commit info: {commit_result.stderr}")
        
        # Push to remote if configured
        push_result = subprocess.run(
            ['git', 'push', 'origin', 'main'],
            capture_output=True,
            text=True
        )
        
        if push_result.returncode == 0:
            print("Changes pushed to remote repository")
        else:
            print(f"Git push note: {push_result.stderr}")
            print("(This is expected if running locally without remote)")
        
    except Exception as e:
        print(f"Git operation error: {str(e)}")
        print("(Continuing pipeline - Git commit is optional)")
