import os
import glob
import pandas as pd


# Important remove punctuation " from all the files usimg: sed -i.bak '/"/d' *


data_path = '/home/stirunag/pre-trained_word_embeddings/PMC n-grams/'

os.chdir(data_path)

extension = 'tsv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]


#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f, sep='\t', error_bad_lines=False) for f in all_filenames ])

appended_data = []
for f in all_filenames:
    print(f)
    temp_ = pd.read_csv(all_filenames[0], sep='\t', error_bad_lines=False, names = ['words', 'year', 'freq', 'papers'], header =None)
    temp_['TF'] = temp_['freq'] * temp_['papers']
    temp = temp_[['words','TF']]

    appended_data.append(temp)
    appended_data = pd.concat(appended_data)
    appended_data = appended_data.groupby(['words'], as_index=False).agg('sum')



#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')


