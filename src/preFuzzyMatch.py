import pandas as pd
import time
import re

def cleaning_company_names_and_numbers(company_names_numbers):
    # Remove spaces and convert to lowercase
    company_names_numbers['fuzzy_company_number'] = company_names_numbers['CompanyNumber'].str.replace(' ', '').str.lower()
    company_names_numbers['fuzzy_company_name'] = company_names_numbers['CompanyName'].str.replace(' ', '').str.lower() 
    # company_names['fuzzy_company_name'] = company_names['company_name'].apply(lambda x: re.sub(r'[^a-zA-Z0-9]', '', x).lower()) # Keeps only letters and numbers

    return company_names_numbers

def removing_top_level_domain(urls):
    with open("data/tld.txt", "r") as tld_file:
        tlds = [line.strip() for line in tld_file]

    urls['fuzzy_homepage_domain'] = urls['Cleaned_homepage_domain']

    # Iterate through each row and remove TLD from 'Cleaned_homepage_domain'
    for idx, row in urls.iterrows():
        domain = row['Cleaned_homepage_domain']
        if pd.notna(domain):  # Check if 'domain' is not NaN
            domain = domain.lower()
            for tld in tlds:
                if domain.endswith(tld):
                    # Remove TLD and update the 'fuzzy_homepage_domain'
                    urls.at[idx, 'fuzzy_homepage_domain'] = domain[:-len(tld)]
                    break  # Break the loop after finding and removing the TLD
        else:
            # Optionally handle NaN values, e.g., setting to None or keeping as NaN
            urls.at[idx, 'fuzzy_homepage_domain'] = None

    return urls

def main():
    start_time = time.time()  # Start time
    company_info = pd.read_csv("data/results/url_cleaning_results.csv")

    company_numbers_and_names = cleaning_company_names_and_numbers(company_info)
    urls = removing_top_level_domain(company_numbers_and_names)


    # Saving the modified DataFrame back to the same CSV file
    urls.to_csv("data/results/preFuzzyMatch_result.csv", index=False)

    end_time = time.time()  # End time
    total_time = end_time - start_time
    total_time_minutes = total_time / 60  # Convert seconds to minutes
    print(f"Total time taken: {total_time_minutes:.3f} minutes")

if __name__ == "__main__":
    main()
