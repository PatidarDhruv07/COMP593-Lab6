import requests, hashlib, subprocess, os

def main():
    # Get SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)
        
        # Silently run the VLC installer
        run_installer(installer_path)
        
        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    path_to_download = "http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe.sha256"
    resquests = requests.get(path_to_download)

    if resquests.ok:
        with open('HashValue.txt', 'w') as f:
            f.write(resquests.content.decode().split(" ")[0])
            print("File Downloaded!")
        with open('HashValue.txt', 'r') as f:
            expected_value_of_hash = f.readline()
        return expected_value_of_hash

def download_installer():
    url = "http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe"
    response_msg = requests.get(url)
    
    if response_msg.status_code == requests.codes.ok:
        return response_msg

def installer_ok(installer_data, expected_sha256):
    installer_hash = hashlib.sha256(installer_data.content).hexdigest()

    if installer_hash == expected_sha256:
        return True
    else:
        return False

def save_installer(installer_data):
    installers_path = os.getenv('TEMP')+"\\vlc_installer.exe"
    data_content = installer_data.content

    with open(installers_path, "wb") as f:
        f.write(data_content)
    return installers_path

def run_installer(installer_path):
    installer_path = os.path.abspath(installer_path)
    subprocess.run([installer_path, '/L=1033', '/S'])
    return

def delete_installer(installer_path):
    installer_path = os.path.abspath(installer_path)
    os.remove(installer_path)
    return

if __name__ == '__main__':
    main()