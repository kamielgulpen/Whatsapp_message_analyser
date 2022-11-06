def order_dictionary(dictionary):
    
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}


def get_names(df):

        
    names_tmp = df.name.value_counts().rename_axis('unique_values').reset_index(name='counts')

    names = names_tmp[names_tmp['counts'] > 10].unique_values.to_list()

    return names
