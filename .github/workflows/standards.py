import os
import json
import re

standard_footer = "<a target=\"_blank\" href=\"http://www.monitoringartist.com\" title=\"Dashboard maintained by Monitoring Artist - DevOps / Docker / Kubernetes / AWS ECS / Google GCP / Zabbix / Zenoss / Terraform / Monitoring\"><img src=\"https://monitoringartist.github.io/monitoring-artist-logo-grafana.png\" height=\"30px\" /></a> | \n<a target=\"_blank\" href=\"https://docs.aws.amazon.com/transfer/latest/userguide/monitoring.html\">AWS CloudWatch Transfer Family documentation</a> | \n<a target=\"_blank\" href=\"https://grafana.com/dashboards/20008\">Installed from Grafana.com dashboards</a>\n"
standard_footer = re.sub(r'https://docs.aws.amazon.com/.*\"', r'https://docs.aws.amazon.com/\"', standard_footer)
standard_footer = re.sub(r'>AWS CloudWatch .* documentation</a', r'>AWS CloudWatch documentation</a', standard_footer)
standard_footer = re.sub(r'https://grafana.com/dashboards/.+\"', r'https://grafana.com/dashboards/n\"', standard_footer)
standard_footer = standard_footer.replace('\n', '')

def validate_title(f, dashboard):
  if not dashboard['title'].startswith('AWS '):
    print('Dashboard ' + f + ' title doesn\'t start with \'AWS \' : ' + dashboard['title'])

def validate_footer(f, dashboard):
    if 'rows' in dashboard:
        footer = dashboard['rows'][len(dashboard['rows']) - 1]['panels'][len(dashboard['rows'][len(dashboard['rows']) - 1]['panels']) - 1]
    if 'panels' in dashboard:
        footer = dashboard['panels'][len(dashboard['panels']) - 1]

    if footer['type'] != 'text':
        print('Dashboard ' + f + ' footer is not a text panel')
    if footer['title'] != 'Documentation':
        print('Dashboard ' + f + ' footer title is not \'Documentation\'')
    if 'mode' not in footer:
        if 'mode' in footer['options'] and footer['options']['mode'] != 'html':
            print('Dashboard ' + f + ' footer is not in html mode')
        footer_content = re.sub(r'https://docs.aws.amazon.com/.*\"', r'https://docs.aws.amazon.com/\"', footer['options']['content'])
        footer_content = re.sub(r'>AWS CloudWatch .* documentation</a', r'>AWS CloudWatch documentation</a', footer_content)
        footer_content = re.sub(r'https://grafana.com/dashboards/.+\"', r'https://grafana.com/dashboards/n\"', footer_content)
        footer_content = footer_content.replace('\n', '')
        if footer_content != standard_footer:
            print('Dashboard ' + f + ' footer content is not standard')
            print(footer_content)
            print(standard_footer)
            print("---")
    else:
        if 'mode' in footer and footer['mode'] != 'html':
            print('Dashboard ' + f + ' footer is not in html mode')
        footer_content = re.sub(r'https://docs.aws.amazon.com/.*\"', r'https://docs.aws.amazon.com/\"', footer['content'])
        footer_content = re.sub(r'>AWS CloudWatch .* documentation</a', r'>AWS CloudWatch documentation</a', footer_content)
        footer_content = re.sub(r'https://grafana.com/dashboards/.+\"', r'https://grafana.com/dashboards/n\"', footer_content)
        footer_content = footer_content.replace('\n', '')
        if footer_content != standard_footer:
            print('Dashboard ' + f + ' footer content is not standard')
            print(footer_content)
            print(standard_footer)
            print("---")

directories = [d for d in os.listdir('.') if os.path.isdir(d) and d.startswith('aws')]
json_files = []
for d in directories:
  json_files.extend([d + '/' + f for f in os.listdir(d) if f.endswith('.json')])
jsons = []
for f in json_files:
  with open(f, 'r') as j:
    dashboard = json.loads(j.read())
    validate_title(f, dashboard)
    validate_footer(f, dashboard)
