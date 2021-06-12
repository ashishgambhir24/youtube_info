# Setup
Clone this repo

For every terminal, first source bash_aliases file to use command line shortcuts, using following command

> source .bash_source

After this first we need to turn on docker containers using command - 
> dc up

or we can also use the following command - 
> dcrestart

above command is a shortcut which is mentioned in .bash_aliases file. It could be used if any time we want to restart all containers, or a specific container or a set of containers
> dcrestart django

or

> dcrestart django worker

This commond stops existing running container, removes its image, and build it again.

similarly we can use following command to stop a container - 
> dcstop


# Logging
Logs of all contianers or specific containers can be monitored using following command - 
> dclogs

or

> dclogs worker


# API
Currently APIs are not authenticated, so we can directly use APIs from postman or browser
APIs - 

all videos api - 
http://0.0.0.0:8000/youtube/video/all-videos/?start=0&entries=20

(here start and entries are used for pagination)

search api - 
http://0.0.0.0:8000/youtube/video/search/?q={urllib_encoded_string}

# Dashboard
To access dashboard you need to first create a superuser

Open a session in currently running container using following command - 
> container

Docker session opens up. Run following command - 
>> python manage.py createsuperuser

It would ask you to set username, email and password for superuser, using which you can access admin dashboard

Link to dashboard - 
http://0.0.0.0:8000/youtube/admin/

Enter your credentials and django dashboard will open up.

In django dashbaord you can see list of all available videos.

You can also search for a video using its title, description, video id or channel name

There are also a few filters added according to which you can filter out required videos

Also many important fields of video model is displayed on all video page, so you can also sort videos according to those fields

(All Thanks to easy to use and easy to integrate django dashboard)

# After Testing
After testing please stop all the containers, or atleast the worker, or else it would exceed the limit of Youtube's APIKEY
> dcstop worker



