import subprocess
import requests
import json
import os

#TODO have the user specify the folder as stdin?
bwp = "/home/arrowx/Pictures/Bing/"

def main():
    #TODO Some sort of safty here
    r = requests.get('https://bing.biturl.top/?resolution=1920&format=json&index=0&mkt=zh-CN')
    image_url = json.loads(r.text)['url']
    file_name = image_url.split("/")[-1]

    if os.path.isfile(bwp+file_name) : 
        print("file already exist")
        return None

    r_url = requests.get(image_url, timeout=5)

    with open(bwp+file_name, 'wb') as f:
        f.write(r_url.content)

    get_monitors_cmd = "xfconf-query --channel xfce4-desktop --list | grep /workspace0| grep last-image"
    _monitors = subprocess.run(get_monitors_cmd, shell=True, capture_output=True, text=True)
    monitors = _monitors.stdout.splitlines()

    cmd_string = "xfconf-query --channel xfce4-desktop --property {mon} --set {img}"
    for i in monitors:
        command = cmd_string.format(mon = i, img = bwp+file_name)
        subprocess.run(command, shell=True)

    return None

if __name__ == "__main__":
    main()
