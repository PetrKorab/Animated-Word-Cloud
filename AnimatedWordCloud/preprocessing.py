from ftfy import fix_encoding as fix_encoding_function
import re
import numpy as np
import pandas as pd


# Function to split a column by a specified delimiter
def split_string(s):
    return pd.Series(str(s).split(':'))


# Function to rename all columns
def rename_columns(df, prefix='col_'):
    new_columns = [prefix + str(i) for i in range(len(df.columns))]
    return df.rename(columns=dict(zip(df.columns, new_columns)))


def replace_commas_after_integer(s):
    return re.sub(r'(\d+),', r'\1+', s)


def remove_punct(text):
    import string
    import re
    
    # First, remove long sequences of dashes (which might be converted to x)
    # This catches patterns like "--------------------"
    text = re.sub(r'-{2,}', ' ', text)  # Replace 2 or more dashes with space
    
    # Define additional characters to remove beyond standard punctuation
    chars_to_remove = '/–—°…«»-'
    
    # Combine standard punctuation with additional characters
    all_chars_to_remove = string.punctuation + chars_to_remove
    
    # Replace punctuation characters with spaces
    for char in all_chars_to_remove:
        text = text.replace(char, '')
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text



def prep(text_prep: str,
         time: str,
         date_format: str,
         max_words: int,
         ngram: str,
         freq:str,
         stopwords: [],
         skip: [],
         numbers: bool = True,
         punct: bool = True,
         fix_encoding: bool = False):


    import pandas as pd
    from arabica import arabica_freq
    import string

    # Remove _x000D_\\n string from text
    text_prep = text_prep.apply(lambda x: x.replace('_x000D_\\n', ' ') if isinstance(x, str) else x)
    text_prep = text_prep.apply(lambda x: x.replace('x000D_\n', ' ') if isinstance(x, str) else x)

    # Clean punctuation if requested
    if punct:
        print("  → Removing punctuation from text...")
        # Remove punctuation from text_prep using custom function
        text_prep = text_prep.apply(lambda x: remove_punct(x) if isinstance(x, str) else x)

    print(f"  → Preprocessing {ngram}-grams with {freq} frequency...")


    
    global matrix
    if ngram == 1:
        print("  → Building dataframe...")
        cool=pd.DataFrame()
        cool['text']=text_prep
        text = text_prep
        cool['time']=time
        cool['time']=cool['time'].astype(str)
        cool['time'] = pd.to_datetime(cool['time'], errors= 'coerce')

        if freq == "Y":
            print("  → Running arabica_freq (this may take a while)...")
            df = arabica_freq(text = text,
                              time = time,
                              date_format = date_format,
                              time_freq = 'Y',
                              max_words = max_words,
                              stopwords = stopwords,
                              skip = skip if skip else [],
                              numbers = numbers,
                              lower_case = False)

            print("  → Processing unigrams...")

            unigram = df[["period", "unigram"]]
            values = unigram["unigram"]
            period = unigram["period"]
            values = values.str.split(pat=',',expand=True)
            period = period.astype(str)
            test = pd.concat([period, values], axis=1)

            colnames = []

            for name in test.columns:
                name = str(name)
                name = "word" + name
                colnames.append(name)

            test.columns = colnames
            test["period"] = test["wordperiod"].rename("period", inplace = True)
            test=test.iloc[:,1:]
            l = test.melt(id_vars = "period")
            l = l[["period","value"]]
            l = test.melt(id_vars = "period")
            l = l[["period","value"]]
            l.columns = ["period", "word"]
            freq = l["word"].str.split(pat = ":", expand = True)
            freq.columns = ["word", "freq"]
            period = l["period"]
            freq.columns = ["word", "freq"]
            pokus = pd.concat([period, freq],axis=1)
            df = pokus.reset_index().pivot_table(values="freq", index="word", columns="period", aggfunc='mean')
            df.reset_index(inplace=True)
            df = df[df['word'] != 'NaT']
            df = df.fillna(0)
            df.rename(columns={df.columns[0]: ' '}, inplace=True)
            if fix_encoding:
                df.iloc[:,0] = df.iloc[:,0].apply(fix_encoding_function)
            # Clip values
  
            max_freq_per_period = df.iloc[:, 1:].max().max()
            sum_value = df.iloc[:, 1:].sum().sum()
 
            df.to_excel("words_yearly_before_clipping.xlsx", index=False)
            T = len(df.columns) - 1
            Max_word_freq_period_allowed = 150      # Adjusted maximum frequency
            Min_word_freq_period_allowed = 25
            Min_word_freq_period = 20               # Adjusted minimum frequency
            const_max = 3
            const_min = 5
            words_allowed = 400 * T 
            actual_words = df.iloc[:, 1:].sum().sum()

            if max_freq_per_period > Max_word_freq_period_allowed:
                coefficient = actual_words / words_allowed
                df.iloc[:, 1:] = df.iloc[:, 1:] / coefficient

                max_value_clip = df.iloc[:, 1:].max().max()
                print(f"  → Maximum frequency before clipping: {max_freq_per_period}")
                print(f"  → Maximum frequency after clipping: {max_value_clip}")
                print(f"  → Sum of all frequencies before clipping: {sum_value}")            
                print(f"  → Max words_allowed: {words_allowed}")
                print(f"  → Actual_words: {actual_words}")

                df.iloc[:, 1:] = np.where(df.iloc[:, 1:] > 130, 150, df.iloc[:, 1:])

                # Save data with statistics sheet
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words', 'Coefficient'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words, coefficient]
                })
                with pd.ExcelWriter("words_yearly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)


            elif max_freq_per_period < Min_word_freq_period:
                df.iloc[:, 1:] = df.iloc[:, 1:] * const_min
                max_value_clip = df.iloc[:, 1:].max().max()
                print(f"  → Maximum frequency before clipping: {max_freq_per_period}")
                print(f"  → Maximum frequency after clipping: {max_value_clip}")
                print(f"  → Sum of all frequencies before clipping: {sum_value}")            
                print(f"  → Max words_allowed: {words_allowed}")
                print(f"  → Actual_words: {actual_words}")    

                # Save data with statistics sheet
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words]
                })
                with pd.ExcelWriter("words_yearly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)

            else:
                # No clipping needed
                coefficient = None
                max_value_clip = None
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words', 'Coefficient'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words, coefficient]
                })
                with pd.ExcelWriter("words_yearly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            
            # Filter out words with 0 frequency across all periods
            df = df[df.iloc[:, 1:].sum(axis=1) > 0]
            print(f"  → Filtered words with 0 frequency. Remaining words: {len(df)}")


        elif freq == "M":
            print("  → Running arabica_freq for monthly data (this may take a while)...")
            df = arabica_freq(text=text,
                              time=time,
                              date_format=date_format,
                              time_freq='M',
                              max_words=max_words,
                              stopwords=stopwords,
                              skip=skip,
                              numbers=numbers,
                              lower_case=False)
            
            print("  → Arabica_freq complete, processing results...")
            print(f"DEBUG 1: Arabica output - unique periods: {df['period'].unique()}")
            print(f"DEBUG 1: Number of periods from arabica: {len(df['period'].unique())}")

            print("  → Reshaping unigram data...")

            unigram = df[["period", "unigram"]]
            values = unigram["unigram"]
            period = unigram["period"]
            values = values.str.split(pat=',', expand=True)
            period = period.astype(str)
            test = pd.concat([period, values], axis=1)

            print("  → Preparing column names...")
            colnames = []

            for name in test.columns:
                name = str(name)
                name = "word" + name
                colnames.append(name)

            print("  → Melting and pivoting data...")
            test.columns = colnames
            test["period"] = test["wordperiod"].rename("period", inplace=True)
            
            print(f"DEBUG 2: Before dropna - unique periods: {test['period'].unique()}")
            print(f"DEBUG 2: Shape before dropna: {test.shape}")
            
            test = test.dropna(how='all')
            
            print(f"DEBUG 3: After dropna - unique periods: {test['period'].unique()}")
            print(f"DEBUG 3: Shape after dropna: {test.shape}")
            
            test = test.iloc[:, 1:]
            l = test.melt(id_vars="period")
            l = l[["period", "value"]]
            l = test.melt(id_vars="period")
            l = l[["period", "value"]]
            l.columns = ["period", "word"]
            freq = l["word"].str.split(pat=":", expand=True)
            freq.columns = ["word", "freq"]
            print("freq")
            period = l["period"]
            freq.columns = ["word", "freq"]
            pokus = pd.concat([period, freq], axis=1)
            
            print(f"DEBUG 4: Before pivot - unique periods: {pokus['period'].unique()}")
            
            df = pokus.reset_index().pivot_table(values="freq", index="word", columns="period", aggfunc='mean')
            df.reset_index(inplace=True)
            
            print(f"DEBUG 5: After pivot - columns: {df.columns.tolist()}")
            print(f"DEBUG 5: Number of date columns: {len(df.columns) - 1}")
            
            print("  → Cleaning and formatting data...")
            df = df[df['word'] != 'NaT']
            df = df.fillna(0)
            df.rename(columns={df.columns[0]: ' '}, inplace=True)
            if fix_encoding:
                df.iloc[:,0] = df.iloc[:,0].apply(fix_encoding_function)

            # Normalization            
            max_freq_per_period = df.iloc[:, 1:].max().max()
            sum_value = df.iloc[:, 1:].sum().sum()
 
            df.to_excel("words_monthly_before_clipping.xlsx", index=False)
            T = len(df.columns) - 1
            Max_word_freq_period_allowed = 130    # Adjusted maximum frequency for bigrams
            Min_word_freq_period = 25             # Adjusted minimum frequency for bigrams
            const_max = 3
            const_min = 5
            words_allowed = Max_word_freq_period_allowed * const_max * T
            actual_words = df.iloc[:, 1:].sum().sum()

            if max_freq_per_period > Max_word_freq_period_allowed:
            # Normalization: if actual_words > words_allowed, divide all frequencies by coefficient
                coefficient = actual_words / words_allowed
                df.iloc[:, 1:] = df.iloc[:, 1:] / coefficient

                max_value_clip = df.iloc[:, 1:].max().max()
                print(f"  → Maximum frequency before clipping: {max_freq_per_period}")
                print(f"  → Maximum frequency after clipping: {max_value_clip}")
                print(f"  → Sum of all frequencies before clipping: {sum_value}")            
                print(f"  → Max words_allowed: {words_allowed}")
                print(f"  → Actual_words: {actual_words}")

                df.iloc[:, 1:] = np.where(df.iloc[:, 1:] > 130, 150, df.iloc[:, 1:])

                # Save data with statistics sheet
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words', 'Coefficient'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words, coefficient]
                })
                with pd.ExcelWriter("words_monthly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)


            elif max_freq_per_period < Min_word_freq_period:
                df.iloc[:, 1:] = df.iloc[:, 1:] * const_min
                max_value_clip = df.iloc[:, 1:].max().max()
                print(f"  → Maximum frequency before clipping: {max_freq_per_period}")
                print(f"  → Maximum frequency after clipping: {max_value_clip}")
                print(f"  → Sum of all frequencies before clipping: {sum_value}")            
                print(f"  → Max words_allowed: {words_allowed}")
                print(f"  → Actual_words: {actual_words}")    

                # Save data with statistics sheet
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words]
                })
                with pd.ExcelWriter("words_yearly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)


            else:
                # No clipping needed
                coefficient = None
                max_value_clip = None
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words', 'Coefficient'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words, coefficient]
                })
                with pd.ExcelWriter("words_monthly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            
            # Filter out words with 0 frequency across all periods
            df = df[df.iloc[:, 1:].sum(axis=1) > 0]
            print(f"  → Filtered words with 0 frequency. Remaining words: {len(df)}")

                
    elif ngram == 2:
        print("  → Building bigram dataframe...")
        cool=pd.DataFrame()
        cool = cool.dropna()
        cool['text']=text_prep
        text = text_prep
        if fix_encoding:
            text = text.apply(fix_encoding_function)
        cool['time']=time
        cool['time']=cool['time'].astype(str)
        cool['time'] = pd.to_datetime(cool['time'], errors= 'coerce')

        if freq == "Y":
            print("  → Running arabica_freq for yearly bigrams (this may take a while)...")
            df = arabica_freq(text = text,
                              time = time,
                              date_format = date_format,
                              time_freq = 'Y',
                              max_words = max_words,
                              stopwords = stopwords,
                              skip = skip,
                              numbers = numbers,
                              lower_case = False)

            print("  → Processing bigram data...")

            unigram = df[["period", "bigram"]]
            period = pd.DataFrame(unigram["period"])
            unigram["bigram"] = unigram["bigram"].apply(replace_commas_after_integer)
            split_values  = unigram["bigram"].str.split(pat='+', expand=True)
            result = pd.merge(period, split_values, left_index=True, right_index=True)
            new_columns = ['period'] + [f'col_{col}' for col in result.columns[1:]]
            result.columns = new_columns
            finals = pd.wide_to_long(result, ["col_"], i="period", j="year")
            finals = finals.reset_index()
            finals = finals[['period','col_']]
            period_final = finals['period']
            frequencies = finals['col_'].str.split(':', expand=True)
            pokus = pd.merge(period_final, frequencies, left_index=True, right_index=True, suffixes=('', ''))
            pokus.columns = ['period',"word", "freq"]
            pokus['word'] = pokus['word'].str.replace(',', ' ')

            df = pokus.reset_index().pivot_table(values="freq", index="word", columns="period", aggfunc='mean')
            df.reset_index(inplace=True)
            df = df[df['word'] != 'NaT']
            df = df.fillna(0)
            df.rename(columns={df.columns[0]: ' '}, inplace=True)
            if fix_encoding:
                df.iloc[:,0] = df.iloc[:,0].apply(fix_encoding)
            df = pd.DataFrame(df)
            df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

            # Normalization            
            max_freq_per_period = df.iloc[:, 1:].max().max()
            sum_value = df.iloc[:, 1:].sum().sum()
 
            df.to_excel("bigram_yearly_before_clipping.xlsx", index=False)
            T = len(df.columns) - 1
            Max_word_freq_period_allowed = 130      # Adjusted maximum frequency for bigrams
            Min_word_freq_period = 20               # Adjusted minimum frequency for bigrams
            const = 4
            words_allowed = Max_word_freq_period_allowed * const * T
            actual_words = df.iloc[:, 1:].sum().sum()

            if max_freq_per_period > Max_word_freq_period_allowed:
            # Normalization: if actual_words > words_allowed, divide all frequencies by coefficient
                coefficient = actual_words / words_allowed
                df.iloc[:, 1:] = df.iloc[:, 1:] / coefficient

                max_value_clip = df.iloc[:, 1:].max().max()
                print(f"  → Maximum frequency before clipping: {max_freq_per_period}")
                print(f"  → Maximum frequency after clipping: {max_value_clip}")
                print(f"  → Sum of all frequencies before clipping: {sum_value}")            
                print(f"  → Max words_allowed: {words_allowed}")
                print(f"  → Actual_words: {actual_words}")

                df.iloc[:, 1:] = np.where(df.iloc[:, 1:] > 130, 150, df.iloc[:, 1:])

                # Save data with statistics sheet
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words', 'Coefficient'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words, coefficient]
                })
                with pd.ExcelWriter("bigram_yearly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            else:
                # No clipping needed
                coefficient = None
                max_value_clip = None
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words', 'Coefficient'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words, coefficient]
                })
                with pd.ExcelWriter("bigram_yearly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            
            # Filter out words with 0 frequency across all periods
            df = df[df.iloc[:, 1:].sum(axis=1) > 0]
            print(f"  → Filtered words with 0 frequency. Remaining words: {len(df)}")




        elif freq == "M":
            print("  → Running arabica_freq for monthly bigrams (this may take a while)...")
            df = arabica_freq(text = text,
                                  time = time,
                                  date_format = date_format,
                                  time_freq = 'M',
                                  max_words = max_words,
                                  stopwords = stopwords,
                                  skip = skip,
                                  numbers = numbers,
                                  lower_case = False)

            print("  → Processing bigram data...")

            unigram = df[["period", "bigram"]]
            period = pd.DataFrame(unigram["period"])
            unigram["bigram"] = unigram["bigram"].apply(replace_commas_after_integer)
            split_values  = unigram["bigram"].str.split(pat='+', expand=True)
            result = pd.merge(period, split_values, left_index=True, right_index=True)
            new_columns = ['period'] + [f'col_{col}' for col in result.columns[1:]]
            result.columns = new_columns
            finals = pd.wide_to_long(result, ["col_"], i="period", j="year")
            finals = finals.reset_index()
            finals = finals[['period','col_']]
            period_final = finals['period']
            frequencies = finals['col_'].str.split(':', expand=True)
            pokus = pd.merge(period_final, frequencies, left_index=True, right_index=True, suffixes=('', ''))
            pokus.columns = ['period',"word", "freq"]
            pokus['word'] = pokus['word'].str.replace(',', ' ')

            df = pokus.reset_index().pivot_table(values="freq", index="word", columns="period", aggfunc='mean')
            df.reset_index(inplace=True)
            df = df[df['word'] != 'NaT']
            df = df.fillna(0)
            df.rename(columns={df.columns[0]: ' '}, inplace=True)
            if fix_encoding:
                df.iloc[:,0] = df.iloc[:,0].apply(fix_encoding_function)
            
            # Normalization            
            max_freq_per_period = df.iloc[:, 1:].max().max()
            sum_value = df.iloc[:, 1:].sum().sum()
 
            df.to_excel("bigram_monthly_before_clipping.xlsx", index=False)
            T = len(df.columns) - 1
            Max_word_freq_period_allowed = 130      # Adjusted maximum frequency for bigrams
            Min_word_freq_period = 20               # Adjusted minimum frequency for bigrams
            const_max = 3
            const_min = 5
            words_allowed = Max_word_freq_period_allowed * const_max * T
            actual_words = df.iloc[:, 1:].sum().sum()

            if max_freq_per_period > Max_word_freq_period_allowed:
            # Normalization: if actual_words > words_allowed, divide all frequencies by coefficient
                coefficient = actual_words / words_allowed
                df.iloc[:, 1:] = df.iloc[:, 1:] / coefficient

                max_value_clip = df.iloc[:, 1:].max().max()
                print(f"  → Maximum frequency before clipping: {max_freq_per_period}")
                print(f"  → Maximum frequency after clipping: {max_value_clip}")
                print(f"  → Sum of all frequencies before clipping: {sum_value}")            
                print(f"  → Max words_allowed: {words_allowed}")
                print(f"  → Actual_words: {actual_words}")

                df.iloc[:, 1:] = np.where(df.iloc[:, 1:] > 130, 150, df.iloc[:, 1:])

                # Save data with statistics sheet
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words', 'Coefficient'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words, coefficient]
                })
                with pd.ExcelWriter("bigram_monthly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)


            elif max_freq_per_period < Min_word_freq_period:
                df.iloc[:, 1:] = df.iloc[:, 1:] * const_min
                max_value_clip = df.iloc[:, 1:].max().max()
                print(f"  → Maximum frequency before clipping: {max_freq_per_period}")
                print(f"  → Maximum frequency after clipping: {max_value_clip}")
                print(f"  → Sum of all frequencies before clipping: {sum_value}")            
                print(f"  → Max words_allowed: {words_allowed}")
                print(f"  → Actual_words: {actual_words}")    

                # Save data with statistics sheet
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words]
                })
                with pd.ExcelWriter("words_yearly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)

            else:
                # No clipping needed
                coefficient = None
                max_value_clip = None
                stats_df = pd.DataFrame({
                    'Metric': ['Maximum frequency before clipping', 'Maximum frequency after clipping', 
                              'Sum of all frequencies before clipping', 'Max words_allowed', 'Actual_words', 'Coefficient'],
                    'Value': [max_freq_per_period, max_value_clip, sum_value, words_allowed, actual_words, coefficient]
                })
                with pd.ExcelWriter("bigram_monthly_after_clipping.xlsx") as writer:
                    df.to_excel(writer, sheet_name='Data', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            
            # Filter out words with 0 frequency across all periods
            df = df[df.iloc[:, 1:].sum(axis=1) > 0]
            print(f"  → Filtered words with 0 frequency. Remaining words: {len(df)}")

    print("  → Preprocessing complete!")
    return df