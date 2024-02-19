from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os

# Set the path for the Chrome driver 
chrome_driver_path = '/Users/jungwoo/Desktop/kjungwoo/DataScienceLab/EDA/chromedriver-mac-arm64/chromedriver'

# Initialize the Chrome driver service
service = Service(chrome_driver_path)

# Configure Chrome options
options = Options()
options.add_argument('--headless') # Unlock '--headless' option to display the browser window for debugging
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the web driver for Chrome
driver = webdriver.Chrome(service=service, options=options)

# List of seasons
seasons = ['2021', '2022', '2023']

for season in seasons:
    # Open the web page
    driver.get("https://www.koreabaseball.com/Record/Crowd/GraphDaily.aspx")

    # Select the season from the dropdown menu
    select = Select(driver.find_element(By.ID, 'cphContents_cphContents_cphContents_ddlSeason'))
    select.select_by_value(season)  # Select the season

    # Click the 'Search' button
    search_button = driver.find_element(By.ID, 'cphContents_cphContents_cphContents_btnSearch')
    search_button.click()

    # Wait for the page to load
    time.sleep(5)

    # Parse the web page using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Select the table body using its CSS selector
    table = soup.select_one('#cphContents_cphContents_cphContents_udpRecord > table > tbody')

    # Create a list that includes all 'tr' tags with the class 'order'
    rows = table.select('tr.order')

    data = []

    # Extract data from each row
    for row in rows:
        # Find all 'td' tags within the row and create a list
        cols = row.find_all('td')
        # Extract text data from each cell and append it to the data list
        data.append([col.text.strip() for col in cols])

    # Create a DataFrame and specify the column names
    df = pd.DataFrame(data, columns=["Date", "Day", "Home Team", "Visiting Team", "Stadium", "Audience Count"])

    # Remove commas from the audience count and convert it to an integer
    df['Audience Count'] = df['Audience Count'].str.replace(',', '').astype(int)

    # Sort the DataFrame based on the 'Date' and 'Home Team'
    df = df.sort_values(by=['Date', 'Home Team'])

    # Print the first few rows of the DataFrame
    print(f'{season} Data:')
    print(df.head())

    # Save the DataFrame to an Excel file
    df.to_excel(f"./data/{season}.xlsx", index=False)

# Close the browser
driver.quit()
