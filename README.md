# Fuzzy Match Search for Company Database

## Overview
This project aims to enhance the search functionality for a large database (5 million) of company records by implementing fuzzy string matching. The goal is to provide accurate and quick search results, even when users input incomplete or incorrectly spelled information. The solution also involves cleaning and standardizing URLs in the database.

## Features
- **Fuzzy String Matching:** Handles common errors in user input, such as typos and incomplete names.
- **URL Cleaning:** Standardizes URLs to ensure consistency and improve search accuracy.
- **Pre-Fuzzy Matching:** Prepares the database for efficient fuzzy matching, reducing search times significantly.

## Performance
- **Improved Search Speed:** Reduces search time from 25 seconds to 2 seconds.
- **Large Database Handling:** Efficiently processes and searches within a database of over 5 million company records.

## Project Structure
- `fuzzyMatch.py`: Contains the main code for implementing the fuzzy matching search functionality.
- `preFuzzyMatch.py`: Includes code for pre-processing and standardizing the database to enhance fuzzy matching efficiency.
- `urlCleaning.py`: Contains functions to clean and standardize URLs in the database.

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/TheKola/fuzzy-match-search.git
    ```
2. Navigate to the project directory:
    ```sh
    cd fuzzy-match-search
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Usage
1. **Prepare the Database:**
   Run the `preFuzzyMatch.py` script to standardize and preprocess the database.
    ```sh
    python preFuzzyMatch.py
    ```

2. **Clean URLs:**
   Run the `urlCleaning.py` script to clean and standardize URLs in the database.
    ```sh
    python urlCleaning.py
    ```

3. **Search for Companies:**
   Use the `fuzzyMatch.py` script to search for companies based on user input.
    ```sh
    python fuzzyMatch.py
    ```

### Example
To search for a company, enter the name, number, or URL in the search box, and the script will return the most relevant results, handling typos and incomplete inputs efficiently.

## Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more details.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
This project was developed at The Data City.

