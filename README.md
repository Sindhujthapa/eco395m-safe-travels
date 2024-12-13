<h1 align="center">PickleSpots Project</h1>
<p align="center"> <img src="https://cdn.sanity.io/images/jvolei4i/production/805cc6aceadb385fe3e80f4c905591837d7a9c8b-736x586.webp" alt="Description" width="500"> </p>
<h2 align="center">Project Goal</h2>
<p>Based on a list of the top 50 visited cities in the United States, we want to create an interface that will recommend nearby pickleball courts with the locations, as well as present weather data and corresponding outfit suggestions to users.</p>
<h2 align="center">Project Description</h2>
We scraped data for the pickleball courts in and nearby each city, along with the daily weather information for each city of the day of search, which includes the daily temperature, wind speed, humidity, and other weather statistics. The data is then turned into a CSV and uploaded to a SQL database so that we can run queries through the SQLAlchemy engine. We will connect the weather data to the corresponding cities in the pickleball data through the schema of the SQL database. The interface is created through Streamlit, an applet that projects Python code in a user-friendly manner.
<h2 align="center">Methodology</h2>
We are scraping data for the following information for this project:
<li>Daily weather for the top 50 visited cities in the United States (Average Temperature and Weather Description)</li>
<li>Prominent pickleball courts in and nearby the aforementioned cities, including data on the number of courts available at each location, and the state of the court's lines and net.</li>
<li>Google Map locations of each court</li>
<h2 align="center">Reproducibility</h2>
The reproducibility of this project is doable, but requires a lot of information. To scrape the courts on Pickleheads, the Selenium package is needed in order to gain access to the web browser since the website uses Cloudflare to prevent scraping. After obtaining the information of courts in each cities, you can create a CSV which all the courts and upload it to an SQL database. 
<h2 align="center">Limitations of Project</h2>
<li>We are only using information for the 50 most visited cities in the United States, so we are limiting the interface's responses to the data we are scraping from.</li>
<li>We are limiting our activities to that of pickleball courts, so more urban cities might have a lower density of courts within the center and may only recommend courts further away.</li>
<li>Since it is difficult to accurately measure if the courts are currently in use, a person might show up to courts only to find out that there are none open.</li>
<h2 align="center">Extensions of Project</h2>
<li>A good start for extending the model can be to include more cities in each state. The inclusion of all major cities in the United States can broaden the recommendations given for users of the interface for other courts.</li>
<li>The inclusion of other outdoor activitues - such as parks, kayaking, and biking paths - can give users more variety what they could do in the city they select.</li>
<li>The inclusion of Yelp or other review sites could add people's opinions about the courts and more easily rank each court in a city</li>
<h2 align="center">Sources of Datatsets</h2>
<li>The cities we are using for this project were selected by this website as the top 50 travel destinations in the United States: https://www.aaa.com/tripcanvas/article/50-top-travel-destinations-in-the-us-CM534#methodology</li>
<li>The list of pickleball courts comes from Pickleheads: https://www.pickleheads.com/</li>
<li>The weather data comes from scraping the weather information on Dress my Run: https://dressmyrun.com/</li>
