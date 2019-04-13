# Feature-Scraper

Scraper designed to extract features of interest from webpages.

- [Install/Setup](#install/setup)
- [Running a Local Webserer for Testing](#running-a-local-webserver-for-testing)
- [Running a Generic Crawler](#running-a-generic-crawler)
  - [Using the Virtual Environment](#using-the-virtual-environment)
  - [Running a Crawler](#running-a-crawler)
- [Running the Feature Crawler](#running-the-feature-crawler)
  - [Controlling Where to Scrape with `app/features/urls.csv`](#controlling-where-to-scrape-with-app/features/urls.csv)
  - [Controlling What is Extracted with `app/features/config.json`](#controlling-what-is-extracted-with-app/features/config.json)
    - [Content Extraction](#content-extraction)
    - [Custom Extraction](#custom-extraction)
    - [Page Grab](#page-grab)
      - [Page Grab Output](#page-grab-output)

## Install/Setup
In a Linux environment with Python 3 installed simply run `./setup.bash` and a virtual python environment will be created and launached from the `app`. If the script is giving an error or for instructions to install in a Windows environment, then please consult the [Scrapy installation instructions](https://docs.scrapy.org/en/latest/intro/install.html).

## Running a Local Webserver for Testing
The tutorials in the Scrapy documenation use [http://quotes.toscrape.com/](http://quotes.toscrape.com/); however, if you want to test the crawler on pages with different structures or content, then you can follow the steps below:
- Place the `HTML` files you want to use to test the crawler in the `server` directory
- Execute the `server.bash` script to run the webserver included in the Python 3 virtual environment from the `server` directory.

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

#### Content Extraction
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

#### Custom Extraction
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

#### Page Grab
It is possible to grab the entire contents of the page. To do so, use the the `"page_grab"` property.
```json
{
    "page_grab": {
        "enabled": true,
        "output_dir": "./pageGrabOutput",
        "header_encoding": "utf-8"
    }
}
```
- The `"enabled"` property controls if pages are grabbed.
- The `"output_dir"` property controls in which the pages are output.
- The headers of the HTTP response headers are byte arrays, so the `"header_encoding"` property is used to specify what encoding should be used for the headers

##### Page Grab Output
Each page grab will have a cooresponding directory created in `"output_dir"`. To avoid problems with long directory/path names the directories will be named `0000` through `9999`. In each directory, there will be 2 files:
- **`response_body.*`**: Since the body of the response could be quite large, it is saved in its own file named either `response_body.byte`, `response_body.txt`, `response_body.html`, or `response_body.xml` depending on the format of the response received. The extension used is given in `crawler.response_extension` in `response_meta.json`.
- **`response_meta.json`**: Contains meta-data about the response which was received by the crawler _(an example is shown below)_. See the Scrapy documentation for [Response](https://docs.scrapy.org/en/latest/topics/request-response.html#response-objects) objects to see definitions for the properties in the `"http"` and `"scrapy"` objects.
    ```json
    {
    "http": {
        "response_url": "http://127.0.0.1:8000/",
        "status": 200,
        "headers": {
        "Server": [
            "SimpleHTTP/0.6 Python/3.6.7"
        ],
        "Date": [
            "Sat, 13 Apr 2019 18:42:48 GMT"
        ],
        "Content-Type": [
            "text/html"
        ],
        "Last-Modified": [
            "Fri, 12 Apr 2019 19:42:00 GMT"
        ]
        }
    },
    "scrapy": {
        "flags": [],
        "encoding": "cp1252"
    },
    "crawler": {
        "response_extension": "html",
        "response_has_text": true
    }
    }
    ```
- **`request_meta.json`**: Contains meta-data about the request which was sent by the crawler _(an example is shown below)_. See the Scrapy documentation for [Request](https://docs.scrapy.org/en/latest/topics/request-response.html#request-objects) objects to see definitions for the properties in the `"http"` and `"scrapy"` objects.
    ```json
    {
    "http": {
        "url": "http://127.0.0.1:8000/",
        "method": "GET",
        "headers": {
        "Accept": [
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        ],
        "Accept-Language": [
            "en"
        ],
        "User-Agent": [
            "Scrapy/1.6.0 (+https://scrapy.org)"
        ],
        "Accept-Encoding": [
            "gzip,deflate"
        ]
        }
    },
    "scrapy": {
        "meta": {
        "download_timeout": 180.0,
        "download_slot": "127.0.0.1",
        "download_latency": 0.0026607513427734375,
        "depth": 0
        }
    }
    }
    ```