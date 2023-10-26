from httpx import get
import os
from selectolax.parser import HTMLParser
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
search_tag =input("Enter your picture tag : ")
def get_img_tags_for(term=None):
    url =f"https://unsplash.com/s/photos/{term}"
    resp = get(url)
    if resp.status_code != 200:
        raise Exception("Error getting response")

    tree = HTMLParser(resp.text)
    imgs = tree.css("figure a img")
    return imgs

def img_filter_out(url:str, keywords:list) -> bool:
    return not any(x in url for x in keywords)
def get_high_res_img_url(img_node):
    srcset = img_node.attrs["src"]
    srcset_list = srcset.split(", ")
    url_res = [src.split(" ") for src in srcset_list if img_filter_out(src, ['plus', 'premium', 'profile','base64'])]
    if not url_res:
        return None
    return url_res[0][0].split("?")[0]
def save_images(img_urls, dest_dir="images", tag=""):

    for url in img_urls:
        resp = get(url)
        logging.info(f"downloading {url} ...")
        file_name = url.split("/")[-1]

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        logging.info(f"Making root Directory...")
        with open(f"{dest_dir}/{tag}{file_name}.jpeg","wb") as f:
            f.write(resp.content)
            logging.info(f"Saved {file_name} ...")

if __name__ == '__main__':
    img_nodes = get_img_tags_for(search_tag)
    all_img_urls = [get_high_res_img_url(i) for i in img_nodes]
    img_urls = [u for u in all_img_urls if u]
    save_images(img_urls[:5],"images",f"{search_tag}")


