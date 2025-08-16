import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import config
from utils import get_folder
import logging

rss_path = get_folder("output") + config.RSS_PATH

def build_rss(entry_list):
    logging.info("Building RSS Feed...")

    if not entry_list:
        return

    entry_list = sorted(
        entry_list,
        key=lambda p: datetime.strptime(p["pubDate"], "%a, %d %b %Y %H:%M:%S %z"),
        reverse=True  # Newest first
    )


    ET.register_namespace('atom', 'http://www.w3.org/2005/Atom')

    rss = ET.Element('rss', {
        'version': '2.0',
    })
    channel = ET.SubElement(rss, 'channel')

    ET.SubElement(channel, 'lastBuildDate').text = entry_list[0]["pubDate"]

    # Channel metadata
    for key, value in config.RSS_CHANNEL.items():
        ET.SubElement(channel, key).text = value

    # Atom self-link
    ET.SubElement(channel, '{http://www.w3.org/2005/Atom}link', {
        'href': config.SITE_ROOT.rstrip('/') + config.RSS_PATH,
        'rel': 'self',
        'type': 'application/rss+xml'
    })

    # Add items
    for entry in entry_list[:config.RSS_FEED_COUNT]:
        xml_entry = ET.SubElement(channel, 'item')
        for key, value in entry.items():
            if key in ["title", "pubDate", "description", "link", "guid"]:
                ET.SubElement(xml_entry, key).text = value

    tree = ET.ElementTree(rss)
    tree.write(rss_path, encoding='utf-8', xml_declaration=True)
    logging.info("Built!")
