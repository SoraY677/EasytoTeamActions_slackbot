import os
from boto.s3.connection import S3Connection
s3 = S3Connection(os.environ['SLACKBOT_API'])