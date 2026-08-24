import json,sys
d = json.load(open('settings_data_current.json'))
before = d['current'].get('logo')
d['current']['logo'] = ""
json.dump(d, open('settings_data.json','w'), indent=2, ensure_ascii=False)
print("logo:", repr(before), "->", repr(d['current']['logo']))
print("keys preserved:", len(d['current']))
