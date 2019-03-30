.. Instructions on how to set up an FTP client to upload data to box.com
   Author: Eirikur Jonsson (eirikurj@umich.edu)


.. _uploadingToBox:

Accessing and using UM box.com with FTP
=======================================

These instructions tell you how to use an FTP client to access and upload
large amount of data to UM box.com.

The Box Sync client does not exist for Linux and it does not handle
large number of files very well.



Set external password on box.com
--------------------------------

To access box.com using the FTP an external password has to be set. To do so
follow these instructions, https://community.box.com/t5/How-to-Guides-for-Account/Box-SSO-Working-with-External-Passwords/ta-p/52034

In short this is what is needed

#. Log on to box.com and go to ``Account Settings``
#. Under ``Authentication`` set your external password



Configure the FTP client
------------------------


The FileZilla FTP client is recommended. To install open a terminal
and type::

    sudo apt-get install filezilla

Once the installation is complete, open the FTP client. To speed the
uploading process, increase the number of simultaneous connections by going to
``Edit -> Settings -> Transfers -> Maximum simultaneous connections``,
and set that to 10


Open ``File -> Site Manager`` and connect to box.com using the following settings shown below::

     Host: ftp.box.com
     Port: 990
     Protocol: FTP- File Transfer Protocol
     Encryption: Require implicit FTP over TLS
     Logon Type: Normal
     User: <your_user_name>@umich.edu
     Password: <your_password>


Once you have typed in your information the window should look like

    .. image:: images/boxFTP.png
        :scale: 50 %
