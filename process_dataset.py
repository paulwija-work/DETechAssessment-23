import pandas as pd
import datetime
import os 
import re
import hashlib

# Clearing up prefix and suffix from name
def prefix_n_suffix_cleanse(name):
    prefix_c = re.sub('^(mr|mrs|miss|dr).{0,1} ' ,'', name.lower())
    c_name= re.sub(' (jr|sr)(.*)$' ,'', prefix_c)
    split_name = c_name.split()
    if len(split_name) > 2:
        f_name,l_name,suffix = split_name
        return f_name.capitalize(),l_name.capitalize()
    f_name,l_name = split_name
    return f_name.capitalize(),l_name.capitalize()

# Formating the date according to YYYYMMDD
# Assumption made 
# 1) that data is not clean and structured  
# 2) day is always be the first 2 digit unless the other 2 digits exceed 12
# 3) invalidated date might occur e.g 30th Feb so we assign a none value and will be treated as
# an another unsuccessful applicant
def format_date(dob):
    day,month,year = None,None,None
    c_dob_split = re.sub(r'(\.|\-|\/)',' ',dob).split()
    for x in c_dob_split:
        if len(x) >= 4:
            year = int(x)
        elif int(x) > 12 and day:
            month = day
            day = int(x)
        elif day and not month:
            month = int(x)
        else:
            day = int(x)
    try:
        c_dob = datetime.date(year,month,day)
        return c_dob,year
    except ValueError:
        return None, year

# creating hash for the member id
def membership_generation(l_name,dob):
    dob_string = f'{re.sub(r"-","",str(dob))}'.encode('utf-8')
    hash_string = hashlib.sha256(dob_string)
    return f'{l_name}_{hash_string.hexdigest()[:5]}'

def main():
    # spcified years when Adults as of 1 Jan 2022
    specific_year = 2022
    adult_year = specific_year - 18
    # processing all csv files in input_dataset folder for easier tracking
    for root, dirs, files in os.walk("input_dataset", topdown=False):
        for name in files:
            dataset = pd.read_csv(f'{root}/{name}')

            # Saving the original columns value in order to create csv of unsuccessful applicants
            original_columns = dataset.columns
            dataset['c_dob'],dataset['dob_year'] = zip(*dataset['date_of_birth'].map(format_date))

            # filtering out the unsuccessful applicants based on email, phone number, age
            # and date of birth
            c_dataset = dataset[
            (dataset['email'].str.contains('.*@.*(\.com|\.net)')) 
            & (dataset['mobile_no'].str.len() == 8 )
            & (dataset['dob_year'] <= adult_year)
            & (dataset['name'].notnull())
            & (dataset['c_dob'].notnull())
            ]

            c_dataset['f_name'],c_dataset['l_name'] = zip(*c_dataset['name'].map(prefix_n_suffix_cleanse))
            c_dataset['above_18'] = True

            c_dataset['member_id'] = c_dataset.apply(lambda x: membership_generation(x.l_name, x.c_dob), axis=1)
            c_dataset.to_csv((f'success_dataset/{name}'), index=False)

            # filtering out the unsuccessful applicants and dumping it as a csv file
            #  so that it can be tracked if needed
            merge_df = pd.merge(dataset,c_dataset,left_index=True, right_index=True, how='outer',
            indicator=True, suffixes=('', '_y'))
            merge_df = merge_df.query('_merge != "both"')[original_columns]
            merge_df.to_csv((f'reject_dataset/{name}'), index=False)

if __name__ == '__main__':
    main()