"""
Project: Web service Data Acquisition - Kaggle Dataset Downloader
This script downloads and extracts any Kaggle dataset to a specified output directory.
"""

import argparse
import csv
import json
import logging
import os
from pathlib import Path
import sys
import zipfile
from model import *
from kaggle_client import RestAccess

logger = logging.getLogger("acquire")

def get_options(argv: list[str]) -> argparse.Namespace:
    base_url = os.environ.get("ACQUIRE_BASE_URL", "https://www.kaggle.com")
    parser = argparse.ArgumentParser(description="Download and extract Kaggle datasets")
    parser.add_argument("-o", "--output", type=Path, help="Output directory path")
    parser.add_argument("-k", "--key", type=Path, help="Path to Kaggle API credentials JSON file")
    parser.add_argument("-z", "--zip", default="carlmcbrideellis/data-anscombes-quartet",  help="Kaggle dataset reference in format 'username/dataset-name'")
    parser.add_argument("-b", "--baseurl", default=base_url, help="Base URL for Kaggle API")
    parser.add_argument("-e", "--extract", action="store_true", help="Extract all files from zip archive (default: True)")
    parser.add_argument("-s", "--save-zip", action="store_true", help="Save the original zip file (default: False)")
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> None:
    options = get_options(argv or sys.argv[1:])
    
    # Check for required credentials
    if options.key:
        with options.key.open() as key_file:
            credentials = json.load(key_file)
    else:
        logger.error("No credentials file provided on command line.")
        sys.exit(2)

    # Check for output directory
    if not options.output:
        logger.error("No output directory specified. Use -o/--output to specify a directory.")
        sys.exit(2)

    # Ensure output directory exists
    output_dir = options.output
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Output directory: %s", output_dir)
    
    # Setup API access
    access = RestAccess(credentials)
    base_url = options.baseurl
    ref = options.zip
    download_url = f"{base_url}/api/v1/datasets/download/{ref}"
    
    # Download dataset
    logger.info("Downloading dataset: %s", ref)
    try:
        zip_data = access.get_zip(download_url)
    except Exception as e:
        logger.error("Failed to download dataset: %s", e)
        sys.exit(1)
    
    logger.info("Download complete. Total files in archive: %d", len(zip_data.namelist()))
    
    # Save the original zip file if requested
    if options.save_zip:
        zip_output_file = output_dir / f"{ref.replace('/', '_')}.zip"
        logger.info("Saving original zip file to: %s", zip_output_file)
        
        with open(zip_output_file, 'wb') as f:
            zip_data.fp.seek(0)
            f.write(zip_data.fp.read())
    
    # Extract all files by default
    extracted_files = []
    
    # Extract files
    for file_name in zip_data.namelist():
        # Skip directory entries
        if file_name.endswith('/'):
            continue
            
        output_file = output_dir / file_name
        
        # Create parent directories if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info("Extracting: %s", file_name)
        
        with zip_data.open(file_name) as source_file:
            with open(output_file, 'wb') as target_file:
                target_file.write(source_file.read())
        
        extracted_files.append(file_name)
    
    # Log summary
    logger.info("Extraction complete.")
    logger.info("Total files extracted: %d", len(extracted_files))
    logger.info("Extracted files:")
    for idx, file_name in enumerate(extracted_files, 1):
        logger.info("  %d. %s", idx, file_name)
    
    # Generate summary report in the output directory
    summary_file = output_dir / "download_summary.txt"
    with open(summary_file, "w") as f:
        f.write(f"Dataset: {ref}\n")
        f.write(f"Total Files: {len(extracted_files)}\n\n")
        f.write("Files:\n")
        for idx, file_name in enumerate(extracted_files, 1):
            f.write(f"{idx}. {file_name}\n")
    
    logger.info("Summary report saved to: %s", summary_file)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()