# Daily-Update

## User Guide and description for this code ##
This is an alarm and notification system that gives daily updates, in these daily updates there are  news updates which gives top heaadlines,weather update which gives current weather and covid update which gives covid updates. From the config file thes user can change crucial information to edit the results that are shown in the notification updates,notification updates are shown on the hour,the user would also be able to make alarms, the user can set and alarm at a particular time and get a Covid Update which also has a voice notification, the user also has the choice to include news updates and weather updates when creating the alarm, the user can also cancel an alarm set and cancel notifications after reading.

## Developer Guide for this code
This code gets news weather and covid updates using this respective API'S from the following sources:<p>(https://newsapi.org/)</p><p>(https://openweathermap.org)</p><p>(https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/)</p>This Code is rendered onto the HTML file,index.HTML.A Function is create to return each update, A function is Created to return text-to-speech for alarm. A function called clock has being created to always get the current time,And a function is created that returns Alarm inputted. In another function a while loop is created so A function is always checking whether Alarm time inputted is equal to the current time, If it is the covid update function will return covid updates and if the user inputted for news and weather, they will also be update respectfully.

## Installation
<p>Flask must be installed to render the code to html using : pip install flask</p>
<p>To use pyowm as it's used in the weather function : pip install pyom </p>
<p>for the CovidAPI : pip install uk-covid19</p>

## How to Extend this code
 In the function where notifications are updated, the time notifications are updated can be altered,also more notification updates can be added by simply creating a function that returns a particular information and calling the functions where neccessary, also in the function where notifications are updated the code can be altered to return notifications at a particular time each day.

