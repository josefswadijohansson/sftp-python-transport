import paramiko
paramiko.util.log_to_file("paramiko.log")
import os

def sftp_upload(host, port, username, password, local_file_path, remote_directory):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()

        # Automatically add untrusted hosts (for production, consider using known_hosts)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        client.connect(host, port=port, username=username, password=password)

        # Create an SFTP session from the connected SSH client
        sftp = client.open_sftp()

        # Ensure the remote directory exists
        try:
            sftp.chdir(remote_directory)  # Test if remote_directory exists
        except FileNotFoundError:
            print(f"Remote directory '{remote_directory}' does not exist. Creating it.")
            sftp.mkdir(remote_directory)  # Create remote directory
            sftp.chdir(remote_directory)  # Change to the new directory

        # Prepare the remote file path
        remote_file_path = os.path.join(remote_directory, os.path.basename(local_file_path))

        # Upload the file
        print(f"Uploading '{local_file_path}' to '{remote_file_path}'...")
        sftp.put(local_file_path, remote_file_path)
        print("Upload complete.")

        # Close the SFTP session and SSH client
        sftp.close()
        client.close()

    except Exception as e:
        print(f"Error: {e}")

def list_remote_files(host, port, username, password, remote_directory):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()

        # Automatically add untrusted hosts (for production, consider using known_hosts)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        client.connect(host, port=port, username=username, password=password)
        print("Connection to SFTP server successful.")

        # Create an SFTP session from the connected SSH client
        sftp = client.open_sftp()

        # Change to the specified remote directory
        sftp.chdir(remote_directory)
        print(f"Changed to remote directory: {remote_directory}")

        # List files and directories in the remote directory
        files = sftp.listdir()
        print("Files and directories in remote directory:")
        for file in files:
            print(file)

        # Close the SFTP session and SSH client
        sftp.close()
        client.close()
        print("Connection closed.")

    except Exception as e:
        print(f"Error: {e}")

# Example usage:
host = "192.168.1.105"     # IP address or hostname of the SFTP server
port = 22             # SFTP port (default is 22, adjust if needed)
username = "josef"
password = ""

# For upload
local_file_path = "./text.txt"
remote_directory = "/home/josef/recieve/"

# To upload a file:
sftp_upload(host, port, username, password, local_file_path, remote_directory)

# To list the files in the directory
list_remote_files(host, port, username, password, remote_directory)

# To download a file:
# sftp_transfer(host, port, username, password, local_file, remote_file, action="download")
