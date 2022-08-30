# Near real time AWS DataPipeline (Kinesis Firehose, S3, Lambda and Athena ) deployed w/ Terraform
Project that utilises Kinesis Firehose to ingest data into a S3 data lake, perform some transformations in AWS Lambda Function (to get location based in coordinates) and copy the transformed data in a new layer in s3. This new data can queried by Amazon Athena. Everyhing is deployed as `Infrastructure as Code` using Terraform.

![Alt text](_Diagrama%20AWS%20em%20branco%20(2017).jpeg?raw=true "Title")

## Requirements 
* Install [Terraform](https://releases.hashicorp.com/terraform/1.2.8/terraform_1.2.8_windows_amd64.zip)
* Unzip the file
* Add the directory in which you have download in the PATH from windows
* Install AWSCLI


## Setup 

* Set 2 env variables locally in your machine 
    set AWS_ACCESS_KEY_ID = [your_access_key_id]
    set AWS_SECRET_ACCESS_KEY = [your_access_key_id]
* If you run it in a Docker environement, you can set the environment variables when you run you container:
    docker run --env AWS_ACCESS_KEY_ID = [access_key_id] --env AWS_SECRET_ACCESS_KEY=[secret_key_id] [docker_image_name]    
* run 'aws configure' command and use this variables to set your credentials


* Clone this repository

Change directory within the repository (inside terraform folder) and run 
Terraform init
After that run `Terraform plan`.
And finally run `Terraform apply`. You may be asked to accept the modification with a "yes"
* Based on the definition of the terraform files the whole environment will be created in AWS.
  * [`variables.tf`] 
        This file has some variables that will be used to identify the account, region, pattern of bucket names and some other resources.
  * [`version.tf`]
        This file just identify the version of terraform to aws
  * [`storage.tf`]
        This is a file that will read variables.tf and create all the the buckets and set their permissions.
  * [`kinesis.tf`] 
        This is the file that will performs the creation of ingestion environment in Kinesis 
  * [`lambda.tf`]
        This file create a trigger action that identify all new files in landinzone of S3 environment. After that some transformations are done to enable to deduplicate data and see the correspondent city for each of geo locations (lat and lon). After that, the datetime format it is converted to a readble format as well and then this is saved in another layer called trips-presentation-layer-dev.
  * [`athena.tf`]
        This files create Athena environent. Performs the of a DataCatalog called `AwsDataCatalog`, the creation of a database called `trips_database`, a external table called `trips_tbl`,  and the creation of a view `vwcte`. A query is also created and saved in the environment to select the latest datasource for the two most commonly appearing regions.
  

## How to produce data to kinesis firehose

aws firehose put-record --delivery-stream-name [terraform-kinesis-firehose-test-stream] --record="{\"Data\":\"1\"}"


## How to check if data was created and correctly loaded in S3:

* aws s3 ls

## How to query data in Athena
* Once logged in AWS Console, access Athena, and you can see a table created during the deploy of the environment with Terraaform. You can see a saved query called `query_trips_top_2`. Just open the `AwsDataCatalog` catalog, then open `trips_database` database and then you can run a regular select: `select * from query_trips_top_2;`


