
from ftfy import fix_encoding


def prep(text_prep: str,
        time: str,
        date_format: str,
        ngram: str,
        freq:str,
        stopwords: []):

        import pandas as pd
        from arabica import arabica_freq

        global matrix
        if ngram == 1:
            cool=pd.DataFrame()
            cool = cool.dropna()
            cool['text']=text_prep
            text = text_prep
            cool['time']=time
            cool['time']=cool['time'].astype(str)
            cool['time'] = pd.to_datetime(cool['time'], errors= 'coerce')
            if freq == "Y":
                df = arabica_freq(text = text,
                                  time = time,
                                  date_format = date_format,
                                  time_freq = 'Y',
                                  max_words = 50,
                                  stopwords = stopwords,
                                  skip = None,
                                  numbers = True,
                                  lower_case = True)

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
                df.iloc[:,0] = df.iloc[:,0].apply(fix_encoding)
                total_sum = df.iloc[1:, 1:].sum().sum()
                if total_sum > 15000:
                    # Calculate the scaling factor
                    scaling_factor = 15000 / total_sum
                    # Divide every element in the DataFrame by the scaling factor
                    df.iloc[1:, 1:] = df.iloc[1:, 1:] * scaling_factor


            elif freq == "M":
                df = arabica_freq(text=text,
                                  time=time,
                                  date_format=date_format,
                                  time_freq='M',
                                  max_words=70,
                                  stopwords=stopwords,
                                  skip=None,
                                  numbers=True,
                                  lower_case=True)

                unigram = df[["period", "unigram"]]
                values = unigram["unigram"]
                period = unigram["period"]
                values = values.str.split(pat=',', expand=True)
                period = period.astype(str)
                test = pd.concat([period, values], axis=1)

                colnames = []

                for name in test.columns:
                    name = str(name)
                    name = "word" + name
                    colnames.append(name)

                test.columns = colnames
                test["period"] = test["wordperiod"].rename("period", inplace=True)
                test = test.dropna()
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
                df = pokus.reset_index().pivot_table(values="freq", index="word", columns="period", aggfunc='mean')
                df.reset_index(inplace=True)
                df = df[df['word'] != 'NaT']
                df = df.fillna(0)
                df.rename(columns={df.columns[0]: ' '}, inplace=True)
                df.iloc[:,0] = df.iloc[:,0].apply(fix_encoding)
                total_sum = df.iloc[1:, 1:].sum().sum()
                if total_sum > 15000:
                    # Calculate the scaling factor
                    scaling_factor = 15000 / total_sum
                    # Divide every element in the DataFrame by the scaling factor
                    df.iloc[1:, 1:] = df.iloc[1:, 1:] * scaling_factor

        return df