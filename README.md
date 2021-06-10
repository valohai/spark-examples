# Valohai Spark Examples

This repository contains examples how to integrate Apache Spark with [Valohai MLOps platform][vh].

The examples are Spark applications of increasing complexity:

* `debug.py` prints debugging information about the runtime to the cluster logs.
* `pi.py` estimates pi and saves a simple data frame to `--output` e.g. to a AWS S3 bucket.

## Running the examples

### Running the examples locally

All of the applications can be ran locally for trying them out:

```bash
pip install -r requirements.txt
python debug.py
```

### Running the examples on Valohai

To run the examples on Valohai requires little AWS setup.

First, create AWS IAM user (with `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID`) containing the following permissions, 
but be sure to edit the `Resource` scoping for your use-case.

* `arn:aws:iam::*:role/EMR_*` matches to the default AWS EMR roles created by `aws emr create-default-roles` command.
   Edit this resource scope if your clusters are using non-default AWS IAM roles.
* `arn:aws:s3:::valohai-emr-*` is the payload bucket that is used for both cluster logs and transferring 
   the Spark application to the cluster. Using the wildcard is common, then you can specify e.g. 
   `valohai-emr-<company-name>` in your executions. If the bucket does not exist, we will create it.
   Note that this is **not** the actual buckets hosting processed datasets, those should be accessible by 
   the above `EMR_` roles assigned to the cluster.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "elasticmapreduce:DescribeStep",
                "elasticmapreduce:ListSteps",
                "elasticmapreduce:ListClusters",
                "elasticmapreduce:AddJobFlowSteps",
                "elasticmapreduce:DescribeCluster",
                "elasticmapreduce:RunJobFlow",
                "elasticmapreduce:TerminateJobFlows",
                "elasticmapreduce:CancelSteps"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:GetRole",
                "iam:PassRole"
            ],
            "Resource": [
                "arn:aws:iam::*:role/EMR_*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:PutBucketPublicAccessBlock",
                "s3:ListBucket",
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::valohai-emr-*",
                "arn:aws:s3:::valohai-emr-*/*"
            ]
        }
    ]
}
```

After that is done, make sure to record `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for later.

Next, import and run the examples on Valohai:

```
 1. Login to Valohai
 2. Click "Create new project"
 3. Configure the project to your liking.
 4. Go to "Settings > Repository"
 5. Use URL: "https://github.com/valohai/spark-examples"
 6. Click "Save"
 7. Click "Fetch repository"
 8. Go to "Settings > Environment Variables" and define the following:
    * `AWS_DEFAULT_REGION`, the region to host both your payload bucket and the cluster
    * `AWS_ACCESS_KEY_ID`, the access key ID to the AWS IAM user we created before
    * `AWS_SECRET_ACCESS_KEY`, marked as a secret, the secret key to the AWS IAM user we created before
 9. Click "Create execution"
10. Select "run-debug-with-minimal-configuration" step.
11. Configure the "bucket" parameter e.g. `valohai-emr-<company-name>`.
12. Click "Create execution".
```

Now it will take anything from 5 to 20 minutes for the execution to finish, mostly depending on the AWS EMR scaling.

Although you can see logs that the Spark application has been completed, 
AWS EMR logs are not automatically transmitted to the execution
but you can see them through the usual AWS EMR interface. 

## Running your own Spark applications 

You can learn how to run your own Spark applications on Valohai by reading the accompanied `valohai.yaml` definitions.

Step named `run-debug-with-maximal-configuration` has the most amount of information about the optional configuration
but `run-debug-with-minimal-configuration` is a much easier starting point to make your own Spark applications 
run on Valohai.

All of the example steps use `valohai/nimue` Docker images to transfer and run the Spark application. `nimue` 
(https://hub.docker.com/repository/docker/valohai/nimue) is a data lake proxy developed by Valohai
for packaging and executing Spark applications on on-demand clusters.

Here are the descriptions of all available command-line arguments:

```
  --payload-bucket PAYLOAD_BUCKET
      (str, required) AWS S3 bucket name to store the application payload and logs 
      e.g. valohai-emr-my-company
  --app-directory APP_DIRECTORY
      (str, required) The root directory that has your application, e.g. /valohai/repository
  --app-main APP_MAIN   
      (str, required) The Python script relative to "app_directory" e.g. spark/extract.py
  --app-requirements APP_REQUIREMENTS
      (str, required) The requirements-file relative to "app_directory" for dependencies 
      e.g. requirements.txt
  --service-role SERVICE_ROLE
      (str, required) Service role to pass to AWS EMR e.g. EMR_DefaultRole
  --instance-role INSTANCE_ROLE
      (str, required) Instance role to pass to AWS EMR e.g. EMR_EC2_DefaultRole
  --release-label RELEASE_LABEL
      (str, required) The AWS EMR release label for big data software versions e.g. emr-6.2.0
  --cluster-applications [CLUSTER_APPLICATIONS [CLUSTER_APPLICATIONS ...]]
      (List[str], required) Comma-separated list of software to preinstall e.g. Hadoop,Hive,Spark
  --configurations CONFIGURATIONS
      (str, default=) Path to the AWS EMR "configurations" JSON file, supports wildcards 
      with * and will use the first matching file e.g. file://path/to/conf.json 
      or file://my/configurations/*.json
  --master-instance-type MASTER_INSTANCE_TYPE
      (str, required) AWS instance type for the master node e.g. m5.xlarge
  --master-security-group MASTER_SECURITY_GROUP
      (str, default=) Optional AWS security group ID for the master node e.g. sg-12312313123123123
  --slave-instance-type SLAVE_INSTANCE_TYPE
      (str, required) AWS instance type for the slave nodes e.g. m5.xlarge
  --slave-security-group SLAVE_SECURITY_GROUP
      (str, default=) Optional AWS security group ID for the slave nodes e.g. sg-12312313123123123
  --instance-count INSTANCE_COUNT
      (int, required) How many total instances to launch in the cluster 
      e.g. 4 means 1 master 3 slaves
  --subnet-id SUBNET_ID
      (str, default=) Optional AWS subnet ID for the nodes e.g. subnet-12341234
  --idle-timeout IDLE_TIMEOUT
      (int, default=1200) Optional minutes do we allow the cluster to be idle before shutdown
  --kill-timeout KILL_TIMEOUT
      (int, default=86400) Optional minutes do we wait for the workload to finish before shutdown
  --tags TAGS           
      (List[Tuple[str, str]], default=[]) Optional comma-separated tags to assign
      e.g. name=circular,company:div=my office
  --python-versions [PYTHON_VERSIONS [PYTHON_VERSIONS ...]]
      (List[str], required) Comma-separated list of Python version to expect on the cluster 
      e.g. 3.6,3.7
```

To pass arguments to your own Spark application, you have two options:

1. add `-pa-<ARGUMENT>` arguments to the call, these "passed arguments" will be forwarded to the Python script
2. add `--` followed by your own arguments; anything past `--` will be forwarded to the Python script unchanged

If using Docker Hub as the image source is not feasible for your workflow, you may pull a `nimue` image and host it on 
a registry of your choosing.

You may later update the used `nimue` version by changing the step `image:` definition 
e.g. from `valohai/nimue:0.1.0` to `valohai/nimue:0.1.1`

Currently `nimue` only supports on-demand AWS EMR clusters.

## Help!

If you have any questions or want guidance, ask your designated Valohai support personnel. 
We are more than happy to help!

[vh]: https://valohai.com/
