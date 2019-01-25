
# Creating static web-sites using AWS S3 Object Storage

You should first have
- installed the awscli package to provide the aws command and also
- configured either
  - the ~/.aws/configure file with your AWS account credentials or
  - created a sourceable ~/.aws/credentials.rc (can be in any location) file

```
> cat ~/.aws/credentials.rc

export AWS_ACCESS_KEY_ID="<your-access-key>"
export AWS_SECRET_ACCESS_KEY="<your-secret-access-key>"
export AWS_DEFAULT_REGION=us-west-1
```

If you have chosen to use an rc file, source it as ```source <your-aws-credentials-rc-file>```, e.g.


```bash
. ~/.aws/credentials
```

We can now use the aws cli utility to access S3 commands.

Let's investigate the available commands with ```aws s3 help```


```bash
aws s3 help 
```

    S3()                                                                      S3()
    
    
    
    NAME
           s3 -
    
    DESCRIPTION
           This  section  explains  prominent concepts and notations in the set of
           high-level S3 commands provided.
    
       Path Argument Type
           Whenever using a command, at least one path argument must be specified.
           There are two types of path arguments: LocalPath and S3Uri.
    
           LocalPath: represents the path of a local file or directory.  It can be
           written as an absolute path or relative path.
    
           S3Uri: represents the location of a S3 object, prefix, or bucket.  This
           must  be  written in the form s3://mybucket/mykey where mybucket is the
           specified S3 bucket, mykey is the specified S3 key.  The path  argument
           must  begin with s3:// in order to denote that the path argument refers
           to a S3 object. Note that prefixes are separated  by  forward  slashes.
           For  example, if the S3 object myobject had the prefix myprefix, the S3
           key would be myprefix/myobject, and if the object  was  in  the  bucket
           mybucket, the S3Uri would be s3://mybucket/myprefix/myobject.
    
       Order of Path Arguments
           Every  command  takes  one or two positional path arguments.  The first
           path argument represents the source, which is the local  file/directory
           or  S3  object/prefix/bucket  that  is being referenced.  If there is a
           second path argument, it represents the destination, which is the local
           file/directory  or  S3  object/prefix/bucket that is being operated on.
           Commands with only one path argument do not have a destination  because
           the operation is being performed only on the source.
    
       Single Local File and S3 Object Operations
           Some  commands  perform operations only on single files and S3 objects.
           The following commands are single file/object operations if no --recur-
           sive flag is provided.
    
              o cp
    
              o mv
    
              o rm
    
           For  this  type of operation, the first path argument, the source, must
           exist and be a local file or S3 object.  The second path argument,  the
           destination,  can  be  the  name  of  a local file, local directory, S3
           object, S3 prefix, or S3 bucket.
    
           The destination is indicated as a local directory,  S3  prefix,  or  S3
           bucket if it ends with a forward slash or back slash.  The use of slash
           depends on the path argument type.  If the path argument  is  a  Local-
           Path,  the type of slash is the separator used by the operating system.
           If the path is a S3Uri, the forward slash must always be  used.   If  a
           slash  is at the end of the destination, the destination file or object
           will adopt the name of the source file or object.  Otherwise, if  there
           is no slash at the end, the file or object will be saved under the name
           provided.  See examples in cp and mv to illustrate this description.
    
       Directory and S3 Prefix Operations
           Some commands only perform operations on the contents of a local direc-
           tory  or  S3 prefix/bucket.  Adding or omitting a forward slash or back
           slash to the end of any path argument, depending on its type, does  not
           affect  the  results  of  the  operation.   The following commands will
           always result in a directory or S3 prefix/bucket operation:
    
           o sync
    
           o mb
    
           o rb
    
           o ls
    
       Use of Exclude and Include Filters
           Currently, there is no support for the use of UNIX style wildcards in a
           command's  path  arguments.   However,  most  commands  have  --exclude
           "<value>" and --include  "<value>"  parameters  that  can  achieve  the
           desired  result.   These  parameters perform pattern matching to either
           exclude or include a particular file or object.  The following  pattern
           symbols are supported.
    
              o *: Matches everything
    
              o ?: Matches any single character
    
              o [sequence]: Matches any character in sequence
    
              o [!sequence]: Matches any character not in sequence
    
           Any  number of these parameters can be passed to a command.  You can do
           this by providing an --exclude or --include  argument  multiple  times,
           e.g.   --include  "*.txt"  --include  "*.png".  When there are multiple
           filters, the rule is the filters that appear later in the command  take
           precedence  over filters that appear earlier in the command.  For exam-
           ple, if the filter parameters passed to the command were
    
              --exclude "*" --include "*.txt"
    
           All files will be excluded from the command  except  for  files  ending
           with  .txt   However, if the order of the filter parameters was changed
           to
    
              --include "*.txt" --exclude "*"
    
           All files will be excluded from the command.
    
           Each filter is evaluated against the source directory.  If  the  source
           location is a file instead of a directory, the directory containing the
           file is used as the source directory.  For example, suppose you had the
           following directory structure:
    
              /tmp/foo/
                .git/
                |---config
                |---description
                foo.txt
                bar.txt
                baz.jpg
    
           In  the  command aws s3 sync /tmp/foo s3://bucket/ the source directory
           is /tmp/foo.  Any include/exclude filters will be  evaluated  with  the
           source  directory prepended.  Below are several examples to demonstrate
           this.
    
           Given the directory structure above and the command aws s3 cp  /tmp/foo
           s3://bucket/  --recursive --exclude ".git/*", the files .git/config and
           .git/description will be excluded from the files to upload because  the
           exclude  filter  .git/*  will  have the source prepended to the filter.
           This means that:
    
              /tmp/foo/.git/* -> /tmp/foo/.git/config       (matches, should exclude)
              /tmp/foo/.git/* -> /tmp/foo/.git/description  (matches, should exclude)
              /tmp/foo/.git/* -> /tmp/foo/foo.txt  (does not match, should include)
              /tmp/foo/.git/* -> /tmp/foo/bar.txt  (does not match, should include)
              /tmp/foo/.git/* -> /tmp/foo/baz.jpg  (does not match, should include)
    
           The command aws s3  cp  /tmp/foo/  s3://bucket/  --recursive  --exclude
           "ba*" will exclude /tmp/foo/bar.txt and /tmp/foo/baz.jpg:
    
              /tmp/foo/ba* -> /tmp/foo/.git/config      (does not match, should include)
              /tmp/foo/ba* -> /tmp/foo/.git/description (does not match, should include)
              /tmp/foo/ba* -> /tmp/foo/foo.txt          (does not match, should include)
              /tmp/foo/ba* -> /tmp/foo/bar.txt  (matches, should exclude)
              /tmp/foo/ba* -> /tmp/foo/baz.jpg  (matches, should exclude)
    
           Note that, by default, all files are included.  This means that provid-
           ing only an --include filter will not  change  what  files  are  trans-
           ferred.   --include  will only re-include files that have been excluded
           from an --exclude filter.  If you only want to upload files with a par-
           ticular extension, you need to first exclude all files, then re-include
           the files with the particular extension.  This command will upload only
           files ending with .jpg:
    
              aws s3 cp /tmp/foo/ s3://bucket/ --recursive --exclude "*" --include "*.jpg"
    
           If  you wanted to include both .jpg files as well as .txt files you can
           run:
    
              aws s3 cp /tmp/foo/ s3://bucket/ --recursive \
                  --exclude "*" --include "*.jpg" --include "*.txt"
    
           See 'aws help' for descriptions of global parameters.
    
    SYNOPSIS
              aws s3 <Command> [<Arg> ...]
    
    OPTIONS
           None
    
           See 'aws help' for descriptions of global parameters.
    
    AVAILABLE COMMANDS
           o cp
    
           o ls
    
           o mb
    
           o mv
    
           o presign
    
           o rb
    
           o rm
    
           o sync
    
           o website
    
    
    
                                                                              S3()


S3 is organized into buckets, each of which contains a hierarchy of named objects.

The bucket name itself must be globally **unique** - across all AWS accounts not just yours.

Let's see if we have any buckets of our own using the ```aws s3 ls``` command.
You won't have any buckets if you just created your account.


```bash
aws s3 ls
```

Let's create our own bucket, we use the 'mb' or *make bucket* command to do this as
    ```aws s3 mb s3://<my-bucket-name>```
    
Note that we always address buckets in URL form ```s3://<bucket>```


```bash
aws s3 mb s3://mybucket
```

    make_bucket failed: s3://mybucket An error occurred (BucketAlreadyExists) when calling the CreateBucket operation: The requested bucket name is not available. The bucket namespace is shared by all users of the system. Please select a different name and try again.




Of course someone got there first with our "mybucket" name !

So create a **unique** name, e.g. for myself:


```bash
aws s3 mb s3://mjbright-static-site
```

    make_bucket: mjbright-static-site



```bash
aws s3 ls
```

    2019-01-25 21:33:37 mjbright-static-site


That was lucky !

Now let's add some files to our bucket.

We can do this with the cp or sync commands.

Let's create an HTML index file and copy this into our bucket.


```bash
mkdir -p website;

cat > website/index.html <<EOF
<html>
<body>
    <h1> My first amazing web site !! </h1>
</body>
</html>
EOF

ls -al website/index.html
```

    -rw-rw-r-- 1 user1 user1 74 Jan 25 21:33 website/index.html



```bash
aws s3 sync ./website s3://mjbright-static-site
```

    upload: website/index.html to s3://mjbright-static-site/index.html



```bash
aws s3 ls s3://mjbright-static-site
```

    2019-01-25 21:33:55         74 index.html


So it seems we have created a static web site.

We can use the handy S3 command website to declare that this is a website.


```bash
aws s3 website s3://mjbright-static-site --index-document index.html
```

The site should be available at http://<bucketname>.s3-website-<region>.amazonaws.com, which in this case would be:
    
    http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/
    
However, if we visit that web page we will get an error telling us that we cannot access the page


```bash
wget -O - http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html
```

    --2019-01-25 21:34:20--  http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html
    Resolving mjbright-static-site.s3-website-us-west-1.amazonaws.com (mjbright-static-site.s3-website-us-west-1.amazonaws.com)... 52.219.24.172
    Connecting to mjbright-static-site.s3-website-us-west-1.amazonaws.com (mjbright-static-site.s3-website-us-west-1.amazonaws.com)|52.219.24.172|:80... connected.
    HTTP request sent, awaiting response... 403 Forbidden
    2019-01-25 21:34:20 ERROR 403: Forbidden.
    




**NOTE**: The following steps using the AWS console can be avoided by

For more information see "awscli enabling of website hosting":  http://notes.webutvikling.org/add-s3-bucket-using-awscli-example/




```bash
BUCKET=mjbright-static-site

# NOT NEEDED AS WE ALREADY CREATED THE BUCKET:
# aws s3api create-bucket --bucket $BUCKET --region us-west-1 --acl public-read --create-bucket-configuration LocationConstraint=us-west-1

# NOT NEEDED as copy already performed:
# aws s3 cp --recursive website/ s3://$BUCKET/

curl https://raw.githubusercontent.com/tomfa/aws-policies/master/s3-bucket-public-read.json > /tmp/s3-bucket-public-read.json

cat /tmp/s3-bucket-public-read.json



```

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100   236  100   236    0     0   1380      0 --:--:-- --:--:-- --:--:--  1380
    {
      "Version":"2012-10-17",
      "Statement":[{
        "Sid":"PublicReadGetObject",
            "Effect":"Allow",
          "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::[[YOUR-BUCKET-NAME]]/*"
          ]
        }
      ]
    }


```bash
sed "s/\[\[YOUR-BUCKET-NAME\]\]/$BUCKET/g" /tmp/s3-bucket-public-read.json > s3.json
cat s3.json
aws s3api put-bucket-policy --bucket $BUCKET --policy file://s3.json
```

    {
      "Version":"2012-10-17",
      "Statement":[{
        "Sid":"PublicReadGetObject",
            "Effect":"Allow",
          "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::mjbright-static-site/*"
          ]
        }
      ]
    }


```bash
http http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html 
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m74[39;49;00m
    [36mContent-Type[39;49;00m: [33mtext/html[39;49;00m
    [36mDate[39;49;00m: [33mFri, 25 Jan 2019 21:41:55 GMT[39;49;00m
    [36mETag[39;49;00m: [33m"a891baebfc13d226edc4eb4e908cf652"[39;49;00m
    [36mLast-Modified[39;49;00m: [33mFri, 25 Jan 2019 21:33:55 GMT[39;49;00m
    [36mServer[39;49;00m: [33mAmazonS3[39;49;00m
    [36mx-amz-id-2[39;49;00m: [33m2kczFb8kdg8e4ecMKLiLFF73Tvy4TVp6uolBH5MdbaNYxeaBjJGSBJbX15iHgQqUjSiEz97+Hig=[39;49;00m
    [36mx-amz-request-id[39;49;00m: [33m463C085A1474ED01[39;49;00m
    
    <[34;01mhtml[39;49;00m>
    <[34;01mbody[39;49;00m>
        <[34;01mh1[39;49;00m> My first amazing web site !! </[34;01mh1[39;49;00m>
    </[34;01mbody[39;49;00m>
    </[34;01mhtml[39;49;00m>
    


**NOTE: THESE GRAPHICAL/CONSOLE STEPS ARE NO LONGER NEEDED IF ABOVE policy commands used**

This information kept here for reference.

If the above request succeeded you can skip to section '**Static-site generators**' below.

_____________________________________________________________________________________________

In fact we first need to enable website hosting from the bucket **and** enable public access to the index.html file.

We can do this via the AWS Console.

Connect to the console with your credentials and then navigate to https://s3.console.aws.amazon.com/s3/buckets/.


![](images/BucketProperties.JPG)

You should see your bucket listed here.

Click on the line (not on the bucket name which is a link, but under the Access or Region column) to see the following dropdown menu

![](images/BucketProperties-BeforeWebHostingEnabled.JPG)

Click on "Enable Web hosting" and you should see:

<!-- ![](images/BucketProperties-Settings-EnableWebsiteHosting.JPG) -->

![](images/BucketProperties-Settings-Enabled_WebsiteHosting.JPG)

But we still cannot access our site as we need to enable public access to the index.html file.

Click on the bucket name to be taken to a list of files in the bucket, select the index.html file and then "*Make Public*" in the dropdown "*Actions*" menu:

![](images/Make_index_public.JPG)

You now should be able to access your site using a browser, or from the command-line:


```bash
http http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m74[39;49;00m
    [36mContent-Type[39;49;00m: [33mtext/html[39;49;00m
    [36mDate[39;49;00m: [33mFri, 25 Jan 2019 21:44:32 GMT[39;49;00m
    [36mETag[39;49;00m: [33m"a891baebfc13d226edc4eb4e908cf652"[39;49;00m
    [36mLast-Modified[39;49;00m: [33mFri, 25 Jan 2019 21:33:55 GMT[39;49;00m
    [36mServer[39;49;00m: [33mAmazonS3[39;49;00m
    [36mx-amz-id-2[39;49;00m: [33mr7BnsjmdWZMO+OwLbaSEIDj8xRfFK7J2EJy6nrLn3ibLjW6rf1DThFNH3LnytA3bpyqRNZ2HDZQ=[39;49;00m
    [36mx-amz-request-id[39;49;00m: [33m6BE5077594B573B8[39;49;00m
    
    <[34;01mhtml[39;49;00m>
    <[34;01mbody[39;49;00m>
        <[34;01mh1[39;49;00m> My first amazing web site !! </[34;01mh1[39;49;00m>
    </[34;01mbody[39;49;00m>
    </[34;01mhtml[39;49;00m>
    


## Static-site generators

Let's now create something a little more like a website.

### 1. Pelican a Python Module
We'll use the Pelican command (installed as a Python module).



```bash
pelican -o PELICAN -q

cp -a PELICAN/* website/

aws s3 sync website/ s3://mjbright-static-site/
```

    Done: Processed 0 articles, 0 drafts, 0 pages, 0 hidden pages and 0 draft pages in 0.07 seconds.
    upload: website/archives.html to s3://mjbright-static-site/archives.html            
    upload: website/images/AWS-SIGNUP.JPG to s3://mjbright-static-site/images/AWS-SIGNUP.JPG
    upload: website/authors.html to s3://mjbright-static-site/authors.html                
    upload: website/categories.html to s3://mjbright-static-site/categories.html          
    upload: website/theme/css/reset.css to s3://mjbright-static-site/theme/css/reset.css
    upload: website/images/BucketProperties-Settings-EnableWebsiteHosting.JPG to s3://mjbright-static-site/images/BucketProperties-Settings-EnableWebsiteHosting.JPG
    upload: website/theme/css/pygment.css to s3://mjbright-static-site/theme/css/pygment.css
    upload: website/images/BucketProperties-Settings-Enabled_WebsiteHosting.JPG to s3://mjbright-static-site/images/BucketProperties-Settings-Enabled_WebsiteHosting.JPG
    upload: website/theme/css/main.css to s3://mjbright-static-site/theme/css/main.css
    upload: website/theme/fonts/Yanone_Kaffeesatz_400.svg to s3://mjbright-static-site/theme/fonts/Yanone_Kaffeesatz_400.svg
    upload: website/feeds/all.atom.xml to s3://mjbright-static-site/feeds/all.atom.xml
    upload: website/index.html to s3://mjbright-static-site/index.html 
    upload: website/tags.html to s3://mjbright-static-site/tags.html   
    upload: website/theme/css/fonts.css to s3://mjbright-static-site/theme/css/fonts.css
    upload: website/theme/fonts/Yanone_Kaffeesatz_400.eot to s3://mjbright-static-site/theme/fonts/Yanone_Kaffeesatz_400.eot
    upload: website/images/BucketProperties.JPG to s3://mjbright-static-site/images/BucketProperties.JPG
    upload: website/theme/css/wide.css to s3://mjbright-static-site/theme/css/wide.css
    upload: website/theme/images/icons/aboutme.png to s3://mjbright-static-site/theme/images/icons/aboutme.png
    upload: website/theme/fonts/font.css to s3://mjbright-static-site/theme/fonts/font.css
    upload: website/images/Make_index_public.JPG to s3://mjbright-static-site/images/Make_index_public.JPG
    upload: website/theme/images/icons/github.png to s3://mjbright-static-site/theme/images/icons/github.png
    upload: website/theme/images/icons/delicious.png to s3://mjbright-static-site/theme/images/icons/delicious.png
    upload: website/theme/fonts/Yanone_Kaffeesatz_400.woff to s3://mjbright-static-site/theme/fonts/Yanone_Kaffeesatz_400.woff
    upload: website/theme/images/icons/facebook.png to s3://mjbright-static-site/theme/images/icons/facebook.png
    upload: website/theme/css/typogrify.css to s3://mjbright-static-site/theme/css/typogrify.css
    upload: website/images/BucketProperties-BeforeWebHostingEnabled.JPG to s3://mjbright-static-site/images/BucketProperties-BeforeWebHostingEnabled.JPG
    upload: website/theme/images/icons/gittip.png to s3://mjbright-static-site/theme/images/icons/gittip.png
    upload: website/theme/images/icons/hackernews.png to s3://mjbright-static-site/theme/images/icons/hackernews.png
    upload: website/theme/fonts/Yanone_Kaffeesatz_400.woff2 to s3://mjbright-static-site/theme/fonts/Yanone_Kaffeesatz_400.woff2
    upload: website/theme/images/icons/google-plus.png to s3://mjbright-static-site/theme/images/icons/google-plus.png
    upload: website/theme/images/icons/bitbucket.png to s3://mjbright-static-site/theme/images/icons/bitbucket.png
    upload: website/theme/images/icons/rss.png to s3://mjbright-static-site/theme/images/icons/rss.png
    upload: website/theme/images/icons/google-groups.png to s3://mjbright-static-site/theme/images/icons/google-groups.png
    upload: website/theme/fonts/Yanone_Kaffeesatz_400.ttf to s3://mjbright-static-site/theme/fonts/Yanone_Kaffeesatz_400.ttf
    upload: website/theme/images/icons/linkedin.png to s3://mjbright-static-site/theme/images/icons/linkedin.png
    upload: website/theme/images/icons/twitter.png to s3://mjbright-static-site/theme/images/icons/twitter.png
    upload: website/theme/images/icons/speakerdeck.png to s3://mjbright-static-site/theme/images/icons/speakerdeck.png
    upload: website/theme/images/icons/stackoverflow.png to s3://mjbright-static-site/theme/images/icons/stackoverflow.png
    upload: website/theme/images/icons/youtube.png to s3://mjbright-static-site/theme/images/icons/youtube.png
    upload: website/theme/images/icons/gitorious.png to s3://mjbright-static-site/theme/images/icons/gitorious.png
    upload: website/theme/images/icons/lastfm.png to s3://mjbright-static-site/theme/images/icons/lastfm.png
    upload: website/theme/images/icons/vimeo.png to s3://mjbright-static-site/theme/images/icons/vimeo.png
    upload: website/theme/images/icons/slideshare.png to s3://mjbright-static-site/theme/images/icons/slideshare.png
    upload: website/theme/images/icons/reddit.png to s3://mjbright-static-site/theme/images/icons/reddit.png


We can now test our new website: using wget, curl or http(ie) or using a browser at http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html


```bash
http http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m1486[39;49;00m
    [36mContent-Type[39;49;00m: [33mtext/html[39;49;00m
    [36mDate[39;49;00m: [33mFri, 25 Jan 2019 21:45:31 GMT[39;49;00m
    [36mETag[39;49;00m: [33m"70ec20e1a2544e5eba9aa224e3b607f6"[39;49;00m
    [36mLast-Modified[39;49;00m: [33mFri, 25 Jan 2019 21:45:19 GMT[39;49;00m
    [36mServer[39;49;00m: [33mAmazonS3[39;49;00m
    [36mx-amz-id-2[39;49;00m: [33mehBTFGAc6bUlc53B7VmUfM+QTJnSn+HN7wU4tXEcERzGM75sVJPZDVXD7BvjjxXqM9MD/rHWhNI=[39;49;00m
    [36mx-amz-request-id[39;49;00m: [33m4026EC8E31BF98D1[39;49;00m
    
    [36m<!DOCTYPE html>[39;49;00m
    <[34;01mhtml[39;49;00m [36mlang[39;49;00m=[33m"en"[39;49;00m>
    <[34;01mhead[39;49;00m>
            <[34;01mmeta[39;49;00m [36mcharset[39;49;00m=[33m"utf-8"[39;49;00m />
            <[34;01mtitle[39;49;00m>A Pelican Blog</[34;01mtitle[39;49;00m>
            <[34;01mlink[39;49;00m [36mrel[39;49;00m=[33m"stylesheet"[39;49;00m [36mhref[39;49;00m=[33m"/theme/css/main.css"[39;49;00m />
            <[34;01mlink[39;49;00m [36mhref[39;49;00m=[33m"/feeds/all.atom.xml"[39;49;00m [36mtype[39;49;00m=[33m"application/atom+xml"[39;49;00m [36mrel[39;49;00m=[33m"alternate"[39;49;00m [36mtitle[39;49;00m=[33m"A Pelican Blog Atom Feed"[39;49;00m />
    </[34;01mhead[39;49;00m>
    
    <[34;01mbody[39;49;00m [36mid[39;49;00m=[33m"index"[39;49;00m [36mclass[39;49;00m=[33m"home"[39;49;00m>
            <[34;01mheader[39;49;00m [36mid[39;49;00m=[33m"banner"[39;49;00m [36mclass[39;49;00m=[33m"body"[39;49;00m>
                    <[34;01mh1[39;49;00m><[34;01ma[39;49;00m [36mhref[39;49;00m=[33m"/"[39;49;00m>A Pelican Blog </[34;01ma[39;49;00m></[34;01mh1[39;49;00m>
                    <[34;01mnav[39;49;00m><[34;01mul[39;49;00m>
                    </[34;01mul[39;49;00m></[34;01mnav[39;49;00m>
            </[34;01mheader[39;49;00m>[37m<!--[39;49;00m[37m /#banner [39;49;00m[37m-->[39;49;00m
    <[34;01msection[39;49;00m [36mid[39;49;00m=[33m"content"[39;49;00m [36mclass[39;49;00m=[33m"body"[39;49;00m>
    <[34;01mh2[39;49;00m>Pages</[34;01mh2[39;49;00m>
    </[34;01msection[39;49;00m>
            <[34;01msection[39;49;00m [36mid[39;49;00m=[33m"extras"[39;49;00m [36mclass[39;49;00m=[33m"body"[39;49;00m>
                    <[34;01mdiv[39;49;00m [36mclass[39;49;00m=[33m"social"[39;49;00m>
                            <[34;01mh2[39;49;00m>social</[34;01mh2[39;49;00m>
                            <[34;01mul[39;49;00m>
                                <[34;01mli[39;49;00m><[34;01ma[39;49;00m [36mhref[39;49;00m=[33m"/feeds/all.atom.xml"[39;49;00m [36mtype[39;49;00m=[33m"application/atom+xml"[39;49;00m [36mrel[39;49;00m=[33m"alternate"[39;49;00m>atom feed</[34;01ma[39;49;00m></[34;01mli[39;49;00m>
    
                            </[34;01mul[39;49;00m>
                    </[34;01mdiv[39;49;00m>[37m<!--[39;49;00m[37m /.social [39;49;00m[37m-->[39;49;00m
            </[34;01msection[39;49;00m>[37m<!--[39;49;00m[37m /#extras [39;49;00m[37m-->[39;49;00m
    
            <[34;01mfooter[39;49;00m [36mid[39;49;00m=[33m"contentinfo"[39;49;00m [36mclass[39;49;00m=[33m"body"[39;49;00m>
                    <[34;01maddress[39;49;00m [36mid[39;49;00m=[33m"about"[39;49;00m [36mclass[39;49;00m=[33m"vcard body"[39;49;00m>
                    Proudly powered by <[34;01ma[39;49;00m [36mhref[39;49;00m=[33m"http://getpelican.com/"[39;49;00m>Pelican</[34;01ma[39;49;00m>, which takes great advantage of <[34;01ma[39;49;00m [36mhref[39;49;00m=[33m"http://python.org"[39;49;00m>Python</[34;01ma[39;49;00m>.
                    </[34;01maddress[39;49;00m>[37m<!--[39;49;00m[37m /#about [39;49;00m[37m-->[39;49;00m
    
                    <[34;01mp[39;49;00m>The theme is by <[34;01ma[39;49;00m [36mhref[39;49;00m=[33m"http://coding.smashingmagazine.com/2009/08/04/designing-a-html-5-layout-from-scratch/"[39;49;00m>Smashing Magazine</[34;01ma[39;49;00m>, thanks!</[34;01mp[39;49;00m>
            </[34;01mfooter[39;49;00m>[37m<!--[39;49;00m[37m /#contentinfo [39;49;00m[37m-->[39;49;00m
    
    </[34;01mbody[39;49;00m>
    </[34;01mhtml[39;49;00m>
    


http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html

### 2. Hugo - a static site generator/CMS written in Go

Let's create a site using Hugo:
```hugo new site <sitename>```


```bash
hugo new site quickstart

cd quickstart
```

    Congratulations! Your new Hugo site is created in /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/quickstart.
    
    Just a few more steps and you're ready to go:
    
    1. Download a theme into the same-named folder.
       Choose a theme from https://themes.gohugo.io/, or
       create your own with the "hugo new theme <THEMENAME>" command.
    2. Perhaps you want to add some content. You can add single files
       with "hugo new <SECTIONNAME>/<FILENAME>.<FORMAT>".
    3. Start the built-in live server via "hugo server".
    
    Visit https://gohugo.io/ for quickstart guide and full documentation.


Now let's install the ananke theme


```bash
git init
git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke
echo 'theme = "ananke"' >> config.toml
```

    Initialized empty Git repository in /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/quickstart/.git/
    Cloning into '/home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/quickstart/themes/ananke'...
    remote: Enumerating objects: 38, done.[K
    remote: Counting objects: 100% (38/38), done.[K
    remote: Compressing objects: 100% (31/31), done.[K
    remote: Total 1234 (delta 16), reused 18 (delta 7), pack-reused 1196[K
    Receiving objects: 100% (1234/1234), 2.61 MiB | 13.72 MiB/s, done.
    Resolving deltas: 100% (656/656), done.


and now
- create the site with this theme
- copy the files into our website directory
- re-sync to our S3 bucket


```bash
pwd
hugo
```

    /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/quickstart
    [K25lBuilding sites … [?25h
                       | EN  
    +------------------+----+
      Pages            |  7  
      Paginator pages  |  0  
      Non-page files   |  0  
      Static files     |  3  
      Processed images |  0  
      Aliases          |  0  
      Sitemaps         |  1  
      Cleaned          |  0  
    
    Total in 8 ms



```bash
ls -al public/
```

    total 40
    drwxrwxr-x  6 user1 user1 4096 Jan 25 21:57 [0m[01;34m.[0m
    drwxrwxr-x 11 user1 user1 4096 Jan 25 21:56 [01;34m..[0m
    -rw-rw-r--  1 user1 user1 2071 Jan 25 21:57 404.html
    drwxrwxr-x  2 user1 user1 4096 Jan 25 21:57 [01;34mcategories[0m
    drwxrwxr-x  4 user1 user1 4096 Jan 25 21:56 [01;34mdist[0m
    drwxrwxr-x  2 user1 user1 4096 Jan 25 21:56 [01;34mimages[0m
    -rw-rw-r--  1 user1 user1 2495 Jan 25 21:57 index.html
    -rw-rw-r--  1 user1 user1  468 Jan 25 21:57 index.xml
    -rw-rw-r--  1 user1 user1  437 Jan 25 21:57 sitemap.xml
    drwxrwxr-x  2 user1 user1 4096 Jan 25 21:57 [01;34mtags[0m



```bash
cd ..

cp -a quickstart/public/* website/
aws s3 sync website/ s3://mjbright-static-site/
```

    upload: website/404.html to s3://mjbright-static-site/404.html                      
    upload: website/categories/index.xml to s3://mjbright-static-site/categories/index.xml
    upload: website/dist/js/app.3fc0f988d21662902933.js to s3://mjbright-static-site/dist/js/app.3fc0f988d21662902933.js
    upload: website/categories/index.html to s3://mjbright-static-site/categories/index.html
    upload: website/tags/index.html to s3://mjbright-static-site/tags/index.html
    upload: website/dist/css/app.955516233bcafa4d2a1c13cea63c7b50.css to s3://mjbright-static-site/dist/css/app.955516233bcafa4d2a1c13cea63c7b50.css
    upload: website/index.html to s3://mjbright-static-site/index.html
    upload: website/index.xml to s3://mjbright-static-site/index.xml  
    upload: website/sitemap.xml to s3://mjbright-static-site/sitemap.xml
    upload: website/images/gohugo-default-sample-hero-image.jpg to s3://mjbright-static-site/images/gohugo-default-sample-hero-image.jpg
    upload: website/tags/index.xml to s3://mjbright-static-site/tags/index.xml


We can now test our new website: using wget, curl or http(ie) or using a browser at http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html


```bash
http http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m2495[39;49;00m
    [36mContent-Type[39;49;00m: [33mtext/html[39;49;00m
    [36mDate[39;49;00m: [33mFri, 25 Jan 2019 21:57:44 GMT[39;49;00m
    [36mETag[39;49;00m: [33m"0e015b35a60e4c5773d0cd12e57b5fc8"[39;49;00m
    [36mLast-Modified[39;49;00m: [33mFri, 25 Jan 2019 21:57:30 GMT[39;49;00m
    [36mServer[39;49;00m: [33mAmazonS3[39;49;00m
    [36mx-amz-id-2[39;49;00m: [33mL/bUXP5g8KE7KJUlX9c4+12xiLGE49MajgayUU3j0ro3LPkaZU2joyzwvlxigZQneoLO8TTyI18=[39;49;00m
    [36mx-amz-request-id[39;49;00m: [33mC392A7553E4EB4CE[39;49;00m
    
    [36m<!DOCTYPE html>[39;49;00m
    <[34;01mhtml[39;49;00m [36mlang[39;49;00m=[33m"en-us"[39;49;00m>
      <[34;01mhead[39;49;00m>
        <[34;01mmeta[39;49;00m [36mcharset[39;49;00m=[33m"utf-8"[39;49;00m>
        <[34;01mmeta[39;49;00m [36mhttp-equiv[39;49;00m=[33m"X-UA-Compatible"[39;49;00m [36mcontent[39;49;00m=[33m"IE=edge,chrome=1"[39;49;00m>
        
        <[34;01mtitle[39;49;00m>My New Hugo Site </[34;01mtitle[39;49;00m>
        <[34;01mmeta[39;49;00m [36mname[39;49;00m=[33m"HandheldFriendly"[39;49;00m [36mcontent[39;49;00m=[33m"True"[39;49;00m>
        <[34;01mmeta[39;49;00m [36mname[39;49;00m=[33m"MobileOptimized"[39;49;00m [36mcontent[39;49;00m=[33m"320"[39;49;00m>
    
        <[34;01mmeta[39;49;00m [36mname[39;49;00m=[33m"viewport"[39;49;00m [36mcontent[39;49;00m=[33m"width=device-width,minimum-scale=1"[39;49;00m>
        <[34;01mmeta[39;49;00m [36mname[39;49;00m=[33m"generator"[39;49;00m [36mcontent[39;49;00m=[33m"Hugo 0.53"[39;49;00m />
        
        
          <[34;01mMETA[39;49;00m [36mNAME[39;49;00m=[33m"ROBOTS"[39;49;00m [36mCONTENT[39;49;00m=[33m"NOINDEX, NOFOLLOW"[39;49;00m>
        
    
        
        
          <[34;01mlink[39;49;00m [36mhref[39;49;00m=[33m"/dist/css/app.955516233bcafa4d2a1c13cea63c7b50.css"[39;49;00m [36mrel[39;49;00m=[33m"stylesheet"[39;49;00m>
        
    
        
    
        
          
        
    
        
          <[34;01mlink[39;49;00m [36mhref[39;49;00m=[33m"http://example.org/index.xml"[39;49;00m [36mrel[39;49;00m=[33m"alternate"[39;49;00m [36mtype[39;49;00m=[33m"application/rss+xml"[39;49;00m [36mtitle[39;49;00m=[33m"My New Hugo Site"[39;49;00m />
          <[34;01mlink[39;49;00m [36mhref[39;49;00m=[33m"http://example.org/index.xml"[39;49;00m [36mrel[39;49;00m=[33m"feed"[39;49;00m [36mtype[39;49;00m=[33m"application/rss+xml"[39;49;00m [36mtitle[39;49;00m=[33m"My New Hugo Site"[39;49;00m />
        
    
        <[34;01mmeta[39;49;00m [36mproperty[39;49;00m=[33m"og:title"[39;49;00m [36mcontent[39;49;00m=[33m"My New Hugo Site"[39;49;00m />
    <[34;01mmeta[39;49;00m [36mproperty[39;49;00m=[33m"og:description"[39;49;00m [36mcontent[39;49;00m=[33m""[39;49;00m />
    <[34;01mmeta[39;49;00m [36mproperty[39;49;00m=[33m"og:type"[39;49;00m [36mcontent[39;49;00m=[33m"website"[39;49;00m />
    <[34;01mmeta[39;49;00m [36mproperty[39;49;00m=[33m"og:url"[39;49;00m [36mcontent[39;49;00m=[33m"http://example.org/"[39;49;00m />
    
    <[34;01mmeta[39;49;00m [36mitemprop[39;49;00m=[33m"name"[39;49;00m [36mcontent[39;49;00m=[33m"My New Hugo Site"[39;49;00m>
    <[34;01mmeta[39;49;00m [36mitemprop[39;49;00m=[33m"description"[39;49;00m [36mcontent[39;49;00m=[33m""[39;49;00m>
    
    <[34;01mmeta[39;49;00m [36mname[39;49;00m=[33m"twitter:card"[39;49;00m [36mcontent[39;49;00m=[33m"summary"[39;49;00m/>
    <[34;01mmeta[39;49;00m [36mname[39;49;00m=[33m"twitter:title"[39;49;00m [36mcontent[39;49;00m=[33m"My New Hugo Site"[39;49;00m/>
    <[34;01mmeta[39;49;00m [36mname[39;49;00m=[33m"twitter:description"[39;49;00m [36mcontent[39;49;00m=[33m""[39;49;00m/>
    
      </[34;01mhead[39;49;00m>
    
      <[34;01mbody[39;49;00m [36mclass[39;49;00m=[33m"ma0 avenir bg-near-white"[39;49;00m>
    
        
    
      <[34;01mheader[39;49;00m>
        <[34;01mdiv[39;49;00m [36mclass[39;49;00m=[33m"pb3-m pb6-l bg-black"[39;49;00m>
          <[34;01mnav[39;49;00m [36mclass[39;49;00m=[33m"pv3 ph3 ph4-ns"[39;49;00m [36mrole[39;49;00m=[33m"navigation"[39;49;00m>
      <[34;01mdiv[39;49;00m [36mclass[39;49;00m=[33m"flex-l justify-between items-center center"[39;49;00m>
        <[34;01ma[39;49;00m [36mhref[39;49;00m=[33m"http://example.org/"[39;49;00m [36mclass[39;49;00m=[33m"f3 fw2 hover-white no-underline white-90 dib"[39;49;00m>
          My New Hugo Site
        </[34;01ma[39;49;00m>
        <[34;01mdiv[39;49;00m [36mclass[39;49;00m=[33m"flex-l items-center"[39;49;00m>
          
    
          
          
    
    
    
    
    
    
    
    
    
        </[34;01mdiv[39;49;00m>
      </[34;01mdiv[39;49;00m>
    </[34;01mnav[39;49;00m>
    
          <[34;01mdiv[39;49;00m [36mclass[39;49;00m=[33m"tc-l pv3 ph3 ph4-ns"[39;49;00m>
            <[34;01mh1[39;49;00m [36mclass[39;49;00m=[33m"f2 f-subheadline-l fw2 light-silver mb0 lh-title"[39;49;00m>
              My New Hugo Site
            </[34;01mh1[39;49;00m>
            
          </[34;01mdiv[39;49;00m>
        </[34;01mdiv[39;49;00m>
      </[34;01mheader[39;49;00m>
    
    
        <[34;01mmain[39;49;00m [36mclass[39;49;00m=[33m"pb7"[39;49;00m [36mrole[39;49;00m=[33m"main"[39;49;00m>
          
      <[34;01marticle[39;49;00m [36mclass[39;49;00m=[33m"cf ph3 ph5-l pv3 pv4-l f4 tc-l center measure-wide lh-copy mid-gray"[39;49;00m>
        
      </[34;01marticle[39;49;00m>
      
      
      
      
      
      
      
    
        </[34;01mmain[39;49;00m>
        <[34;01mfooter[39;49;00m [36mclass[39;49;00m=[33m"bg-black bottom-0 w-100 pa3"[39;49;00m [36mrole[39;49;00m=[33m"contentinfo"[39;49;00m>
      <[34;01mdiv[39;49;00m [36mclass[39;49;00m=[33m"flex justify-between"[39;49;00m>
      <[34;01ma[39;49;00m [36mclass[39;49;00m=[33m"f4 fw4 hover-white no-underline white-70 dn dib-ns pv2 ph3"[39;49;00m [36mhref[39;49;00m=[33m"http://example.org/"[39;49;00m >
        &copy; 2019 My New Hugo Site
      </[34;01ma[39;49;00m>
        <[34;01mdiv[39;49;00m>
    
    
    
    
    
    
    
    
    </[34;01mdiv[39;49;00m>
      </[34;01mdiv[39;49;00m>
    </[34;01mfooter[39;49;00m>
    
        
    
      <[34;01mscript[39;49;00m [36msrc[39;49;00m=[33m"/dist/js/app.3fc0f988d21662902933.js"[39;49;00m></[34;01mscript[39;49;00m>
    
    
      </[34;01mbody[39;49;00m>
    </[34;01mhtml[39;49;00m>
    


Visit http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html

### 3. create-react-app

create-react-app is an npm module created by Facebook allowing to quickly create a skeleton React app.


```bash
create-react-app my-react-app
#cd my-react-app/; npm start
#ls -al my-react-app/public/
```


```bash
cd my-react-app; npm run build
ls -al public/
```

    [?25h[0G[K
    > my-react-app@0.1.0 build /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda/my-react-app
    > react-scripts build
    
    [?25l[0G▀ ╢░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░╟
    [?25h[?25h[1A[0G[K[?25h[0G[KCreating an optimized production build...
    [32mCompiled successfully.[39m
    [32m[39m
    File sizes after gzip:
    
      34.71 KB  [2mbuild/static/js/[22m[36m1.fa92c112.chunk.js[39m
      763 B     [2mbuild/static/js/[22m[36mruntime~main.229c360f.js[39m
      716 B     [2mbuild/static/js/[22m[36mmain.a7b1c78b.chunk.js[39m
      510 B     [2mbuild/static/css/[22m[36mmain.8cc6a47e.chunk.css[39m
    
    The project was built assuming it is hosted at [32mthe server root[39m.
    You can control this with the [32mhomepage[39m field in your [36mpackage.json[39m.
    For example, add this to build it for GitHub Pages:
    
      [32m"homepage"[39m [36m:[39m [32m"http://myname.github.io/myapp"[39m[36m,[39m
    
    The [36mbuild[39m folder is ready to be deployed.
    You may serve it with a static server:
    
      [36mnpm[39m install -g serve
      [36mserve[39m -s build
    
    Find out more about deployment here:
    
      [33mhttp://bit.ly/CRA-deploy[39m
    
    [?25l[0G▀ ╢░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░╟
    [?25h[?25h[1A[0G[K[?25h[0G[Ktotal 20
    drwxrwxr-x 2 user1 user1 4096 Jan 25 22:06 [0m[01;34m.[0m
    drwxrwxr-x 6 user1 user1 4096 Jan 25 22:12 [01;34m..[0m
    -rwxrwxr-x 1 user1 user1 3870 Jan 25 22:06 [01;32mfavicon.ico[0m
    -rwxrwxr-x 1 user1 user1 1586 Jan 25 22:06 [01;32mindex.html[0m
    -rwxrwxr-x 1 user1 user1  306 Jan 25 22:06 [01;32mmanifest.json[0m



```bash
ls -altr build
```

    total 36
    drwxrwxr-x 6 user1 user1 4096 Jan 25 22:12 [0m[01;34m..[0m
    -rwxrwxr-x 1 user1 user1  306 Jan 25 22:13 [01;32mmanifest.json[0m
    -rwxrwxr-x 1 user1 user1 3870 Jan 25 22:13 [01;32mfavicon.ico[0m
    drwxrwxr-x 3 user1 user1 4096 Jan 25 22:13 [01;34m.[0m
    drwxrwxr-x 5 user1 user1 4096 Jan 25 22:13 [01;34mstatic[0m
    -rw-rw-r-- 1 user1 user1 1041 Jan 25 22:13 service-worker.js
    -rw-rw-r-- 1 user1 user1  606 Jan 25 22:13 precache-manifest.16ab4e73d949e217b5bb10bd22a96200.js
    -rw-rw-r-- 1 user1 user1 2062 Jan 25 22:13 index.html
    -rw-rw-r-- 1 user1 user1  779 Jan 25 22:13 asset-manifest.json



```bash
cd ..; pwd
rm -rf website/*
cp -av my-react-app/build/* website/
```

    /home/user1/src/git/ServerlessLabs/ServerlessWorkshop/AWS-S3-Lambda
    'my-react-app/build/asset-manifest.json' -> 'website/asset-manifest.json'
    'my-react-app/build/favicon.ico' -> 'website/favicon.ico'
    'my-react-app/build/index.html' -> 'website/index.html'
    'my-react-app/build/manifest.json' -> 'website/manifest.json'
    'my-react-app/build/precache-manifest.16ab4e73d949e217b5bb10bd22a96200.js' -> 'website/precache-manifest.16ab4e73d949e217b5bb10bd22a96200.js'
    'my-react-app/build/service-worker.js' -> 'website/service-worker.js'
    'my-react-app/build/static' -> 'website/static'
    'my-react-app/build/static/media' -> 'website/static/media'
    'my-react-app/build/static/media/logo.5d5d9eef.svg' -> 'website/static/media/logo.5d5d9eef.svg'
    'my-react-app/build/static/css' -> 'website/static/css'
    'my-react-app/build/static/css/main.8cc6a47e.chunk.css' -> 'website/static/css/main.8cc6a47e.chunk.css'
    'my-react-app/build/static/css/main.8cc6a47e.chunk.css.map' -> 'website/static/css/main.8cc6a47e.chunk.css.map'
    'my-react-app/build/static/js' -> 'website/static/js'
    'my-react-app/build/static/js/main.a7b1c78b.chunk.js' -> 'website/static/js/main.a7b1c78b.chunk.js'
    'my-react-app/build/static/js/1.fa92c112.chunk.js' -> 'website/static/js/1.fa92c112.chunk.js'
    'my-react-app/build/static/js/runtime~main.229c360f.js' -> 'website/static/js/runtime~main.229c360f.js'
    'my-react-app/build/static/js/main.a7b1c78b.chunk.js.map' -> 'website/static/js/main.a7b1c78b.chunk.js.map'
    'my-react-app/build/static/js/1.fa92c112.chunk.js.map' -> 'website/static/js/1.fa92c112.chunk.js.map'
    'my-react-app/build/static/js/runtime~main.229c360f.js.map' -> 'website/static/js/runtime~main.229c360f.js.map'



```bash
aws s3 rm --recursive s3://mjbright-static-site/
```

    delete: s3://mjbright-static-site/manifest.json
    delete: s3://mjbright-static-site/index.html
    delete: s3://mjbright-static-site/favicon.ico



```bash
aws s3 ls s3://mjbright-static-site/
```


```bash
aws s3 sync website/ s3://mjbright-static-site/
```

    upload: website/asset-manifest.json to s3://mjbright-static-site/asset-manifest.json   
    upload: website/precache-manifest.16ab4e73d949e217b5bb10bd22a96200.js to s3://mjbright-static-site/precache-manifest.16ab4e73d949e217b5bb10bd22a96200.js
    upload: website/favicon.ico to s3://mjbright-static-site/favicon.ico                 
    upload: website/static/css/main.8cc6a47e.chunk.css.map to s3://mjbright-static-site/static/css/main.8cc6a47e.chunk.css.map
    upload: website/static/media/logo.5d5d9eef.svg to s3://mjbright-static-site/static/media/logo.5d5d9eef.svg
    upload: website/static/js/main.a7b1c78b.chunk.js.map to s3://mjbright-static-site/static/js/main.a7b1c78b.chunk.js.map
    upload: website/index.html to s3://mjbright-static-site/index.html 
    upload: website/service-worker.js to s3://mjbright-static-site/service-worker.js
    upload: website/static/js/runtime~main.229c360f.js.map to s3://mjbright-static-site/static/js/runtime~main.229c360f.js.map
    upload: website/static/css/main.8cc6a47e.chunk.css to s3://mjbright-static-site/static/css/main.8cc6a47e.chunk.css
    upload: website/manifest.json to s3://mjbright-static-site/manifest.json
    upload: website/static/js/runtime~main.229c360f.js to s3://mjbright-static-site/static/js/runtime~main.229c360f.js
    upload: website/static/js/main.a7b1c78b.chunk.js to s3://mjbright-static-site/static/js/main.a7b1c78b.chunk.js
    upload: website/static/js/1.fa92c112.chunk.js.map to s3://mjbright-static-site/static/js/1.fa92c112.chunk.js.map
    upload: website/static/js/1.fa92c112.chunk.js to s3://mjbright-static-site/static/js/1.fa92c112.chunk.js


We can now test our new website: using wget, curl or http(ie) or using a browser at http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html



```bash
http http://mjbright-static-site.s3-website-us-west-1.amazonaws.com/index.html
```

    /usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.24.1) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    [34mHTTP[39;49;00m/[34m1.1[39;49;00m [34m200[39;49;00m [36mOK[39;49;00m
    [36mContent-Length[39;49;00m: [33m2062[39;49;00m
    [36mContent-Type[39;49;00m: [33mtext/html[39;49;00m
    [36mDate[39;49;00m: [33mFri, 25 Jan 2019 22:15:15 GMT[39;49;00m
    [36mETag[39;49;00m: [33m"7919b1a9089a669e063517d00d7ada31"[39;49;00m
    [36mLast-Modified[39;49;00m: [33mFri, 25 Jan 2019 22:15:11 GMT[39;49;00m
    [36mServer[39;49;00m: [33mAmazonS3[39;49;00m
    [36mx-amz-id-2[39;49;00m: [33m5EIMuAzMksTQxTlEfSa5l6oiCb3YxMHZzEAtZtLAnl1osQt6/G4oQmIaDgpep/4Q65udFtk2P+0=[39;49;00m
    [36mx-amz-request-id[39;49;00m: [33m9483B6104E576BD8[39;49;00m
    
    [36m<!doctype html>[39;49;00m<[34;01mhtml[39;49;00m [36mlang[39;49;00m=[33m"en"[39;49;00m><[34;01mhead[39;49;00m><[34;01mmeta[39;49;00m [36mcharset[39;49;00m=[33m"utf-8"[39;49;00m/><[34;01mlink[39;49;00m [36mrel[39;49;00m=[33m"shortcut icon"[39;49;00m [36mhref[39;49;00m=[33m"/favicon.ico"[39;49;00m/><[34;01mmeta[39;49;00m [36mname[39;49;00m=[33m"viewport"[39;49;00m [36mcontent[39;49;00m=[33m"width=device-width,initial-scale=1,shrink-to-fit=no"[39;49;00m/><[34;01mmeta[39;49;00m [36mname[39;49;00m=[33m"theme-color"[39;49;00m [36mcontent[39;49;00m=[33m"#000000"[39;49;00m/><[34;01mlink[39;49;00m [36mrel[39;49;00m=[33m"manifest"[39;49;00m [36mhref[39;49;00m=[33m"/manifest.json"[39;49;00m/><[34;01mtitle[39;49;00m>React App</[34;01mtitle[39;49;00m><[34;01mlink[39;49;00m [36mhref[39;49;00m=[33m"/static/css/main.8cc6a47e.chunk.css"[39;49;00m [36mrel[39;49;00m=[33m"stylesheet"[39;49;00m></[34;01mhead[39;49;00m><[34;01mbody[39;49;00m><[34;01mnoscript[39;49;00m>You need to enable JavaScript to run this app.</[34;01mnoscript[39;49;00m><[34;01mdiv[39;49;00m [36mid[39;49;00m=[33m"root"[39;49;00m></[34;01mdiv[39;49;00m><[34;01mscript[39;49;00m>![34mfunction[39;49;00m(l){[34mfunction[39;49;00m e(e){[34mfor[39;49;00m([34mvar[39;49;00m r,t,n=e[[34m0[39;49;00m],o=e[[34m1[39;49;00m],u=e[[34m2[39;49;00m],f=[34m0[39;49;00m,i=[];f<n.length;f++)t=n[f],p[t]&&i.push(p[t][[34m0[39;49;00m]),p[t]=[34m0[39;49;00m;[34mfor[39;49;00m(r [34min[39;49;00m o)[36mObject[39;49;00m.prototype.hasOwnProperty.call(o,r)&&(l[r]=o[r]);[34mfor[39;49;00m(s&&s(e);i.length;)i.shift()();[34mreturn[39;49;00m c.push.apply(c,u||[]),a()}[34mfunction[39;49;00m a(){[34mfor[39;49;00m([34mvar[39;49;00m e,r=[34m0[39;49;00m;r<c.length;r++){[34mfor[39;49;00m([34mvar[39;49;00m t=c[r],n=![34m0[39;49;00m,o=[34m1[39;49;00m;o<t.length;o++){[34mvar[39;49;00m u=t[o];[34m0[39;49;00m!==p[u]&&(n=![34m1[39;49;00m)}n&&(c.splice(r--,[34m1[39;49;00m),e=f(f.s=t[[34m0[39;49;00m]))}[34mreturn[39;49;00m e}[34mvar[39;49;00m t={},p={[34m2[39;49;00m:[34m0[39;49;00m},c=[];[34mfunction[39;49;00m f(e){[34mif[39;49;00m(t[e])[34mreturn[39;49;00m t[e].exports;[34mvar[39;49;00m r=t[e]={i:e,l:![34m1[39;49;00m,exports:{}};[34mreturn[39;49;00m l[e].call(r.exports,r,r.exports,f),r.l=![34m0[39;49;00m,r.exports}f.m=l,f.c=t,f.d=[34mfunction[39;49;00m(e,r,t){f.o(e,r)||[36mObject[39;49;00m.defineProperty(e,r,{enumerable:![34m0[39;49;00m,get:t})},f.r=[34mfunction[39;49;00m(e){[33m"undefined"[39;49;00m!=[34mtypeof[39;49;00m Symbol&&Symbol.toStringTag&&[36mObject[39;49;00m.defineProperty(e,Symbol.toStringTag,{value:[33m"Module"[39;49;00m}),[36mObject[39;49;00m.defineProperty(e,[33m"__esModule"[39;49;00m,{value:![34m0[39;49;00m})},f.t=[34mfunction[39;49;00m(r,e){[34mif[39;49;00m([34m1[39;49;00m&e&&(r=f(r)),[34m8[39;49;00m&e)[34mreturn[39;49;00m r;[34mif[39;49;00m([34m4[39;49;00m&e&&[33m"object"[39;49;00m==[34mtypeof[39;49;00m r&&r&&r.__esModule)[34mreturn[39;49;00m r;[34mvar[39;49;00m t=[36mObject[39;49;00m.create([34mnull[39;49;00m);[34mif[39;49;00m(f.r(t),[36mObject[39;49;00m.defineProperty(t,[33m"default"[39;49;00m,{enumerable:![34m0[39;49;00m,value:r}),[34m2[39;49;00m&e&&[33m"string"[39;49;00m!=[34mtypeof[39;49;00m r)[34mfor[39;49;00m([34mvar[39;49;00m n [34min[39;49;00m r)f.d(t,n,[34mfunction[39;49;00m(e){[34mreturn[39;49;00m r[e]}.bind([34mnull[39;49;00m,n));[34mreturn[39;49;00m t},f.n=[34mfunction[39;49;00m(e){[34mvar[39;49;00m r=e&&e.__esModule?[34mfunction[39;49;00m(){[34mreturn[39;49;00m e.[34mdefault[39;49;00m}:[34mfunction[39;49;00m(){[34mreturn[39;49;00m e};[34mreturn[39;49;00m f.d(r,[33m"a"[39;49;00m,r),r},f.o=[34mfunction[39;49;00m(e,r){[34mreturn[39;49;00m [36mObject[39;49;00m.prototype.hasOwnProperty.call(e,r)},f.p=[33m"/"[39;49;00m;[34mvar[39;49;00m r=[36mwindow[39;49;00m.webpackJsonp=[36mwindow[39;49;00m.webpackJsonp||[],n=r.push.bind(r);r.push=e,r=r.slice();[34mfor[39;49;00m([34mvar[39;49;00m o=[34m0[39;49;00m;o<r.length;o++)e(r[o]);[34mvar[39;49;00m s=n;a()}([])</[34;01mscript[39;49;00m><[34;01mscript[39;49;00m [36msrc[39;49;00m=[33m"/static/js/1.fa92c112.chunk.js"[39;49;00m></[34;01mscript[39;49;00m><[34;01mscript[39;49;00m [36msrc[39;49;00m=[33m"/static/js/main.a7b1c78b.chunk.js"[39;49;00m></[34;01mscript[39;49;00m></[34;01mbody[39;49;00m></[34;01mhtml[39;49;00m>
    


# Further Work

## S3 Static Site Hosting

An article describing the use of S3 for static website hosting including use of https, DNS routing
https://medium.freecodecamp.org/how-to-host-a-static-website-with-s3-cloudfront-and-route53-7cbb11d4aeea


## Static Site Generators

Try other Static Site generators such as Hugo, Gatsby or Jekyll.

Information about such generators is available here: https://www.staticgen.com/



You can find more details about S3 website hosting here: https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html


# Cleanup

Note that we can use the ```aws s3 rm``` command to remove files from the bucket and ```aws s3 rb``` command to remove a bucket.


```bash
aws s3 rm s3://mjbright-static-site --recursive
aws s3 rb s3://mjbright-static-site
```

It's also possible to remoce the bucket directly using the ```--force``` option:
    ```aws s3 rb --force s3://mjbright-static-site```
