import pandas as pd

def get_image_urls(file_path):
    # Load the Excel file
    df = pd.read_excel(file_path, engine='openpyxl')
    # drop duplicated based on Style ID
    df = df.drop_duplicates(subset='Joor Style ID', keep='first')
    # reset the index if desired
    df.reset_index(drop=True, inplace=True)

    # Select needed colummns
    filtered_columns = df.filter(regex='^Style Image URL_\d+$')
    selected_columns = df[['Joor Style ID', 'Style Number', 'Style Name', 'Identifier']]
    df = pd.concat([selected_columns, filtered_columns], axis=1)
    print(df.columns)
    #rename url_columns
    url_columns = df.filter(regex='^Style Image URL').columns

    result_dict = {}
    for _, row in df.iterrows():
        key = f"{row['Identifier']}_{row['Style Number']}"
        value = row[url_columns].dropna().tolist()
        result_dict[key] = value


    return result_dict









