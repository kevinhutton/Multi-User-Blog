# Udacity Fullstack Nanodegree Project 3 - Multi-User Blog 

The purpose of this project was to create a Multi-User Blog application which runs on google app engine.

Users can do the following with this application

  a) Add/remove blog posts
  b) Comment on blog posts created by other users (or their own blog post)
  c) Upvote/like blog posts

The application has the following security/privacy features:

  a) Passwords are fully encrypted and storing securely within a Google App Engine Entity
  b) Secure Cookies are used to avoid spoofing and session hijacking
  c) Users can only post/comment/like while logged in
  d) Users can delete posts,comments,likes which were created by themselves
  e) Users can not modify posts/comments/likes created by other users
  
This application demonstrates the following tools/technologies:

  a) python
  b) jinja2 templating
  c) Google App Engine
  d) Encryption
  e) Html5/CSS

This project was done as part of the Udacity Fullstack Nanodegree program

Required Libraries and Dependencies
-----------------------------------
1) Web browser which supports HTML5 (E.g. Chrome,Firefox)
2) git
3) python 2.7+
4) jinja2 python module

How to Run Project
------------------
Running Locally:

1) Install jinja2 python module

2) Install Google App Engine SDK for Python  (https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)

2) git clone https://github.com/kevinhutton/Udacity-Fullstack-Nanodegree-Project3.git

3) cd Udacity-Fullstack-Nanodegree-Project3/

4) Run the local Google App Engine dev server using the Google App Engine SDK 

      <your-google-cloud-sdk-install-location>/bin/dev_appserver.py .
      
5) The application should now be availavle at localhost:8080

Running on Google App Engine:

1) 
