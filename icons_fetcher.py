from __future__ import print_function
import sys
import os
import argparse
PY3 = sys.version_info[0] == 3
if PY3:
    from urllib.request import urlopen
    from urllib.parse import urlencode, urlparse
    from urllib.error import URLError
else:
     from urllib import urlopen, urlencode
     import urlparse
     from urllib2 import URLError
from lxml import html, etree
import json
import time

def url_fetch(targeturl, attempt=0, num_retries=5, retry_interval=10):
    """Fetch a
    
    Args:
        targeturl (str): URL to fetch
        attempt (int): Current attempt number
        num_retries (int): Number of times to retry before throwing an exception
        retry_interval (int, optional): Amount of time to wait between retries in seconds
    
    Returns:
        TYPE: Description
    """
    try:
        img_data = urlopen(targeturl).read()
        return img_data
    except URLError as ue:
        # sometimes the connection gets reset when a lot of requests are made.
        if e.errno == errno.ECONNRESET and attempt < num_retries:
            time.sleep(retry_interval)
            return img_fetch(targeturl, attempt + 1, num_retries, retry_interval)
        else:
            raise ue

def download_and_save_image(imgurl, save_dir, num_retries=5, retry_interval=10):
    """Download and save an image. The save name is dervied from the url
    
    Args:
        imgurl (str): Image URL
        save_dir (str): Output directory
        num_retries (int, optional): Number of times to retry before throwing an exception
        retry_interval (int, optional): Amount of time to wait between retries in seconds
    
    Returns:
        dict: Returns dict containing the path and the id of image saved
              ```
              {
                    "path": str, // image save path,
                    "img_id": str, // image id
              }
              ```
    """
    parse_result = urlparse(imgurl)
    img_name = os.path.basename(parse_result.path)
    img_id = img_name.split(".")[0]
    img_data = url_fetch(imgurl, attempt=0, num_retries=num_retries, retry_interval=retry_interval)
    save_name = os.path.join(save_dir, img_name)
    with open(save_name, "wb") as f:
        f.write(img_data)
    return {"path": save_name, "img_id": img_id}

def normalize_search_term(search_term):
    # convert a search query into proper folder name
    return search_term.replace(" ", "_")

def create_save_dir_name(search_term, out_dir):
    """Create a directory name for saving specific search results
    
    Args:
        search_term (str): Search query
        out_dir (str): Output directory
    
    Returns:
        str: Directory in which to store images
    """
    dirname = normalize_search_term(search_term)
    # c = 0
    # while os.path.exists(os.path.join(out_dir, dirname)):
    #     dirname += "(%d)"%c
    #     c+=1
    return os.path.join(out_dir, dirname)

def fetch_icons(search_term, out_dir):
    """Fetch and save icons for given search term
    
    Args:
        search_term (str):search query
        out_dir (str): directory in which to save images
    
    Returns:
        list: List of dicts, dict is as returned by `download_and_save_image`
    """
    search_url = "https://www.flaticon.com/search?" + urlencode({"word": search_term})    
    # download and parse html
    page = urlopen(search_url)
    src = page.read().decode("UTF-8")
    htmlpage = html.fromstring(src)
    icon_paths = '//div[@class="icon--holder"]/img'
    image_tags = htmlpage.xpath(icon_paths)
    # extract urls
    image_urls = [tag.get("src") for tag in image_tags]
    results = []
    # download and save
    for iurl in image_urls:
        result =  download_and_save_image(iurl, out_dir)
        print("[%s]: saved" % search_term, result["img_id"], "at", result["path"])
        results.append(result)
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--inp-file", help="File containing search terms", required=True)
    parser.add_argument("--out-dir", help="Output directory", default="downloaded_images")    
    args = parser.parse_args()

    inp_file = args.inp_file
    out_dir = args.out_dir

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    with open(inp_file, "r") as f:
        for line in f:
            print("fetching for:", line)
            search_term = line.strip(" \n \t, ; ").lower()
            if len(search_term) == 0:
                continue
            # create a valid directory name
            st_out_dir = create_save_dir_name(search_term, out_dir)
            if not os.path.exists(st_out_dir):
                os.makedirs(st_out_dir)
            # fetch icons
            results = fetch_icons(search_term, st_out_dir)