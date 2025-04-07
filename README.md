# Web Service Data Acquisition

## Description
This project is a Command Line Interface (CLI) application that extracts data from RESTful web services, specifically from the Kaggle API. The application allows you to download datasets from Kaggle, such as the Anscombe's Quartet example.

## Requirements
- Python 3.11+
- Conda (for environment management)
- pip-tools

## Installation

1. Clone the repository:
```bash
git clone [REPOSITORY-URL]
cd web-service-data-acquisition
```

2. Create and activate the conda environment:
```bash
conda create -n web_dataset python=3.11
conda activate web_dataset
```

3. Install the dependencies:
```bash
pip-sync requirements-dev.txt
```

4. Configure your Kaggle credentials:
   - Access your Kaggle account and download your API file (`kaggle.json`) from your profile
   - Save the `kaggle.json` file in a secure location on your computer

## Usage

### Extract data from Kaggle

To download a dataset from Kaggle:

```bash
python src/acquire.py -o OUTPUT_DIRECTORY -k KAGGLE_JSON_PATH -z DATASET_REFERENCE
```

Parameters:
- `-o`, `--output`: Output directory where data will be saved
- `-k`, `--key`: Path to the Kaggle credentials file (kaggle.json)
- `-z`: Reference to the dataset in the format "owner/dataset-name"
- `-b`, `--baseurl`: Base API URL (optional, default: https://www.kaggle.com)

### Example

```bash
python src/acquire.py -o quartet -k ~/Downloads/kaggle.json -z carlmcbrideellis/data-anscombes-quartet
```

This command:
- Downloads the "data-anscombes-quartet" dataset from user "carlmcbrideellis"
- Uses authentication credentials from the file located at ~/Downloads/kaggle.json
- Saves the results in the "quartet" directory in files such as quartet/series_1.json

## Project Structure

```
.
├── src/                    # Source code
│   ├── __init__.py
│   ├── acquire.py          # Main execution script
│   ├── kaggle_client.py    # Kaggle API client
│   ├── model.py            # Data models
│   └── webpage_client.py   # Web page data extraction client
│
└── tests/                  # Automated tests
    ├── environment.py      # Environment settings for BDD tests
    ├── features/           # BDD (Behavior-Driven Development) scenarios
    │   └── dataset_download.feature
    ├── mock_kaggle_bottle.py   # Mock server using Bottle
    ├── mock_kaggle_server.py   # Mock server using HTTPServer
    ├── steps/              # BDD steps implementation
    │   └── cli_interface.py
    └── test_kaggle_client.py   # Unit tests
```

## Running Tests

This project uses BDD tests with Behave and unit tests with pytest, all managed through tox and Make.

### Run all tests:

```bash
make test
```
### Generate documentation:

```bash
make docs
```

### Clean temporary files:

```bash
make clean
```

## Technology Stack

The project uses the following key technologies:

| Tool | Description |
|------|-------------|
| requests  | HTTP library for API calls |
| beautifulsoup4 | Library for parsing HTML and XML documents |
| pytest | Framework for writing unit tests |
| behave | BDD framework for testing |
| tox | Tool for automating testing in multiple environments |
| pylint |Static code analysis tool |
| sphinx | Documentation generator |
| pip-tools | Dependency management tool |

## Development Notes

- The project uses the `requests` HTTP client by default but implements dependency injection to facilitate testing
- Supports data extraction from ZIP files and HTML pages
- Includes mock servers to test integration with the Kaggle API without making actual requests
