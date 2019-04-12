# Feature-Scraper

Scraper designed to extract features of interest from webpages.

## Install/Setup
In a Linux environment with Python 3 installed simply run `./setup.bash` and a virtual python environment will be created and launached from the `app`. If the script is giving an error or for instructions to install in a Windows environment, then please consult the [Scrapy installation instructions](https://docs.scrapy.org/en/latest/intro/install.html).

## Running a Generic Crawler

### Using the Virtual Environment

Python 3 provides a built-in module for creating isolated development environments: [venv](https://docs.python.org/3/library/venv.html). We will use this module to manage the project's dependencies. To launch the virtual environment navigate to the `app` directory then execute `source ./bin/activate`. To exit the virtual environment simply enter the `deactivate` command.

### Running a Crawler

To run a crawler:

1. Launch the virtual environment in the `app` directory.
1. Navigate to the `app/features` directory and execute `scrapy list` to see the list of crawlers available to run.
1. Run a crawler by executing `scrapy crawl <name-of-crawler>`

## Running the Feature Crawler

The feature crawler has two primary stages. The first is the spider which sends requests to `URLs` and parses the raw data from the response. The second stage is a pipeline which process the data extracted from the spider and prepares it of output. The behavior of these stages is primarily controlled through two files: `app/features/urls.csv` and `app/features/config.json`.

### Controlling Where to Scrape with `app/features/urls.csv`
This file contains a single column with a header of `url` which contains the `url` to be scraped.

### Controlling What is Extracted with `app/features/config.json`

#### Content
The crawler can be configured to extract content from a webpage by adding an object to `content_features`. An example of a content feature is shown below:
```json
{
    "content_features": {
        "extract_science_text": {
            "tag": "p",
            "regex": "*science*",
            "mode": "match"
        }
    }
}
```
- The identifier of this content feature is `"extract_sicence_text"` and will be used by the crawler to uniquely identify the feature during runtime and in the crawler's output.
- The `"tag"` property tells the crawler the `HTML` tags whose content should be searched for the `"regex"`.
- The `"regex"` property is used to supply the crawler with a regular expression which the content of the specified `"tag"` must meet to be included in the results.
- The `"mode"` property is used to control how the `"regex"` is applied to the content of the `"tag"`. The supported modes are `"match"` and `"search"`. Please reference the [Python 3 re module documentation](https://docs.python.org/3/library/re.html) for the differences

#### Custom
Custom feature extractors can be added to the crawler for situations which can't be satisfied with existing extractors by adding members to the `custom_features` property.
```json
{
    "custom_features": {
        "title": {
            "xpath_expr": "//title"
        }
    }
}
```
- The identifier of this custom feature is `"title"` and will be used by the crawler to uniquely identify the feature during runtime and in the crawler's output.
- The `"xpath_expr"` is an [XPath](https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-xpaths) expression which is used to extract content from a page for the feature.