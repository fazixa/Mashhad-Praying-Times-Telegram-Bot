import requests

def news_data():
	res=requests.get('https://prayer.aviny.com/api/prayertimes/13');
	return res.json();

def out_news(result):
	CityName = "اوقات شرعی {}".format(result['CityName'])
	Today = "امروز: {}".format(result['Today'])
	Imsaak = "اذان صبح: {}".format(result['Imsaak'])
	Sunrise = "طلوع آفتاب: {}".format(result['Sunrise'])
	Noon = "اذان ظهر: {}".format(result['Noon'])
	Sunset = "غروب خورشید: {}".format(result['Sunset'])
	Maghreb = "اذان مغرب: {}".format(result['Maghreb'])
	Midnight = "نیمه شب شرعی: {}".format(result['Midnight'])


	message = "\n".join([CityName,Today,Imsaak,Sunrise,Noon,Sunset,Maghreb,Midnight])
	return message

def news():

	data= news_data();
	return out_news(data)
