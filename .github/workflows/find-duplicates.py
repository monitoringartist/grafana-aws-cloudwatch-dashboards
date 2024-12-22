import requests

# Naive detection of plain dashboard duplicates on https://grafana.com/grafana/dashboards?dataSource=cloudwatch

url="https://grafana.com/api/dashboards?orderBy=name&direction=asc&includeLogo=0&page=1&pageSize=1000&dataSourceSlugIn=cloudwatch"

def downloadDashboard(d):
  resp = requests.get(url="https://grafana.com/api/dashboards/" + str(i['id']) + "/revisions/" + str(i['revision']) + "/download")
  return resp.json()

def normalizeDashboard(d):
  keys = ['__inputs','__requires','annotations','description','editable','gnetId','iteration','links','refresh','schemaVersion','style','tags','templating','time','timepicket','timezone','title','uid','version']
  for k in keys:
    if k in d:
      del(d[k])
  '''
  i = 0
  pkeys = ['datasource','fieldConfig','fillGradient','hiddenSeries','legend','pluginVersion','timeRegions']
  for p in d['panels']:
    for pk in pkeys:
      if pk in d['panels'][i]:
        del(d['panels'][i][pk])
    i = i + 1
  '''
  return d

resp = requests.get(url=url)
data = resp.json()

monDashboards = {}
nonMonDashboards = []
for i in data["items"]:
  if i['orgSlug'] == 'monitoringartist':
    monDashboards[i['name'].lower().strip()] = normalizeDashboard(downloadDashboard(i))
  else:
    nonMonDashboards.append(i)

for i in nonMonDashboards:
  if i['name'].lower().strip() in monDashboards:
    if normalizeDashboard(downloadDashboard(i)) == monDashboards[i['name'].lower().strip()]:
      print("Found a copy: " + str(i['id']) + " - " + i['name'] + " by " + i['orgName'])
