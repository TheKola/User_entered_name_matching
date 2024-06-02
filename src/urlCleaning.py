import pandas as pd
import time

def removing_schema(urls):
    urls['Cleaned_homepage_domain'] = urls['url'].apply(lambda x: x.split("://")[-1] if isinstance(x, str) else x)
    return urls

def removing_subdomain(urls):
    '''
     This code not only removes the subdomain but also corrects it, for example there are a lot of urls say wwwwabcd.com
    '''
    urls['Cleaned_homepage_domain'] = urls['Cleaned_homepage_domain'].apply(lambda x: x.split("www.")[-1].replace("www", "") if isinstance(x, str) else x)
    return urls

def removing_subdirectory(urls):
    urls['Cleaned_homepage_domain'] = urls['Cleaned_homepage_domain'].apply(lambda x: x.split("/")[0] if isinstance(x, str) else x)
    return urls

def main():
    start_time = time.time()  # Start time
    urls = pd.read_csv("data/names_numbers_domain.csv")
    '''
    The names_numbers_domain.csv file is from the February 2024 database and the columns are ["CompanyNumber","CompanyName","url"]
    '''

    urls = removing_schema(urls)
    urls = removing_subdomain(urls)

    # Saving the modified DataFrame back to the same CSV file
    urls.to_csv("data/results/url_cleaning_results.csv", index=False)

    end_time = time.time()  # End time
    total_time = end_time - start_time
    total_time_minutes = total_time / 60  # Convert seconds to minutes
    print(f"Total time taken: {total_time_minutes:.3f} minutes")

if __name__ == "__main__":
    main()
