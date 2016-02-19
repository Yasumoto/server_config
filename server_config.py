# check argument
# do we have a hostlist with that name
# if so, delegate to that command
# command should zip up the current hello_world directory, include the git sha in the filename
# for each file, ssh into the host
# if apache2, php5, or libapche2-mod-php5 are not present
  # sudo apt-get install apache2 php5 libapache2-mod-php5
  # sudo /etc/init.d/apache2 restart
  # rm index.html (for apache2 only)
# scp over the new zip file to a staging directory that you create
# unzip it into /var/www/html
# urllib.urlopen(), ensure Hello, World! (make a comment that it can change)
