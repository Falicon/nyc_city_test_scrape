import json
import requests
import slate3k as slate

url = 'https://hhinternet.blob.core.windows.net/wait-times/testing-wait-times.pdf'
data = requests.get(url)
temp = open('temp.pdf', 'wb+')
temp.write(data.content)

with open('temp.pdf', 'rb') as f:
  doc = slate.PDF(f)

content = doc[0]
lines = content.split('\n')

json_data = {
  'refresh_time':'',
  'current_time_window': ''
}

log_refresh = False
log_window = 0
key = ''
for line in lines:
  if log_refresh and json_data['refresh_time'] == '':
    json_data['refresh_time'] = line.strip()
    log_refresh = False

  elif json_data['current_time_window'] == '' and log_window == 2:
    json_data['current_time_window'] = line.strip().replace('|', '')

  elif line.find('Refresh') > -1:
    log_refresh = True

  elif line.find('Current Time Window') > -1 or log_window == 1:
    log_window += 1

  elif json_data['current_time_window'] != '':
    if line.strip() == '':
      pass

    elif key == '':
      key = line.strip()

    else:
      json_data[key] = line.strip()
      key = ''

# write out as a local json file
new_data_file = open('%s_data.json' % json_data['current_time_window'].replace(' ', '_').replace('/', '-'), 'w+')
new_data_file.write(json.dumps(json_data))
