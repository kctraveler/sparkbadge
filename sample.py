# This is a sample script of how the package might be used.
from typing import Any, Iterator
import requests
from itertools import islice
import tempfile
from sparkbadge import *
from pybadges import badge


class Observer:
    """Simple base observer for printing output."""

    def update(self, data: Any):
        print(data)


class MakeBadge(Observer):
    # TODO: This all should be moved into our package. Proof of concept
    def update(self, data: list[dict]):
        points = [int(x["covered_percent"]) for x in data]
        sparkline = trend(points, "blue", 1)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".svg") as tmpfile:
            tmpfile.write(sparkline)
            tmpfile.flush()

            s = badge(
                center_image=tmpfile.name,
                left_text="Coverage",
                right_text=f"{points[-1]}%",
                center_color="#007ec6",
                embed_center_image=True,
            )
            browser_preview(s)


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
    out.update(recents)


if __name__ == "__main__":
    url = "https://coveralls.io/github/kctraveler/github-actions.json"
    run(get_data(url), MakeBadge())
    # run(get_data(url), Observer())
