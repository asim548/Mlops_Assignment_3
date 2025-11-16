import subprocess
import os


def dvc_track_data(**context):
    """
    Track the processed CSV data with DVC.
    Creates or updates apod_data.csv.dvc file for version control.
    """
    # Get CSV path from XCom
    ti = context['ti']
    csv_path = ti.xcom_pull(task_ids='transform_apod_data', key='transformed_csv_path')
    
    if not csv_path or not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
    # Change to airflow directory where .dvc is initialized
    os.chdir('/opt/airflow')
    
    # Initialize DVC if not already initialized
    if not os.path.exists('.dvc'):
        subprocess.run(['dvc', 'init', '--no-scm'], check=True)
        print("DVC initialized successfully")
    
    # Add the CSV file to DVC
    relative_path = os.path.relpath(csv_path, '/opt/airflow')
    result = subprocess.run(
        ['dvc', 'add', relative_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"DVC add error: {result.stderr}")
        raise RuntimeError(f"Failed to track file with DVC: {result.stderr}")
    
    print(f"DVC Tracking Step Completed!")
    print(f"File tracked: {relative_path}")
    print(f"DVC file created: {relative_path}.dvc")
    print(result.stdout)
    
    # Push metadata to XCom
    dvc_file_path = f"{relative_path}.dvc"
    ti.xcom_push(key='dvc_file_path', value=dvc_file_path)
