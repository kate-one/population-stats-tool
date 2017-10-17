import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

POP_DATA_PATH = 'https://esa.un.org/unpd/wpp/DVD/Files/1_Indicators%20(Standard)/EXCEL_FILES/1_Population/WPP2017_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx'
POP_RELATEABLE_PATH = ''
POP_AGE_DATA_PATH = 'https://esa.un.org/unpd/wpp/DVD/Files/1_Indicators%20(Standard)/EXCEL_FILES/1_Population/WPP2017_POP_F07_1_POPULATION_BY_AGE_BOTH_SEXES.xlsx'


# Make a function that pulls general population data from the UN site and re-shapes it for our use
def ReadPopulationData(path, skiprows=16):
    medium_variant = pd.read_excel(path, sheetname=1, skiprows=skiprows)

    medium_variant_long = pd.melt(medium_variant,
                                  id_vars=['Index', 'Variant', 'Region, subregion, country or area *', 'Notes',
                                           'Country code'],
                                  value_name='Population',
                                  var_name='Year')

    return medium_variant_long

# Write another function that pulls the age-disaggregated data from the UN site
def ReadPopulationAgeData(path, skiprows=16):
    age_data = pd.read_excel(path, sheetname=1, skiprows=skiprows)

    age_data_long = pd.melt(age_data,
                            id_vars=['Index', 'Variant', 'Region, subregion, country or area *', 'Notes',
                                     'Country code', 'Reference date (as of 1 July)'],
                            value_name='Population',
                            var_name='Age Cohort')

    return age_data_long


# Make a function that asks user to input a valid country name contained in the data set
def GetValidCountry(dataset):
    valid_country = False
    while valid_country == False:
        country = input('Enter a country name (in proper case, e.g. Nigeria):')
        if country == 'quit':
            quit()
        elif country in dataset['Region, subregion, country or area *'].unique():
            valid_country = True
            print('Thanks. {} is in the dataset.'.format(country))
        else:
            print('Sorry, {} is not in dataset. Please try again, e.g. Nigeria:'.format(country))

    return country

# Make a function that asks user to input a valid year contained in the data set
def GetValidYear(dataset, check_field='Year'):
    valid_year = False
    while valid_year == False:
        year = int(input('Enter a projection year (e.g. 2040):'))
        if year == 'quit':
            quit()
        elif year in dataset[check_field].unique():
            valid_year = True
            print('Thanks. {} is in the dataset.'.format(year))
        else:
            print('Sorry, {} is not in dataset. Please try again:'.format(year))

    return year

# Another function that asks user to input a valid age cohort range
def GetValidAgeCohort(dataset, check_field='Age Cohort'):
    valid_cohort = False
    while valid_cohort == False:
        cohort = str(input('Enter an age cohort (e.g. 10-14):'))
        if cohort == 'quit':
            quit()
        elif cohort in dataset[check_field].unique():
            valid_cohort = True
            print('Thanks. {} is in the dataset.'.format(cohort))
        else:
            print('Sorry, {} is not in dataset. Please try again. Valid values:'.format(cohort))
            print(dataset[check_field].unique())

    return cohort

# Write a function that runs the main menu prompts and asks the user to select an option
def MainMenu():
    print("")
    print("*********************")
    print(
        "Welcome to David & Kate's (as yet) Front-end-less Python Population Tool. Please select an option from the list:")
    print("1) Get a population projection for a given country and year")
    print("2) Find a comparable population for a given population projection")
    print("3) Find a population projection for a given country, year and age cohort")

    valid_answer = False
    while valid_answer == False:
        selection = str(input('Input a number (1-3):'))
        if selection in ['1', '2', '3', 'quit']:
            valid_answer = True
        else:
            print("Sorry, that is not a valid selection. Please enter numbers 1-3 or type 'quit':")

    return selection

# A small function to ask if the user would like to keep investigating or quit
def AnotherQuery():
    valid_answer = False
    while valid_answer == False:
        response = input('Would you like to make another query? (Y/N)')
        if response.lower() == 'y':
            valid_answer = True
            keep_playing = True
        elif response.lower() == 'n':
            print('Thanks for using this tool. Quitting....')
            keep_playing = False
            break
        else:
            print('Sorry, invalid response. Please type Y or N.')

    return keep_playing


# A function for Task 1: input a country and year and return the relevant population projection
def TaskOne(dataset):
    country = GetValidCountry(dataset)
    year = GetValidYear(dataset)

    population = dataset.loc[(dataset['Region, subregion, country or area *'] == country) &
                             (dataset['Year'] == year), 'Population'].values[0]

    print('The population for {} in the year {} is projected to be {} thousand.'.format(country, year, population))

    print('A time series plot of this population over time:')

    subset = dataset[(dataset['Region, subregion, country or area *'] == country)]

    subset.plot(x='Year', y='Population')
    #plt.show(block=True)
    file_name = country + '.png'
    plt.savefig(file_name)

    url = 'http://www.pythonanywhere.com/user/kateone/files/home/kateone/plots/' + file_name


    print('View your plot at:{}'.format(url))

# A function for Task 3: Find a population projection for a given country, year and age cohort
def TaskThree(dataset):
    country = GetValidCountry(dataset)
    year = GetValidYear(dataset, check_field='Reference date (as of 1 July)')
    age = GetValidAgeCohort(dataset)

    population = dataset.loc[(dataset['Region, subregion, country or area *'] == country) &
                             (dataset['Reference date (as of 1 July)'] == year) &
                             (dataset['Age Cohort'] == age), 'Population'].values[0]

    print('The population aged {} for {} in the year {} is projected to be {} thousand.'.format(age, country, year,
                                                                                                population))
    print('A time series plot of this age cohort over time:')

    subset = dataset[(dataset['Region, subregion, country or area *'] == country) &
                     (dataset['Age Cohort'] == age)]

    subset.plot(x='Reference date (as of 1 July)', y='Population')
    #plt.show(block=True)
    file_name = country + age + '.png'
    plt.savefig(file_name)

    url = 'http://www.pythonanywhere.com/user/kateone/files/home/kateone/plots/' + file_name

    print('View your plot at:{}'.format(url))


# Write the main function that calls all the other functions when needed
def run():
    keep_using = True

    # Create a blank variables to store each population data sets when needed
    pop_data = None
    pop_relateable = None
    pop_age_data = None

    # Start a loop that will keep going until the user decides to quit
    while keep_using == True:
        selection = MainMenu()  # Run main menu function to retrieve a valid menu option

        # Series of if statements to do different actions based on menu option
        if selection == '1':
            print("Thanks. You selected option 1.")
            if pop_data is None:  # Check if the population data is already downloaded and if not, download it
                print("Downloading the latest data from the UN....")
                pop_data = ReadPopulationData(POP_DATA_PATH)
                pop_data['Year'] = pop_data['Year'].astype('int64')
            TaskOne(pop_data)  # Run task 1 function

        elif selection == '2':
            print("Thanks. You selected option 2. Sorry, this is still in development.")

        elif selection == '3':
            print("Thanks. You selected option 3.")
            if pop_age_data is None:  # Check if the population data is already downloaded and if not, download it
                print("Downloading the latest data from the UN....")
                pop_age_data = ReadPopulationAgeData(POP_AGE_DATA_PATH)
            TaskThree(pop_age_data)  # Run Task 3 function

        elif selection == "quit":  # Add a secret 'quit' option in case the programme malfunctions in testing
            print("Quitting...")
            break

        else:  # Hopefully no one should get to this point, but just in case print an error message and stop the loop
            print("Error")
            break

        # Before re-running the loop, run the AnotherQuery function to see if the user would like to continue
        keep_using = AnotherQuery()

    return

if __name__ == "__main__":
    run()