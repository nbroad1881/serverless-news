# Using serverless platform to regularly log news headlines


Using [serverless framework](serverless.com) to deploy an AWS lambda function that routinely looks for news headlines about 2020 presidential candidates and logs them in an AWS RDS.


Part of my [Sentimentr](sentimentr.nmbroad.com) project.

## How it works
1. CloudWatch event triggers lambda function every hour
2. Lambda function uses [NewsApi](http://newsapi.org/) to get recent headlines.
3. Headlines get sent to an AWS RDS via SQLAlchemy 