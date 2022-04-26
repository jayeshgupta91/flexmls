# importing all the libraries 
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import time
from sheet import *

# hiding the browser window and for one error solution 

def dataScraper():
    options = webdriver.ChromeOptions()
    
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # giving web browser webdriver path
    # for windows
    # driver = webdriver.Chrome('chromedriver.exe', options = options)

    # for ubuntu
    driver = webdriver.Chrome(service = Service('./drivers/chromedriver'), options = options) 

    try:
        # requesting the site to fetch the data
        url = sheetGet.cell(1,2).value
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # switching to the iframe 
        iframe_src = soup.select_one("#publiclinkpanel").attrs["src"]
        driver.get(f"https://www.flexmls.com:{iframe_src}")
        time.sleep(3)
        # left_grid Data list 
        # left_grid_list = driver.find_element(By.CLASS_NAME,"listing").text.split("\n")
        pro_id = driver.find_element(By.XPATH,"/html/body/div[42]/div[7]/table[1]/tbody/tr[1]/td[2]/span/div/span[4]/span[2]/a").text
        if not sheetData.find(f'{pro_id}'):
            next = next_available_row(sheetData)
            # updating id
            sheetData.update_cell(next,1,pro_id)

            # Swiching to detail view iframe 
            iframe_src = driver.find_element(By.ID,"iframe_detail").get_attribute("src")
            driver.get(f"{iframe_src}")
            time.sleep(2)

            # gettind price
            price = driver.find_element(By.XPATH,"/html/body/span/table[1]/tbody/tr/td/table[1]/tbody/tr/td[3]/span").text
            address = driver.find_element(By.XPATH,"/html/body/span/table[1]/tbody/tr/td/table[1]/tbody/tr/td[2]/span").text
            sheetData.update_cell(next,10,price)
            sheetData.update_cell(next,14,address)
            # print(address + " "+ price)

            detail_frame_data_list = driver.find_element(By.CSS_SELECTOR,"tbody:nth-child(1) tr:nth-child(2) td:nth-child(1) span:nth-child(1)").text.split("\n")
            print(detail_frame_data_list)

            # getting sqft
            sqft = detail_frame_data_list[2]
            sqft = sqft[sqft.find(":")+1:sqft.find("/")]
            sheetData.update_cell(next,11,sqft)
            # print(sqft)

            # getting bedsBaths
            bedsBaths = detail_frame_data_list[0]
            s = detail_frame_data_list[0].rfind("/")
            beds = bedsBaths[bedsBaths.find(":")+2:s]
            bath =  bedsBaths[s+2:]

            sheetData.update_cell(next,12,beds)
            sheetData.update_cell(next,13,bath)

            # print(beds + " "+bath)

            # Fetching some images from the detail view 
            # Going back to secound frame to get photos view 
            iframe_src = soup.select_one("#publiclinkpanel").attrs["src"]
            driver.get(f"https://www.flexmls.com:{iframe_src}")
            time.sleep(2)

            # Go to photos view 
            driver.find_element(By.ID,"tab_tour").click()
            time.sleep(2)
            iframe_src = driver.find_element(By.ID,"iframe_tour").get_attribute("src")
            driver.get(f"{iframe_src}")
            time.sleep(2)

            # Finding Gallary Of photos
            find_gallery = driver.find_elements(By.CSS_SELECTOR, ".rsTmb.photo")
            images_list = []
            try:
                if len(find_gallery) <= 6:
                    for get_images in find_gallery:
                        images_list.append(get_images.value_of_css_property("background-image"))
                else:
                    for index, get_images in enumerate(find_gallery):
                        if index < 6:
                            images_list.append(get_images.value_of_css_property("background-image"))
                        else:
                            break
            except:
                print("No images found")


            print(images_list)
            imageValue = []
            imagenext = 4
            for i in images_list:
                temp = (i.split('"')[1::2][0])
                index = temp.rfind('.')
                temp = temp[:index] + "-o" + temp[index:]
                sheetData.update_cell(next,imagenext,temp)
                imagenext += 1
                imageValue.append(temp)
            print(imageValue)
            # creating the log file
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f= open("log.txt","a")
            f.write(str(dt_string)+"      "+str(pro_id)+"\n")
            f.close()
            driver.quit()
        else:
            # creating the log file
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f= open("log.txt","a")
            f.write(str(dt_string)+"      No New Id Found"+"\n")
            f.close()
            print("no ID found")
            driver.quit()

    except Exception as e:
        # creating the log file
        driver.quit()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f= open("log.txt","a")
        f.write(str(dt_string)+"   error occured"+str(e)+"\n")
        f.close()
