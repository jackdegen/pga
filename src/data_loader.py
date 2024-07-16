import requests
import pandas as pd

from private import DATAGOLF_API_KEY

API_REQUEST = f'https://feeds.datagolf.com/preds/fantasy-projection-defaults?tour=pga&site=draftkings&slate=main&file_format=json&key={DATAGOLF_API_KEY}'

def collapse(list_of_dicts: list[dict[str, float|int|str]]) -> pd.DataFrame:
    """
    Transforms a list of dicts into a single dataframe
    """
    df = (pd
          .DataFrame(data={
              column: [value] for column, value in list_of_dicts[0].items()
          })
         )

    for data_dict in list_of_dicts[1:]:
        df = (pd
              .concat([
                  df,
                  pd.DataFrame(data={
                      column: [value] for column, value in data_dict.items()
                  })
              ])
             )

    return df


def load_data() -> pd.DataFrame:
    """
    Loads in all data from DataGolf projections
    """

    raw = collapse(requests.get(API_REQUEST).json()['projections'])
          
    # raw['name'] = raw['player_name'].map(lambda name_str: ' '.join(name_str.split(', ')[::-1]))

    raw['name'] = raw['site_name_id'].map(lambda name_id: ' '.join(name_id.split(' ')[:-1]))
    raw['id'] = raw['site_name_id'].map(lambda name_id: name_id.split(' ')[-1].replace('(','').replace(')',''))

    raw = (raw
           .set_index('name')
           .drop(['player_name', 'site_name_id'], axis=1)
          )
    return raw