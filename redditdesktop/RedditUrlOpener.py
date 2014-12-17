from urllib.request import FancyURLopener


class RedditUrlOpener(FancyURLopener):
    def __init__(self, username):
        FancyURLopener.__init__(self)
        FancyURLopener.version = "/u/" + username + " getting awesome wallpapers"