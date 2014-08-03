Django Poll Site
================

This repository contains the source code for a sample Django Polls site. The username and password for Django administration is simply "admin".

# Basic Deployment
The following deployment setup is only meant as an example for those wishing to quickly deploy this application to a web server without necessarily understanding the code.

You'll need the following installed before cloning the source code:
- [Python 2.7](https://www.python.org/downloads/)
- [PyCrypto](https://www.dlitz.net/software/pycrypto/) (if you're on Windows, look at [these installers](http://www.voidspace.org.uk/python/modules.shtml#pycrypto))
- [PIP](http://pip.readthedocs.org/en/latest/installing.html)

You'll need to setup the following [Amazon Web Services (AWS)](http://aws.amazon.com/):
- [Launch an EC2 instance](http://aws.amazon.com/ec2) running Ubuntu Server (or some other Debian-based operating system)
- Save the .pem key pair file for the EC2 instance as ~/.ssh/myserver.pem
- Create an EC2 Security Group that has port 80 opened
- [Create an S3 bucket](http://aws.amazon.com/s3/).
- Generate an AWS Access Key and Secret Access Key
- (Optional) An elastic IP associated with the VM
- (Optional) A DNS entry pointing to the elastic IP address

Now you're ready to checkout, configure, and deploy the code to your EC2 server.

- Clone the source code
- Modify the variables at the bottom of djangopollsite/settings.py to customize the application
- Modify the variables at the top of fabfile.py to point to your EC2 instance's IP or domain
- From the Command Line at the root of the cloned source, execute "pip install -r reqs.txt"
- From the Command Line at the root of the cloned source, execute "fab deploy"

## Use a Production-Like Database
In a production setting, you should not use the accompanying SQLite database. To use a database like PostgreSQL, execute the following commands on the EC2 instance:

- sudo apt-getinstall python-psycopg2 postgresql-9.3
- sudo -u postgres psql
 - CREATE USER db_user WITH PASSWORD 'db_password';
 - CREATE DATABASE "db_name" encoding='UTF8';
 - GRANT ALL PRIVILEGES ON DATABASE "db_name" to db_user;
 - \q

Modify the database configuration in djangopollsite/settings.py to match the PostgreSQL settings found here: https://docs.djangoproject.com/en/1.7/ref/settings/#databases, then restart Apache:

- sudo service apache2 restart

# More Information
If you're looking for a more detailed tutorial on the code and deployment, check out the full tutorial found here: http://www.alexlaird.com/2014/08/django-dropzone-uploader
