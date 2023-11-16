import os
import shutil
import tarfile
import datetime
import schedule
import subprocess
import time

# Configuration options
web_root = "/logs/access.log"  # Update this to your web server root directory
backup_dir = "/backup_data"  # Backup destination directory
backup_prefix = "web_backup"
max_backups = int(os.getenv('MAX_NUM_BACKUPS'))
time_backup = float(os.getenv('TIME_BACKUP'))


def create_backup():
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    backup_filename = f"{backup_prefix}_{timestamp}.tar.gz"
    backup_path = os.path.join(backup_dir, backup_filename)

    if os.path.exists(web_root):
        print(f"El archivo {web_root} existe.")
    else:
        print(f"El archivo {web_root} no existe.")


    try:
        with tarfile.open(backup_path, "w:gz") as tar:
            tar.add(web_root, arcname=os.path.basename(web_root))

        return True, f"Backup created: {backup_filename}"

    except Exception as e:
        return False, f"Backup failed: {str(e)}"

def backup_policy():
    try:
        # Clean up old backups
        backup_files = [file for file in os.listdir(backup_dir) if file.startswith(backup_prefix)]
        backup_files = sorted(backup_files, reverse=True)
        message = []
        for old_backup in backup_files[max_backups:]:
            os.remove(os.path.join(backup_dir, old_backup))
            message.append(old_backup)

        out_message = f"These files have been removed: {message}"
        return True, out_message

    except Exception as e:
        return False, f"Failed to apply your backup policy"

def run_backup_job():
    success, message = create_backup()
    return_str = {'create':{'success':success,'message':message}}
    success, message = backup_policy()
    return_str = {'remove policy':{'success':success,'message':message}}

if __name__ == "__main__":
    # Programar la tarea de respaldo cada 1 minuto
    print(time_backup)
    schedule.every(time_backup).minutes.do(run_backup_job)
    # Bucle principal para ejecutar las tareas programadas
    while True:
        schedule.run_pending()
        time.sleep(time_backup)
