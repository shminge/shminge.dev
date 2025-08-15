import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import config
from utils import get_folder

rss_path = get_folder("output") + config.RSS_PATH

def build_rss(entry_list):
    ET.register_namespace('atom', 'http://www.w3.org/2005/Atom')

    rss = ET.Element('rss', {
        'version': '2.0',
    })
    channel = ET.SubElement(rss, 'channel')

    ET.SubElement(channel, 'lastBuildDate').text = datetime.now(timezone.utc).strftime(
        '%a, %d %b %Y %H:%M:%S +0000'
    )

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
            ET.SubElement(xml_entry, key).text = value

    tree = ET.ElementTree(rss)
    tree.write(rss_path, encoding='utf-8', xml_declaration=True)
