import json
from pathlib import Path

skip_ids = {
    '1':  True,
    '55': True,
    '62': True,
    '65': True,
    '69': True,
    '79': True,
}

parent_types = {
    'chapter',
}

leaf_types = {
    'symptom',
    'clinicalFinding',
    'complaint',
    'infection',
    'neoplasm',
    'trauma',
    'congenital',
    'otherDiagnosis',
}

skip_property_kinds = {
    'viewer',       # Some unknown number. Depth?
    'comment',      # On submitting this record.
    'sdg',          # Sustainable development goal.
    'shortTitle',   # A lot of over-shortened trash.
    'ichi',         # Not found useful.
    'icf',          # Not found useful.

    'hasExtension',             # Minor sub-classifications
    'extension_preferred',
    'extension_description',
}

dict_ = {}
root_id = 'root'
ancestor_ids = [root_id]


def process_recursive(id, dict_, current_ancestor_ids):
    for item in get_list_by_id(id):
        id = str(item.get('id', ''))
        type_ = item.get('type', '')
        children = item.get('children', False)
        processed_item = None

        if not children:
            processed_item = leaf_to_dict(id)
        else:
            if id in skip_ids: continue
            if type_ == 'chapter':
                processed_item = chapter_to_dict(item)

        if type_ in parent_types:
            children_ancestor_ids = current_ancestor_ids + [id]
        else:
            children_ancestor_ids = current_ancestor_ids

        if processed_item != None:
            processed_item['parentId'] = current_ancestor_ids[-1]
            processed_item['ancestorIds'] = current_ancestor_ids
            processed_item['type'] = type_

            title = processed_item.get('title', '')
            if title == '':
                processed_item['title'] = cut_code_from_title(item['text'])

            dict_[id] = processed_item
    

        if children:
            process_recursive(id, dict_, children_ancestor_ids)


def get_list_by_id(id):
    filename = id_to_filename(id)
    content = Path(filename).read_text().replace('\n', '')
    return json.loads(content)


def id_to_filename(id):
    return 'downloaded/' + id + '.json'


def chapter_to_dict(item):
    return {}


def cut_code_from_title(title):
    return title.split(' ', 1)[1].strip()


def leaf_to_dict(id):
    title = ''
    description = ''
    inclusion = []
    exclusion = []
    indexwords = []
    icpc1 = []
    icpc1nl = []
    icpc2 = []
    icd10 = []
    icd11 = []
    snomed_ct = []
    uhc = []
    gbd = []
    dsmv = []
    codinghint = ''
    note = ''

    for property_ in get_list_by_id(id):
        kind = property_.get('kind', '')
        label = property_['label'].strip()

        if kind == 'preferred':
            title = label
        elif kind == 'description':
            description = label
        elif kind == 'inclusion':
            inclusion.append(cut_trailing_html(label))
        elif kind == 'exclusion':
            exclusion.append(cut_trailing_html(label))
        elif kind == 'indexwords':
            indexwords.append(label)
        elif kind == 'icpc-1':
            icpc1.append(label)
        elif kind == 'icpc-1nl':
            icpc1nl.append(label)
        elif kind == 'icpc-2':
            icpc2.append(label)
        elif kind == 'icd10':
            icd10.append(label)
        elif kind == 'icd11':
            icd11.append(label)
        elif kind == 'snomed-CT':
            snomed_ct.append(label)
        elif kind == 'uhc':
            uhc.append(label)
        elif kind == 'gbd':
            gbd.append(label)
        elif kind == 'dsm-v':
            dsmv.append(label)
        elif kind == 'codinghint':
            codinghint = label
        elif kind == 'note':
            note = label
        elif kind in skip_property_kinds:
            pass
        else:
            raise ValueError('Unknown record kind: ' + kind + ' in ' + id)

    result = {
        'title':        title,
        'description':  description,
    }

    if len(inclusion):      result['inclusion']     = inclusion
    if len(exclusion):      result['exclusion']     = exclusion
    if len(indexwords):     result['indexWords']    = indexwords
    if len(icpc1):          result['icpc1']         = icpc1
    if len(icpc1nl):        result['icpc1nl']       = icpc1nl
    if len(icpc2):          result['icpc2']         = icpc2
    if len(icd10):          result['icd10']         = icd10
    if len(icd11):          result['icd11']         = icd11
    if len(snomed_ct):      result['snomedCt']      = snomed_ct
    if len(uhc):            result['uhc']           = uhc
    if len(gbd):            result['gbd']           = gbd
    if len(dsmv):           result['dsmV']          = dsmv

    return result


def cut_trailing_html(str):
    return str.split('<', 1)[0].strip()


process_recursive(root_id, dict_, ancestor_ids)
print(json.dumps(dict_))
