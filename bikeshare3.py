#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 16:23:14 2024

@author: hibahvora
"""


import time
# Pandas organizes data tables and allows us to manipulate them to find insights
import pandas as pd 

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Initialize city variable
    city = ""
    while city not in ['chicago', 'new york city', 'washington']:
        print("Kindly add what city (chicago, new york city, washington):")
        city = input().lower()  # Get user input and convert to lowercase
        if city not in ['chicago', 'new york city', 'washington']:
            print("Invalid city. Please try again.")  # Inform the user if the input is invalid

    # Initialize month variable
    month = ""
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in valid_months:
        print("Kindly add what month (all, January, February, ... , June):")
        month = input().lower()  # Get user input and convert to lowercase
        if month not in valid_months:
            print("Invalid month. Please try again.")  # Inform the user if the input is invalid

    # Initialize day variable
    day = ""
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day not in valid_days:
        print("Kindly add what day (all, Monday, Tuesday, ... Sunday):")
        day = input().lower()  # Get user input and convert to lowercase
        if day not in valid_days:
            print("Invalid day. Please try again.")  # Inform the user if the input is invalid

    return city, month, day  # Return the values

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df = pd.read_csv(CITY_DATA[city])  # Load the data into a DataFrame

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day if applicable
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df  # Return the filtered DataFrame

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print(f'Most common month: {most_common_month}')

    # Display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f'Most common day: {most_common_day}')

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f'Most common start hour: {most_common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_station_start = df['Start Station'].mode()[0]
    print(f'Most common start station: {most_common_station_start}')

    # Display most commonly used end station
    most_common_station_end = df['End Station'].mode()[0]
    print(f'Most common end station: {most_common_station_end}')

    # Display most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_start_end = df['Start End Station'].mode()[0]
    print(f'Most frequent combination of start and end station: {most_common_start_end}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total travel time: {total_travel_time}')

    # Display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print(f'Mean travel time: {avg_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender if available
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)

    # Display earliest, most recent, and most common year of birth if available
    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print(f'Earliest year of birth: {earliest_birth}')
        print(f'Most recent year of birth: {most_recent_birth}')
        print(f'Most common year of birth: {most_common_birth}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def descr_stats(df):
    # Ask the user if they want to see descriptive statistics
    user_input = input("Do you want to see descriptive statistics? yes or no: ").strip().lower()
    
    # Check the user's response
    if user_input == 'yes':
        # Display the descriptive statistics
        print(df.describe())
    elif user_input == 'no':
        print("Okay, not displaying the statistics.")
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        return  # Exit the function if the input is invalid

    # Now ask the user if they want to see raw data
    start_index = 0
    while True:
        user_input = input("Do you want to see 5 lines of raw data? yes or no: ").strip().lower()
        
        if user_input == 'yes':
            # Display the next 5 lines of raw data
            print(df.iloc[start_index:start_index + 5])
            start_index += 5  # Move to the next set of 5 lines
            
            # Check if there are more lines to display
            if start_index >= len(df):
                print("No more raw data to display.")
                break  # Exit the loop if there are no more lines
        elif user_input == 'no':
            print("Okay, not displaying more raw data.")
            break  # Exit the loop if the user says no
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        descr_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
