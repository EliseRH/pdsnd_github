import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': r"C:\Users\HL-Dev-01\Documents\Udacity\Final_project\chicago.csv",
              'new york city': r"C:\Users\HL-Dev-01\Documents\Udacity\Final_project\new_york_city.csv",
              'washington': r"C:\Users\HL-Dev-01\Documents\Udacity\Final_project\washington.csv" }

cities = list(CITY_DATA.keys())
months = ['january','february','march','april','may','june']
months2 = ['jan','feb','mar','apr','may','june']
months3 = ['1', '2', '3', '4', '5', '6']
months_short = dict(zip(months2, months))
months_int = dict(zip(months3, months))
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
days2 = ['mon','tues','wed','thurs','fri','sat','sun']
days_short = dict(zip(days2, days))

#Ask the end user to specify a city to analyze
def get_city():
    """
    Asks user to specify a city to analyze.
    Returns:
        (str) city - name of the city to analyze
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        try:
            city = input(f"Would you like to see data for {cities[0].title()}, {cities[1].title()}, or {cities[2].title()}?\n").lower()
            city_df = pd.read_csv(CITY_DATA[city.lower()])
            print(f"You would like to see data for {city.title()}.")
            break
        except:
            print(f"{city} is not a valid city. Please enter one of the {len(cities)} city values provided.") 
    print('-'*40)
    return city, city_df


#provide some basic city-time stats (most common month, day of week, hour)
def time_stats(city, city_df):
    """Displays statistics on the most frequent times of travel."""
    print(f"\nCalculating The Most Frequent Times of Travel for {city}...\n")
    #city_df = pd.read_csv(CITY_DATA[city.lower()])
    start_time = time.time()
    city_df['Start Time'] = pd.to_datetime(city_df['Start Time'])
    #add a month column - udacity had me just do dt.month for month number but I switched it to month_name as we were filtering by name
    city_df['month'] = city_df['Start Time'].dt.month_name()
    #add a day of week name column
    city_df['day_of_week'] = city_df['Start Time'].dt.day_name()
    #add an hour column
    city_df['hour'] = city_df['Start Time'].dt.hour
    # display the most common month
    month_stats = (f"The most frequently travelled month in {city.title()} is {city_df['month'].mode()[0]}.\n")
    # display the most common day of week 
    day_stats =  (f"The most frequently travelled day of the week in {city.title()} is {city_df['day_of_week'].mode()[0]}.\n")
    # display the most common start hour
    add_on = ":00 hours"
    hour_stats = (f"The most frequently travelled hour in {city.title()} is {str(city_df['hour'].mode()[0]) + add_on}.\n")
    time_taken = "\nThis took %s seconds." % (time.time() - start_time)
    return print(month_stats, day_stats, hour_stats, "\n", time_taken, "\n", "-"*40)

# get user input for month (all, january, february, ... , june)
def get_other_stats():
    """
    Asks user to specify a month and a day of the week to analyze.
    Returns:
        (str) month - name of the month to analyze, from jan - june inclusive
        (str) day - day of the week to analyze
    """
    print("Let's dive into month and day-of-week specific data!")
    while True: 
        try: 
            month = input("For what month do you want to see data? You may write the month name or number. Please note that you can only input January - June. \n").lower()
            if month.lower() in months:
                print(f"You would like to see data for {month.title()}.")
                month = month.title()
                break
            elif month.lower() in months2:
                print(f"You would like to see data for {months_short.get(month).title()}.")
                month = months_short.get(month).title()
                break
            elif month in months3:
                print(f"You would like to see data for {months_int.get(month).title()}.")
                month = months_int.get(month).title()
                break
            else:
                print("That's not a valid month. Please enter a month from January - June")
        except:
            print("That's not a valid month. Please enter a month from January - June")
        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True: 
        try: 
            day = input("For what day of the week do you want to see data? You may write the day name or abbreviated name.\n").lower()
            if day.lower() in days:
                print(f"You would like to see data for {day.title()}.")
                day = day.title()
                break
            #need to add if they want for all days
            elif day.lower() in days2:
                print(f"You would like to see data for {days_short.get(day).title()}.")
                day = days_short.get(day).title()
                break
            else:
                print("That's not a valid day of the week. Please enter a day (e.g. Monday) or abbreviation (Mon, Tues, Wed, Thurs, Fri, Sat, or Sun)")
        except:
                print("That's not a valid day of the week. Please enter a day (e.g. Monday) or abbreviation (Mon, Tues, Wed, Thurs, Fri, Sat, or Sun)")
    print('-'*40)
    return month, day

# load all the filtered data into a new dataframe.
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #index a piece of the dictionary with [] to pull just one csv
    df = pd.read_csv(CITY_DATA[city.lower()])
    #convert the start time to a date-time object
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #add a month column
    df['month'] = df['Start Time'].dt.month_name()
    #add a day of week name column
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #filter by month
    if month != "all":
        df = df[df['month'] == month.title()]
    if day != 'all':
    #same filtering mechanism for day
        df = df[df['day_of_week'] == day.title()]
    return df

def station_stats(city, month, day, df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    start_station = (f"The most frequently used start station in {city.title()} in {month.title()} on a {day.title()} is {df['Start Station'].mode()[0]}.\n")
    # display most commonly used end station
    end_station = (f"The most frequently used end station in {city.title()} in {month.title()} on a {day.title()} is {df['End Station'].mode()[0]}.\n")
    # display most frequent combination of start station and end station trip
    combo_stations = (f"The most frequently used combination of start and end stations in {city.title()} in {month.title()} on a {day.title()} is {df.groupby(['Start Station','End Station']).size().idxmax()}.\n")
    time_statement = "\nThis took %s seconds." % (time.time() - start_time)
    return print(start_station, end_station, combo_stations, time_statement, "\n",'-'*40)

def trip_duration_stats(city, month, day, df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel_time = (f"Total travel time in {city.title()} during {month.title()} on a {day.title()} is {((df['Trip Duration'].sum()) // 60)//60} hours.\n")
    # display mean travel time
    mean_travel_time = (f"Average travel time in {city.title()} during {month.title()} on a {day.title()} is {(df['Trip Duration'].mean()) // 60} minutes.\n")
    time_statement = "\nThis took %s seconds." % (time.time() - start_time)
    print(total_travel_time, mean_travel_time, time_statement, "\n", '-'*40)

def user_stats(city, month, day, df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print(f"Bike user types in {city} in {month} on a {day} are:\n")
    for idx,name in enumerate(df['User Type'].value_counts().index.tolist()):
        print(name,":", df['User Type'].value_counts()[idx])
        print("\n")
    # Display counts of gender
    if "Gender" in df:
        mode_gender = df["Gender"].mode()[0]
        print(f"The most common gender for bike riders in {city} in {month} on a {day} is {mode_gender}.")
    else:
        print(f"There is no gender data for {city}.")
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        mode_birth = df["Birth Year"].mode()[0]
        print(f"The most common birth year for bike riders in {city} in {month} on a {day} is {mode_birth}.\n")
        earliest_birth = df["Birth Year"].min()
        print(f"The earliest birth year of any bike rider in {city} in {month} on a {day} is {earliest_birth}.\n")
        latest_birth = df["Birth Year"].max()
        print(f"The latest birth year of any bike rider in {city} in {month} on a {day} is {latest_birth}.\n")
    else:
        print(f"There is no birth year data for {city}.")
    time_statement = "\nThis took %s seconds." % (time.time() - start_time)
    print(time_statement, "\n", '-'*40)

def five_lines(city, month, day, df):
    #Displays 5 lines of raw data in a DataFrame at a time if users would like to see it
    view_data = input(f'\nWould you like to view 5 rows of individual trip data for {city} in {month} on a {day}? Enter yes or no\n')
    start_loc = 0
    if view_data == "yes":
        while True:
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            print("\n")
            view_display = input("Do you wish to continue viewing more lines of data?:").lower()
            if view_display != "yes":
                print("Ok, we will not show you any more raw data.")
                break
    else:
        print("Ok, we will not show you raw data.")



def main():
    while True:
        city, city_df = get_city()
        time_stats(city, city_df)
        month, day = get_other_stats()
        df = load_data(city, month, day)
        station_stats(city, month, day, df)
        trip_duration_stats(city, month, day, df)
        user_stats(city, month, day, df)
        five_lines(city, month, day,df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()