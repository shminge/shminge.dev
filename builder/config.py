# The root folder
ROOT = ".."

# folder to store the components in
COMPONENTS = "/components"

# folder for builder to build
SOURCE = "/src"

# destination folder for the built site
OUTPUT = "/docs"

# how deep to render nested components
MAX_RECURSION = 10


# Optional features
PARSE_MD = True
PARSE_MD_LINKS = True

# RSS Features
GENERATE_RSS = True

# where to save the rss
RSS_PATH = "/feed.xml"

# how many of the latest posts to include on the feed
RSS_FEED_COUNT = 15

SITE_ROOT = "https://shminge.dev/"

RSS_CHANNEL = {
    'title': 'shminge.dev',
    'link': 'https://shminge.dev/',
    'description':'Posts from shminge.dev, covering various topics',
    'language': 'en-us'
}


GLOBAL_PARAMS = {
    "pages": [],
}

