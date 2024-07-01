import pandas as pd
import time

from rapidfuzz import process, fuzz

exact_match = pd.DataFrame()
potential_match = pd.DataFrame()

def convert_to_dict(tuple_list):
    dictionary = {}
    for tup in tuple_list:
        key = tup[2]
        value = tup[1]  
        dictionary[key] = value 
    
    return dictionary

def combining_dict(dict_1,dict_2,dict_3):
    result = {key: max(dict_1.get(key, 0), dict_2.get(key, 0), dict_3.get(key, 0)) for key in dict_1.keys() | dict_2.keys() | dict_3.keys() }
    return result

def cleaning_input(name):
        name = name.split("://")[-1] # Remove Schema
        name = name.split("www.")[-1].replace("www", "") # Remove Subdomain
        name = name.split("/")[0] # Remove sub directory
        name = name.replace(" ", "").lower()

        with open("data/tld.txt", "r") as tld_file:
            tlds = [line.strip() for line in tld_file]
        
        for tld in tlds:
            if name.endswith(tld):
                    # Remove TLD and update the 'fuzzy_homepage_domain'
                    name = name[:-len(tld)]
                    break

        return name

def main():
    company_info = pd.read_csv("data/results/preFuzzyMatch_result.csv")
    '''
    [CompanyNumber,CompanyName,url,Cleaned_homepage_domain,fuzzy_company_name,fuzzy_homepage_domain]
    '''
    print(f"Total number of entries: {len(company_info)}")

    company_numbers = company_info['fuzzy_company_number'].values.tolist()
    company_names = company_info['fuzzy_company_name'].values.tolist()
    urls = company_info['fuzzy_homepage_domain'].values.tolist()

    user_inputs = pd.read_csv("data/test.csv")

    if 'id' not in user_inputs.columns:
        user_inputs.insert(0, 'id', range(1, 1 + len(user_inputs)))

    results = []

    for ind in user_inputs.index:
        exact_match = pd.DataFrame()
        potential_match = pd.DataFrame()
        score_100_flag = False

        input_id = user_inputs['id'][ind]
        input_name = user_inputs['company_name'][ind].replace('"','')

        from_search = time.time()

        cleaned_name = cleaning_input(input_name)

        companynumbers_result = process.extract(cleaned_name, company_numbers, scorer=fuzz.ratio, processor=None, limit=100, score_cutoff=70)
        companynames_result = process.extract(cleaned_name, company_names, scorer=fuzz.ratio, processor=None, limit=100, score_cutoff=70)
        urls_result = process.extract(cleaned_name, urls, scorer=fuzz.ratio, processor=None, limit=100, score_cutoff=70)

        companynumbers_dict = convert_to_dict(companynumbers_result)
        companynames_dict = convert_to_dict(companynames_result)
        urls_dict = convert_to_dict(urls_result)

        combined_dict = combining_dict(companynumbers_dict,companynames_dict,urls_dict)
        # combined_dict = sorted(combined_dict.items(), key=lambda x: x[1], reverse=True)
        
        for index, score in combined_dict.items():
            if score == 100:
                # print(company_info.loc[[index], ['CompanyNumber','CompanyName','url']].to_string(header=False)) # Takes 18 seconds
                exact_match = pd.concat([exact_match, company_info.loc[[index]]])
                score_100_flag = True
            else:
                temp = company_info.loc[[index]].copy()
                temp['score'] = score
                potential_match = pd.concat([potential_match, temp])

        if score_100_flag == True:
            print(exact_match[['CompanyNumber', 'CompanyName', 'url']])
            matches = exact_match['CompanyName'].astype(str).tolist() # Change to save comapny name/ number
        else:
            if not potential_match.empty:
                potential_match = potential_match.sort_values('score', ascending=False)
                highest_score = potential_match['CompanyName'].iloc[0]
                matches = potential_match['CompanyName'].astype(str).tolist() # Change to save comapny name/ number
                # print(f"Did you mean {highest_score}?")
                # print("-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
                # print(potential_match[['CompanyNumber', 'CompanyName', 'url']])
            # else:
                # print("No potential matches found.")
        
        execution_time = time.time() - from_search
        results.append({'id': input_id, 'matches': ', '.join(matches), 'time_taken': execution_time})

        # print(f"Execution time after entering the search: {(time.time() - from_search) :.3f} seconds")
    
    result_df = pd.DataFrame(results)
    user_inputs = user_inputs.merge(result_df, on='id', how='left')
    user_inputs.to_csv("data/test.csv", index=False)

if __name__ == "__main__":
    main()

