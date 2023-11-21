from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import os
from time import sleep

def get_list_items(button_id, list_id):
    sleep(1)

    # open dropdown
    WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_element_located((By.ID, button_id))
    ).click()

    # get list items
    list = driver.find_element(By.ID, list_id)
    items = list.find_elements(By.TAG_NAME, "li")

    # remove the first item as it is the "All" option
    items.pop(0)
    items = [item.text for item in items]

    # close dropdown
    WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_element_located((By.ID, button_id))
    ).click()

    sleep(1)

    return items

downloads_path = os.getcwd() + "\downloads"
data_path = os.getcwd() + "\data"

if not os.path.exists(downloads_path):
    os.mkdir(downloads_path)

if not os.path.exists(data_path):
    os.mkdir(data_path)

# wipe the folders
downloads = os.listdir(downloads_path)
for download in downloads:
    os.unlink(download)

data = os.listdir(data_path)
for d in data:
    os.unlink(d)


chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : downloads_path}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)
driver.get(
    "https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2F0b3119f0-db06-4f10-a9cd-61092b5790bc&sectionIndex=0&sso_guest=true&reportViewOnly=true&reportContextBar=false&sas-welcome=false"
)
driver.set_window_size(1280, 800)

# wait for the page to load
WebDriverWait(driver, 60).until(
    expected_conditions.frame_to_be_available_and_switch_to_it(
        (By.ID, "VANextLogon_iframe")
    )
)

# hide error message
WebDriverWait(driver, 30).until(
    expected_conditions.presence_of_element_located(
        (By.ID, "__dialog1-closeButton-BDI-content")
    )
).click()

# find the parent of the element with the text "Salud mental" and click it
WebDriverWait(driver, 30).until(
    expected_conditions.presence_of_element_located(
        (By.XPATH, "//*[contains(text(), 'Salud mental')]/..")
    )
).click()

### find the dropdowns with the region, servicio, comuna and establecimiento
# get all the values for each of the 4 dropdowns
# for each value, select it and wait for the table to load
# then, click the export button and wait for the download to finish
# first dropdown (regiones) __select0 and get values from __list2
# second dropdown (servicios) __select1 and get values from __list3
# third dropdown (comunas) __select2 and get values from __list4
# fourth dropdown (establecimientos) __select3 and get values from __list5

for region in get_list_items("__select0", "__list2"):
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.ID, "__select0"))
    ).click()
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, f'[title*="Región: {region}"]')
        )
    ).click()

    for servicio in get_list_items("__select1", "__list3"):
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "__select1"))
        ).click()
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, f'[title*="Servicio de Salud: {servicio}"]')
            )
        ).click()

        for comuna in get_list_items("__select2", "__list4"):
            print(comuna)
            comuna = comuna.replace("'", "\\'")  # replace O'HIGGINS with O\'HIGGINS
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "__select2"))
            ).click()
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, f'[title*="Comuna: {comuna}"]')
                )
            ).click()

            for establecimiento in get_list_items("__select3", "__list5"):
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.ID, "__select3")
                    )
                ).click()
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            f'[title*="Establecimiento: {establecimiento}"]',
                        )
                    )
                ).click()

                ### download report
                # right click canvas
                canvas =WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.ID, "__uiview1canvas")
                    )
                )
                action = ActionChains(driver)
                action.context_click(canvas).perform()

                # click button that says "Export data"
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "//*[contains(text(), 'Export data...')]")
                    )
                ).click()

                # download the report
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, "//*[contains(text(), 'OK')]")
                    )
                ).click()

                # somehow wait until file is downloaded
                sleep(2)

                # move file, indexed by name
                file = os.listdir(downloads_path).pop()
                os.rename(f"{downloads_path}/{file}", f"{data_path}/edad_{region}_{servicio}_{comuna}_{establecimiento}.xlsx")


