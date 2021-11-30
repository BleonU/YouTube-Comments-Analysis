import Algorithm
import Scraper
import json
import shutil


def main():
    data = []
    with open('comments.json', encoding="utf8") as f:
        for line in f:
            data.append(json.loads(line))
    Algorithm.main(data)

if __name__ == "__main__":
    main()
