import requests
import pprint
from bs4 import BeautifulSoup, Tag


def sort_by_votes(hnlist: list[dict]) -> list[dict]:
    return sorted(hnlist, key=lambda k: k["votes"], reverse=True)


def create_custom_hn(links: list[Tag], subtext: list[Tag]) -> list[dict]:
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get("href", None)
        vote = subtext[idx].select(".score")
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points >= 100:
                hn.append({"title": title, "link": href, "votes": points})
    return sort_by_votes(hn)


def main():
    pg1 = requests.get("https://news.ycombinator.com/news")
    pg2 = requests.get("https://news.ycombinator.com/news?p=2")

    soup_pg1 = BeautifulSoup(pg1.text, "html.parser")
    links_pg1 = soup_pg1.select(".titleline > a")
    subtext_pg1 = soup_pg1.select(".subtext")

    soup_pg2 = BeautifulSoup(pg2.text, "html.parser")
    links_pg2 = soup_pg2.select(".titleline > a")
    subtext_pg2 = soup_pg2.select(".subtext")

    mega_links = links_pg1 + links_pg2
    mega_subtext = subtext_pg1 + subtext_pg2

    pprint.pprint(create_custom_hn(mega_links, mega_subtext))


if __name__ == "__main__":
    main()
