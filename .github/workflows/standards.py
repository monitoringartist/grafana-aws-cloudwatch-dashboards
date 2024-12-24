import os
import json
import re

validated_dashboards = [
   "aws-api-gateway/aws-api-gateway.json",
   "aws-autoscaling/aws-autoscaling.json",
   "aws-billing/aws-billing.json",
   "aws-certificate-manager/aws-certificate-manager.json",
   "aws-cloudfront/aws-cloudfront.json",
   "aws-cloudwatch-synthetics/aws-cloudwatch-synthetics.json",
   "aws-cloudwatch-usage-metrics/aws-cloudwatch-usage-metrics.json",
   "aws-codebuild/aws-codebuild.json",
   "aws-cognito/aws-cognito.json",
   "aws-direct-connect/aws-direct-connect.json",
   "aws-dynamodb/aws-dynamodb.json",
   "aws-ebs/aws-ebs.json",
   "aws-ec2/aws-ec2.json"
]

standard_footer = "<a target=\"_blank\" href=\"http://www.monitoringartist.com\" title=\"Dashboard maintained by Monitoring Artist - DevOps / Docker / Kubernetes / AWS ECS / Google GCP / Zabbix / Zenoss / Terraform / Monitoring\"><img src=\"https://monitoringartist.github.io/monitoring-artist-logo-grafana.png\" height=\"30px\" /></a> | \n<a target=\"_blank\" href=\"https://docs.aws.amazon.com/transfer/latest/userguide/monitoring.html\">AWS CloudWatch Transfer Family documentation</a> | \n<a target=\"_blank\" href=\"https://grafana.com/dashboards/20008\">Installed from Grafana.com dashboards</a>"
standard_footer = re.sub(r'https://docs.aws.amazon.com/.*\"', r'https://docs.aws.amazon.com/\"', standard_footer)
standard_footer = re.sub(r'>AWS CloudWatch .* documentation</a', r'>AWS CloudWatch documentation</a', standard_footer)
standard_footer = re.sub(r'https://grafana.com/dashboards/.+\"', r'https://grafana.com/dashboards/n\"', standard_footer)
standard_footer = standard_footer.replace('\n', '')

def validate_template(f, template):
    if "datasource" in template and "uid" in template["datasource"] and template["datasource"]["uid"] != "$datasource":
        print('Dashboard ' + f + ' - variable: ' + template['name'] + ' doesn\'t use $datasource variable')   

def validate_panel(f, panel):
    if "datasource" in panel and "uid" in panel["datasource"] and panel["datasource"]["uid"] != "$datasource":
        print('Dashboard ' + f + ' - panel: ' + panel['title'] + ' doesn\'t use $datasource variable')
    if "targets" in panel:
        for target in panel["targets"]:
            if "datasource" in target and "uid" in target["datasource"] and target["datasource"]["uid"] != "$datasource":
                print('Dashboard ' + f + ' - panel: ' + panel['title'] + ' doesn\'t use $datasource variable')
    if "fieldConfig" in panel and "defaults" in panel["fieldConfig"] and "custom" in panel["fieldConfig"]["defaults"] and "lineWidth" in panel["fieldConfig"]["defaults"]["custom"] and panel["fieldConfig"]["defaults"]["custom"] ["lineWidth"] != 1:
        print('Dashboard ' + f + ' - panel: ' + panel['title'] + ' doesn\'t use lineWidth = 1')
    if "options" in panel and "legend" in panel["options"] and "calcs" in  panel["options"]["legend"] and "lastNotNull" in panel["options"]["legend"]["calcs"]:
        print('Dashboard ' + f + ' - panel: ' + panel['title'] + ' has lastNotNull in the legend')

def validate_config(f, dashboard):
    if 'panels' in dashboard:
        for panel in dashboard['panels']:
            validate_panel(f, panel)
    ## TODO if 'rows' in dashboard:
    if "templating" in dashboard:
        for template in dashboard['templating']:
            validate_template(f, template)
    if "editable" in dashboard and dashboard["editable"] != False:
        print('Dashboard ' + f + ' is editable=true')
    if dashboard["tags"] != ["monitoringartist","cloudwatch"]:
        print('Dashboard ' + f + ' is missing tags "monitoringartist","cloudwatch"')

def validate_inputs(f, dashboard):
    if len(dashboard["__inputs"]) > 0:
        print('Dashboard ' + f + ' doesn\'t have empty __inputs') 

def validate_schema_version(f, dashboard):
    if dashboard["schemaVersion"] < 40:
        print('Dashboard ' + f + ' schemaVersion is lower than 40, migrate it') 

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
    if f not in validated_dashboards:
       continue
    print(f + " validating ...")
    dashboard = json.loads(j.read())
    validate_title(f, dashboard)
    validate_footer(f, dashboard)
    validate_schema_version(f, dashboard)
    validate_inputs(f, dashboard)
    validate_config(f, dashboard)
