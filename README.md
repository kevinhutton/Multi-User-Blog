# Udacity Fullstack Nanodegree Project 3 - Multi-User Blog

The purpose of this project was to create a Multi-User Blog application which runs on google app engine.

Users can do the following with this application

1. Add/remove blog posts 
2. Comment on blog posts created by other users (or their own blog post)
3. Upvote/like blog posts

The application has the following security/privacy features:

  1. Passwords are fully encrypted and storing securely within a Google App Engine Entity
  2. Secure Cookies are used to avoid spoofing and session hijacking
  3. Users can only post/comment/like while logged in
  4. Users can delete posts,comments,likes which were created by themselves
  5. Users can not modify posts/comments/likes created by other users


This application demonstrates the following tools/technologies:

  1. python
  2. jinja2 templating
  3. Google App Engine
  4. Encryption
  5. Html5/CSS

This project was done as part of the Udacity Fullstack Nanodegree program

##Required Libraries and Dependencies

1. Web browser which supports HTML5 (E.g. Chrome,Firefox)
2. git
3. python 2.7+
4. jinja2 python module


###How to Run Project

####Running Locally:


1. Install jinja2 python module

2. Install Google App Engine SDK for Python  (https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)

2. ``` git clone https://github.com/kevinhutton/Udacity-Fullstack-Nanodegree-Project3.git ```

3. ``` cd Udacity-Fullstack-Nanodegree-Project3/ ```

4. Run the local Google App Engine dev server using the Google App Engine SDK

   ``` <your-google-cloud-sdk-install-location>/bin/dev_appserver.py . ```

5. The application should now be available at localhost:8080

####Running on Google App Engine:


1. Signup for Google App Engine (https://appengine.google.com/)
2. Create a new project in Google’s Developer Console
3. Install Google App Engine SDK for Python  (https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
4. Configure the SDK for deployment by using
    ``` <your-google-cloud-sdk-install-location>/bin/gcloud init ```
5. ``` git clone https://github.com/kevinhutton/Udacity-Fullstack-Nanodegree-Project3.git ```
6. ``` cd Udacity-Fullstack-Nanodegree-Project3/ ```
7. Deploy the app using
      ``` <your-google-cloud-sdk-install-location>/bin/gcloud app deploy ```
8. Your app should be available at https://<your-unique-project-name.appspot.com/


