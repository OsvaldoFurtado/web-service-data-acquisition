########
Overview
########

This project is a CLI application that grab data from a a RESTful web service.


Example of command: python src/acquire.py -o quartet -k ~/Downloads/kaggle.json \ -z carlmcbrideellis/data-anscombes-quartet

-o quartet : specifies a directory into which four results are written. These will have names like quartet/series_1.json.
-k kaggle.json : name of a file with the username and Kaggle API token.
-z : provides the “reference” — the owner and data set name — to open and extract. This information is found by examining the details of the Kaggle interface.