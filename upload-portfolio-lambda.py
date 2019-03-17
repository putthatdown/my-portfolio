import io
import zipfile
import mimetypes

import boto3

# Get the proper aws-cli profile
wildman = boto3.session.Session(profile_name='wildman')                                                                                                                 
s3 = wildman.resource('s3')

portfolio_bucket = s3.Bucket('portfolio.wildman.ninja')
build_bucket = s3.Bucket('portfoliobuild.wildman.ninja')

portfolio_zip = io.BytesIO() # Python 3.7
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for name in myzip.namelist():
        obj = myzip.open(name)
        portfolio_bucket.upload_fileobj(obj, name,
            ExtraArgs={'ContentType': mimetypes.guess_type(name)[0]})
        portfolio_bucket.Object(name).Acl().put(ACL='public-read')
