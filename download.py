import json
import requests
from pathlib import Path

start_url = 'https://browser.icpc-3.info/browse.php?operation=getClasses&id='

group_url_template = 'https://browser.icpc-3.info/browse.php?operation=getClasses&id=__ID__'
leaf_url_template = 'https://browser.icpc-3.info/browse.php?operation=getRubrics&id=__ID__'


def query_recursive(url, id):
    print('Downloading ' + url)
    response = requests.get(url)
    response_list = json.loads(response.content)

    with open('downloaded/' + id + '.json', 'wb') as f:
        f.write(response.content)

    for item in response_list:
        id = str(item.get('id', ''))
        type_ = item.get('type', '')
        children = item.get('children', False)

        if children:
            url = group_url_template.replace('__ID__', id)
            query_recursive(url, id)
        else:
            url = leaf_url_template.replace('__ID__', id)
            query_leaf(url, id)
            

def query_leaf(url, id):
    print('Downloading ' + url)
    response = requests.get(url)
    
    with open('downloaded/' + id + '.json', 'wb') as f:
        f.write(response.content)


Path('downloaded').mkdir(parents=True, exist_ok=True)
query_recursive(start_url, 'root');
