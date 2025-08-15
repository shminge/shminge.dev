import xml.etree.ElementTree as ET
from datetime import datetime
import config
from utils import get_folder


rss_path = get_folder("output") + config.RSS_PATH

def build_rss(entry_list):
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')

    ET.SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')

    for key, value in config.RSS_CHANNEL.items():
        ET.SubElement(channel, key).text = value


    for entry in entry_list[:config.RSS_FEED_COUNT]:
        xml_entry = ET.SubElement(channel, 'item')
        for key, value in entry.items():
            ET.SubElement(xml_entry, key).text = value


    tree = ET.ElementTree(rss)
    tree.write(rss_path, encoding='utf-8', xml_declaration=True)