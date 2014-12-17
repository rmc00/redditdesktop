from uuid import uuid4
import json
from RedditUrlOpener import RedditUrlOpener
import os
import tempfile
import datetime
import configparser


def get_front_page_urls(subreddit, link_count, username):
    reddit_opener = RedditUrlOpener(username)
    front_page = reddit_opener.open("http://www.reddit.com" + subreddit + "/hot.json?limit=" + str(link_count))
    response_string = front_page.read().decode('utf-8')
    response_data = json.loads(response_string)
    return [child["data"]["url"] for child in response_data["data"]["children"]]


def download_to_folder(url, folder, username):
    try:
        with open(folder + "\\" + str(uuid4())+".jpg", 'wb') as f:
            reddit_opener = RedditUrlOpener(username)
            f.write(reddit_opener.open(url).read())
            f.close()
    except:
        print("download failed for " + url)


def clear_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def move_all_files(source, destination):
    create_directory(source)
    create_directory(destination)
    for the_file in os.listdir(source):
        file_path = os.path.join(source, the_file)
        if os.path.isfile(file_path):
            os.rename(file_path, os.path.join(destination, the_file))


def setup_temp_directory(folder):
    create_directory(folder)
    clear_folder(folder)

def create_directory(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def delete_old_files(folder, hours):
    threshold = datetime.datetime.now() - datetime.timedelta(hours=hours)
    print("files older than " + threshold.strftime("%m/%d/%Y %H:%M") + " will be deleted")
    for f in os.listdir(folder):
        full_name = os.path.join(folder, f)
        mod_time = datetime.datetime.fromtimestamp(os.stat(full_name).st_mtime)
        if os.path.isfile(full_name) and mod_time < threshold:
            os.remove(full_name)


def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return {
        "subreddits" : config["DEFAULT"]["SubReddits"].split(","),
        "username" : config["DEFAULT"]["RedditUserName"],
        "link_count" : int(config["DEFAULT"]["LinkCount"]),
        "image_extensions" : config["DEFAULT"]["ImageExtensions"].split(","),
        "wallpaper_folder" : config["DEFAULT"]["WallpaperFolder"],
        "max_file_age_hours" : int(config["DEFAULT"]["MaxFileAgeHours"]),
        "wallpaper_folder" : config["DEFAULT"]["WallpaperFolder"]
    }


def main():
    config = get_config()
    temp_folder = os.path.join(tempfile.gettempdir(), "redditdesktop")
    setup_temp_directory(temp_folder)

    urls = []
    for subreddit in config["subreddits"]:
        print("Getting front page for " + subreddit)
        urls.extend(get_front_page_urls(subreddit, config["link_count"], config["username"]))

    for url in urls:
        if url[-3:] in config["image_extensions"]:
            print("Downloading " + url)
            download_to_folder(url, temp_folder, config["username"])

    move_all_files(temp_folder, config["wallpaper_folder"])
    delete_old_files(config["wallpaper_folder"], config["max_file_age_hours"])


if __name__ == "__main__":
    main()
