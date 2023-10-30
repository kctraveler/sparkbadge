# This is a sample script of how the package might be used.
from typing import Any, Iterator
import requests
from itertools import islice
from sparkbadge import Sparkbadge


class Observer:
    """Simple base observer for printing output."""

    def update(self, data: Any):
        print(data)


class DisplayBadge(Observer):
    def update(self, badge: Sparkbadge):
        badge.preview()


def get_data(url: str) -> Iterator[dict]:
    """Generator for build coverage data"""
    page = 1
    data = requests.get(url, params={"page": page}).json()
    while page <= data["pages"]:
        for build in data["builds"]:
            yield build
        page += 1
        data = requests.get(url, params={"page": page}).json()


def parse(raw_data: dict) -> dict:
    """Parse build data down to only the values we need"""
    return {
        "created_at": raw_data["created_at"],
        "coverage_change": raw_data["coverage_change"],
        "covered_percent": raw_data["covered_percent"],
    }


def run(input: Iterator[dict], out: Observer, count: int = 10):
    main_branches = filter(lambda build: build["branch"] in ["main", "master"], input)
    parsed_data = map(parse, main_branches)
    # reverse the data to ascending order to be graphed
    recents = list(islice(parsed_data, count))[::-1]
    points = [int(x["covered_percent"]) for x in recents]
    badge = Sparkbadge(
        metric_data=points, metric_name="Coverage", right_text=f"{points[-1]}%"
    )
    out.update(badge)


if __name__ == "__main__":
    url = "https://coveralls.io/github/kctraveler/github-actions.json"
    run(get_data(url), DisplayBadge())
