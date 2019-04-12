# Feature-Scraper

Scraper designed to extract features of interest from webpages.

## Repo Setup and Management

### Install/Setup
In a Linux environment with Python 3 installed simply run `./setup.bash` and an `app` directory will be created and a virtual python environment launched. If the script is giving an error or for instruction to install in a Windows environment, then please consult the [Scrapy installation instructions](https://docs.scrapy.org/en/latest/intro/install.html).

## Running the Crawler

### Using the Virtual Environment

Python 3 provides a built-in module for creating isolated development environments [venv](https://docs.python.org/3/library/venv.html). We will use this module to manage the project's dependencies. To launch the virtual environment navigate to the `app` directory then execute `source ./bin/activate`. To exit the virtual environment simply enter the `deactivate` command.

### Running a Crawler

To run a crawler:

1. Launch the virtual environment in the `app` directory.
1. Navigate to the `app/features` directory and execute `scrapy list` to see the list of crawlers available to run.
1. Run a crawler by executing `scrapy crawl <name-of-crawler>`

### Controlling the Feature Crawler

The feature crawler is controlled by two files:

#### Controlling Where to Scrape with `app/features/urls.csv`
This file contains a single column with a header of `url` which contains the `url` to be scraped.
- `app/features/config.json`: This file contains a description of the features for which the crawler will look.

#### Controlling What is Extracted with `app/features/config.json`

##### Content
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