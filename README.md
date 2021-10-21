# icpc-3-to-json

These scripts download the ICPC-3 classification and convert it to JSON.

Usage:
```
python3 download.py
python3 downloaded-to-json.py > icpc-3.json
```

This classifier has 3 levels of entities:
- Chapters are top level entities. They can contain only components.
- Components group leafs and separate symptoms from diagnoses. They can contain only leafs.
- Leafs are the payload.

This script ignores auxilary chapters A1, I, II, III, IV, V. These have other levels in structure, may contain dictionaries for properties, and thus should not appear in the tree.

This script imports chapters and leafs ignoring components because they should not appear in search results.


## Firebase Import
In case you want to import this JSON to Firebase, use this:

```bash
npm install -g node-firestore-import-export
firestore-import --accountCredentials credentials.json --backupFile icpc-3.json --nodePath conditions
```

where `credentials.json` is a file you export from Firebase console as per this tutorial: https://www.youtube.com/watch?v=gPzs6t3tQak
