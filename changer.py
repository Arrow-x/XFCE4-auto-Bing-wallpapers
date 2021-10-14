import subprocess
import requests
import json
import os

#TODO Auto Detect the system moniors (for XFCE4 now, maybe i3 later?
monitorVGA= "/backdrop/screen0/monitorVGA-1/workspace0/last-image"
monitorLVDS= "/backdrop/screen0/monitorLVDS-1/workspace0/last-image"
monitors = [monitorLVDS,monitorVGA]
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

    cmd_string = "xfconf-query --channel xfce4-desktop --property {mon} --set {img}"
    for i in monitors:
        command = cmd_string.format(mon = i, img = bwp+file_name)
        subprocess.run(command, shell=True)

    return None

if __name__ == "__main__":
    main()
