[<img src="https://monitoringartist.github.io/managed-by-monitoringartist.png" alt="Managed by Monitoring Artist: DevOps / Docker / Kubernetes / AWS ECS / Zabbix / Zenoss / Terraform / Monitoring" align="right"/>](http://www.monitoringartist.com 'DevOps / Docker / Kubernetes / AWS ECS / Zabbix / Zenoss / Terraform / Monitoring')

# Grafana dashboards for AWS CloudWatch

Set of AWS Grafana dashboards published on
[grafana.com](https://grafana.com/dashboards?dataSource=cloudwatch) -
100k+ downloads.

Doc:
- [Cloudwatch datasource configuration](https://grafana.com/docs/features/datasources/cloudwatch/)
- [Grafana doc](http://docs.grafana.org/)

Feel free to create pull request for additional AWS resources/printscreens/...

Please set your dashboard variables (`Region, ...`) after dashboard import.
Empty dashboard variables are reason of initial *"Unable to call AWS API" or "Metric request error"* error.

Import all Monitoring Artist AWS dashboards in one go (example script,
`bash/curl/jq` required):

```bash
#!/bin/bash
jq --version >/dev/null 2>&1 || { echo >&2 "I require jq but it's not installed.  Aborting."; exit 1; }
### Please edit grafana_* variables to match your Grafana setup:
grafana_host="http://localhost:3000"
grafana_cred="admin:admin"
# Keep grafana_folder empty for adding the dashboards in "General" folder
grafana_folder="AWS CloudWatch"
ds=(1516 677 139 674 590 659 758 623 617 551 653 969 650 644 607 593 707 575 1519 581 584 2969 8050 11099 11154 11155 12979 13018 13040);
folderId=$(curl -s -k -u "$grafana_cred" $grafana_host/api/folders | jq -r --arg grafana_folder  "$grafana_folder" '.[] | select(.title==$grafana_folder).id')
if [ -z "$folderId" ] ; then echo "Didn't get folderId" ; else echo "Got folderId $folderId" ; fi
for d in "${ds[@]}"; do
  echo -n "Processing $d: "
  j=$(curl -s -k -u "$grafana_cred" $grafana_host/api/gnet/dashboards/$d | jq .json)
  payload="{\"dashboard\":$j,\"overwrite\":true"
  if [ ! -z "$folderId" ] ; then payload="${payload}, \"folderId\": $folderId }";  else payload="${payload} }" ; fi
  curl -s -k -u "$grafana_cred" -XPOST -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    $grafana_host/api/dashboards/import; echo ""
done
```

Use [AWS Policy Generator](http://awspolicygen.s3.amazonaws.com/policygen.html),
which fits your needs. Example of minimal IAM role for Grafana (CloudWatch + EC2 metrics):

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowReadingMetricsFromCloudWatch",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:DescribeAlarmsForMetric",
                "cloudwatch:DescribeAlarmHistory",
                "cloudwatch:DescribeAlarms",
                "cloudwatch:ListMetrics",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:GetMetricData"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AllowReadingTagsInstancesRegionsFromEC2",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeTags",
                "ec2:DescribeInstances",
                "ec2:DescribeRegions"
            ],
            "Resource": "*"
        },
        {
            "Sid": "AllowReadingResourcesForTags",
            "Effect" : "Allow",
            "Action" : "tag:GetResources",
            "Resource" : "*"
        }
    ]
}
```

You can also install this project as a Jsonnet library with [jsonnet-bundler](https://github.com/jsonnet-bundler/jsonnet-bundler):

```shell
$ jb install github.com/monitoringartist/grafana-aws-cloudwatch-dashboards
$ cat > aws-cloudwatch-dashboards.jsonnet <<EOF
local awsCloudWatch = import 'github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/dashboards.libsonnet';

awsCloudWatch.grafanaDashboards
EOF
$ jsonnet -J vendor aws-cloudwatch-dashboards.jsonnet
```

### [AWS API Gateway](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-api-gateway)
[![AWS API Gateway](aws-api-gateway/aws-api-gateway.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-api-gateway)

### [AWS Auto Scaling](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-autoscaling)

### [AWS Billing](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-billing)
[![AWS Billing](aws-billing/aws-billing.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-billing)

### [AWS CloudFront](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-cloudfront)

### [AWS CloudWatch Browser](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-cloudwatch-browser)
[![AWS Cloudwatch Browser](aws-cloudwatch-browser/aws-cloudwatch-browser.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-cloudwatch-browser)

### [AWS CloudWatch Usage Metrics](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-cloudwatch-usage-metrics)
[![AWS Cloudwatch Browser](aws-cloudwatch-usage-metrics/aws-cloudwatch-usage-metrics.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-cloudwatch-usage-metrics)

### [AWS EBS](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-ebs)
[![AWS EBS](aws-ebs/aws-ebs.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-ebs)

### [AWS EC2](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-ec2)
[![AWS EC2](aws-ec2/aws-ec2.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-ec2)

### [AWS ECS](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-ecs)

### [AWS EFS](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-efs)
[![AWS EFS](aws-efs/aws-efs.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-efs)

### [AWS ElastiCache Redis](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-elasticache)
[![AWS ElastiCache Redis](aws-elasticache/aws-elasticache-redis.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-elasticache)

### [AWS ELB Classic Load Balancer](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-elb)
[![AWS ELB Classic Load Balancer](aws-elb/aws-elb-classic-lb.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-elb)

### [AWS ELB Application Load Balancer](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-elb)
[![AWS ELB Application Load Balancer](aws-elb/aws-elb-application-lb.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-elb)

### [AWS EMR Hadoop 2](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-emr)
[![AWS EMR Hadoop 2](aws-emr/aws-emr-hadoop-2.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-emr)

### [AWS Events](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-events)
[![AWS Events](aws-events/aws-events.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-events)

### [AWS Kinesis](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-kinesis)
[![AWS Kinesis](aws-kinesis/aws-kinesis.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-kinesis)

### [AWS Lambda](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-lambda)
[![AWS Lambda](aws-lambda/aws-lambda.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-lambda)

### [AWS Logs](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-logs)
[![AWS Logs](aws-logs/aws-logs.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-logs)

### [AWS CodeBuild](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-codebuild)
[![AWS CodeBuild](aws-codebuild/aws-codebuild.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-codebuild)

### [AWS RDS](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-rds)
[![AWS RDS](aws-rds/aws-rds.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-rds)

### [AWS Redshift](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-redshift)
[![AWS Redshift](aws-redshift/aws-redshift.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-redshift)

### [AWS Route 53](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-route-53)

### [AWS S3](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-s3)
[![AWS S3](aws-s3/aws-s3.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-s3)

### [AWS SES](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-ses)

### [AWS SNS](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-sns)
[![AWS SNS](aws-sns/aws-sns.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-sns)

### [AWS SQS](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-sqs)
[![AWS SQS](aws-sqs/aws-sqs.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-sqs)

### [AWS Step Functions](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-step-functions)
[![AWS SNS](aws-step-functions/aws-step-functions.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-step-functions)

### [AWS Storage Gateway](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-storage-gateway)
[![AWS Storage Gateway](aws-storage-gateway/aws-storage-gateway.png)](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-storage-gateway)

### [AWS VPN](https://github.com/monitoringartist/grafana-aws-cloudwatch-dashboards/tree/master/aws-vpn)

# Author

[Devops Monitoring Expert](http://www.jangaraj.com 'DevOps / Docker / Kubernetes / AWS ECS / Google GCP / Zabbix / Zenoss / Terraform / Monitoring'),
who loves monitoring systems and cutting/bleeding edge technologies: Docker,
Kubernetes, ECS, AWS, Google GCP, Terraform, Lambda, Zabbix, Grafana, Elasticsearch,
Kibana, Prometheus, Sysdig,...

Summary:
* 3000+ [GitHub](https://github.com/monitoringartist/) stars
* 100 000+ [Grafana dashboard](https://grafana.net/monitoringartist) downloads
* 15 000 000+ [Docker images](https://hub.docker.com/u/monitoringartist/) downloads

Professional devops / monitoring / consulting services:

[![Monitoring Artist](http://monitoringartist.com/img/github-monitoring-artist-logo.jpg)](http://www.monitoringartist.com 'DevOps / Docker / Kubernetes / AWS ECS / Google GCP / Zabbix / Zenoss / Terraform / Monitoring')
