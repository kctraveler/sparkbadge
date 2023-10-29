# This is a sample script of how the package might be used.
import requests


def get_data(url: str):
    """Generator for build coverage data"""
    page = 1
    data = requests.get(url, params={'page': page}).json()
    while page <= data['pages']:
        for build in data['builds']:
            yield build
        page += 1
        data = requests.get(url, params={'page': page}).json()


def main():
    url = "https://coveralls.io/github/kctraveler/github-actions.json"
    main_branches = filter(lambda build: build["branch"] in ["main", "master"],
                           get_data(url))
    parsed_data = map(lambda raw_data: {
        "created_at": raw_data["created_at"],
        "coverage_change": raw_data["coverage_change"],
        "covered_percent": raw_data["covered_percent"]},
        main_branches)

    print(list(parsed_data))


if __name__ == "__main__":
    main()
