App write with django python
=================================
To start app please following the step
=================================
1.Start virenv by
cd ~/gitrepo
source newenv/bin/activate

2.Start Django server
cd ~/gitrepo/aim1
python manage.py runserver 0.0.0.0:8000


==================================
Please note the limitation of clawler is around 500 perday
But to collect all the data, it need around 900 request
So you have to at least use 2 days to collect the data. (please change offset variable in views.py to continue in the second day)
*****Also you can found the current schema at the script folder
