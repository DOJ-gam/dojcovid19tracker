from flask import Flask, redirect, url_for, render_template, request
import requests

app = Flask(__name__)


# Gambia
req = requests.get("https://disease.sh/v3/covid-19/countries/gambia")
gambia = req.json()

# Global Data
req = requests.get("https://disease.sh/v3/covid-19/all")
global_data = req.json()

# All countries data
req = requests.get("https://disease.sh/v3/covid-19/countries")
all_countries_data = req.json()

# Africa
req = requests.get("https://disease.sh/v3/covid-19/continents/africa")
africa = req.json()

# Europe
req = requests.get("https://disease.sh/v3/covid-19/continents/europe")
europe = req.json()

# Asia
req = requests.get("https://disease.sh/v3/covid-19/continents/asia")
asia = req.json()


@app.route('/')
def home():

    # Continents
    # continent
    # req = requests.get(
    #     f"https://disease.sh/v3/covid-19/continents/{continent}")
    # continent = req.json()

    # render_template('header.html', single_country=single_country_data)
    return render_template('index.html', asia=asia, africa=africa, europe=europe, all_countries=all_countries_data, gambia=gambia, global_data=global_data, page_title="HOME PAGE")


@app.route('/global')
def allCountries():

    # All countries data
    req = requests.get("https://disease.sh/v3/covid-19/countries")
    all_countries_data = req.json()

    return render_template('global.html', global_data=global_data, all_countries=all_countries_data, gambia=gambia,  page_title="GLOBAL STATISTICS")


@app.route('/countries/<country>')
def country(country):
    try:

        # have to use the 'f' to be able to insert '{}'
        req = requests.get(
            f"https://disease.sh/v3/covid-19/countries/{country}")

        data = req.json()

        return render_template('country.html', country=data, gambia=gambia)

    except Exception as error:
        print('There is an error', error)
        return "There is an error " + error
        return "data for a {country}"


@app.route('/continents/<continent>')
def continent(continent):

    # Data for continents
    if continent == 'america':
        req = requests.get(
            f"https://disease.sh/v3/covid-19/continents/north america")
        north_america = req.json()

        req = requests.get(
            f"https://disease.sh/v3/covid-19/continents/south america")
        south_america = req.json()

        # Make a dictionary with keys and values of records of the data
        continent_stats = {
            "cases": north_america['cases'] + south_america['cases'],
            "population": north_america['population'] + south_america['population'],
            "critical": north_america['critical'] + south_america['critical'],
            "todayRecovered": north_america['todayRecovered'] + south_america['todayRecovered'],
            "todayDeaths": north_america['todayDeaths'] + south_america['todayDeaths'],
            "todayCases": north_america['todayCases'] + south_america['todayCases'],
            "active": north_america['active'] + south_america['active'],
            "recovered": north_america['recovered'] + south_america['recovered'],
            "tests": north_america['tests'] + south_america['tests'],
        }
    else:
        req = requests.get(
            f"https://disease.sh/v3/covid-19/continents/{continent}")

        continent_stats = req.json()

    all_continent_data = []

#       for every country in all the countries, if the continent is in the all_countries_data as continent, add to the list
    # we use in because america is in north america, and south america
    for country in all_countries_data:
        if continent in country['continent'].lower():
            all_continent_data.append(country)

    return render_template('continents.html', all_continent_data=all_continent_data, continent_stats=continent_stats, gambia=gambia, page_title=continent)


@app.route('/search')
def search():
    # country here is what the user entered in the form input
    country = request.args.get('country')

    # Filtering starts here...
    filtered_data = []

    for record in all_countries_data:
        # we are converting country to lowercase and check if the word is in the name of the country in the covid-data list.
        if country.lower() in record['country'].lower():
            filtered_data.append(record)

    return render_template('global.html', global_data=global_data, all_countries=filtered_data, gambia=gambia,  page_title="GLOBAL STATISTICS")


if __name__ == '__main__':
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run()
