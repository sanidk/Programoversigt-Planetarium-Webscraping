import math
import time
#import numpy as np
import pandas as pd
# from tkinter import *
import tkinter as tk
from tkinter import ttk

# WEB SCRAPING LIBRARIES
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

URL = "https://planetarium.dk/billetter-og-program/"

# BEGIN SCRAPE
options = webdriver.ChromeOptions()
options.add_argument("--headless")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path='driver\chromedriver', options=options)

driver.get(URL)

shows_title_data = []
shows_time_data = []

events_title_data = []
events_time_data = []

time.sleep(5)

try:
    html = driver.page_source
    soup = BeautifulSoup(html, features='html.parser')

    shows = soup.find_all('li', {'class': 'c-program__item'})
    events = soup.find_all('li', {'class': 'c-schedule__event'})

    for show in shows:
        title = show.find('h4', {'class': 'c-program__item__title'})
        title_string = title.get_text()
        times = show.find_all('li')

        for time in times:
            time_string = time.get_text()
            # print(title_string + time_string)

            shows_title_data.append(title_string)
            shows_time_data.append(time_string)

    for event in events:
        title = event.find('a', {'class': 'c-schedule__event__title u-link'})
        if title is not None:
            title_string = title.get_text()
            # print(title_string)

            time_string = event.find('p', {'class': 'c-schedule__event__time'}).get_text()
            # print(title_string + time_string)

            events_title_data.append(title_string)
            events_time_data.append(time_string)

    driver.quit()


except TimeoutException:
    driver.quit()
    exit()

# end scraping start sorting data

all_times = []
all_titles = []

shows_array = []

for title in events_title_data:
    all_titles.append(title)
    shows_array.append(title)

for title in shows_title_data:
    all_titles.append(title)
    shows_array.append(title)

event_start_times = []
event_end_times = []

show_start_times = []

for event_time in events_time_data:
    time = event_time.split("-")
    # if (time.length == 2)
    startime = time[0]
    # endtime = time[1]
    all_times.append(startime)
    shows_array.append([[startime]])

    # event_start_times.append(event_times[0])
    # event_end_times.append(event_times[1])

# print(event_start_times)
for show_time in shows_time_data:
    # show_start_times.append(show_time[1:-1])
    starttime = show_time[1:-1]
    all_times.append(starttime)
    shows_array.append([[starttime]])

all_dict = {'title': all_titles, 'time': all_times}
all_df = pd.DataFrame(all_dict)
sort_df = all_df.sort_values(by=['time'])

# events_dict = {'title': events_title_data, 'time': event_start_times}
# events_df = pd.DataFrame(events_dict)

# print(sort_df)


# START GUI APP
# root window
root = tk.Tk()
root.geometry("1200x800")
root.title('Planetarium Program')
root.resizable(0, 0)

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

row = 0

for item in sort_df['time']:
    time_label = ttk.Label(root, text=item)
    time_label.config(font=("Courier", 16))
    time_label.grid(column=0, row=row, sticky=tk.W, padx=5, pady=5)
    row += 1

row = 0

for item in sort_df['title']:
    title_label = ttk.Label(root, text=item)
    title_label.config(font=("Courier", 14))
    title_label.grid(column=1, row=row, sticky=tk.W, padx=5, pady=5)
    row += 1

root.mainloop()
