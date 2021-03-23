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

## `nimue`?

All of the example steps use `valohai/nimue` Docker images to transfer and run the Spark application. `nimue` 
(https://hub.docker.com/repository/docker/valohai/nimue) is a data lake proxy developed by Valohai
for packaging and executing Spark applications on on-demand clusters.

If using Docker Hub as the image source is not feasible for your workflow, you may pull a `nimue` image and host it on 
a registry of your choosing.

You may later update the used `nimue` version by changing the step `image:` definition 
e.g. from `valohai/nimue:0.1.0` to `valohai/nimue:0.1.1`

Currently `nimue` only supports on-demand AWS EMR clusters.

## Help!

If you have any questions or want guidance, ask your designated Valohai support personnel. 
We are more than happy to help!

[vh]: https://valohai.com/
