from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import pdb
import mysql.connector
from mysql.connector import Error
import asyncio


async def main():
    def create_connection(host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
            pass

        return connection

    def query(connection, query):
        cursor = connection.cursor()
        try:
            print(query)
            cursor.execute(query)
            connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")
            pass

    db = create_connection("localhost", "root", "", "walmart")
    #query(db, 'DELETE FROM `products` WHERE 1')

    driver = webdriver.Chrome()
    driver.maximize_window()
    action = ActionChains(driver)
    touch_action = TouchActions(driver)

    errors_file = open('./errors.txt', 'w', newline='')

    def scroll_down(driver):
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = driver.execute_script(
            "return document.body.scrollHeight")

        while True:
            print("Bajando")

            # Scroll down to the bottom.
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(5)

            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script(
                "return document.body.scrollHeight")

            if new_height == last_height:

                break

            last_height = new_height

    def scroll_down2(driver):
        time.sleep(1)
        page_1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/div/main/div/div/section/div[4]/div/div[3]/div[2]/ul/li[1]")))
        print(page_1)

        while True:
            print("Bajando")
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(2)

            if page_1.is_displayed():
                break

    walmart_categories = open('./walmart_categories.txt', 'r').readlines()
    for line in walmart_categories:
        print('Obteniendo productos de: ', line)

        driver.get(line)

        try:
            while True:
                # Cargar todos los items de la pagina
                scroll_down(driver)

                items = driver.find_element_by_css_selector(
                    '.prateleira.prat-qtd').find_elements_by_css_selector('div.prateleira>ul>li')

                # Realizar Acciones
                i = 0

                for producto in items:
                    i += 1
                    print(f'Prod: {i}')

                    try:
                        name = producto.find_element_by_css_selector(
                            'div.prateleira__item').get_attribute('title')
                    except:
                        name = ''

                    try:
                        category = driver.title.split('-')[0]
                    except:
                        category = ''

                    try:
                        brand = producto.find_element_by_css_selector(
                            'p.texto.brand').get_attribute('innerText')
                    except:
                        brand = ''

                    try:
                        vendor = producto.find_element_by_css_selector(
                            'div.product-field.product_field_169.product-field-type_1>ul>li').get_attribute('innerText')
                    except:
                        vendor = ''

                    try:
                        price = float(producto.find_element_by_css_selector(
                            'span.prateleira__best-price').text.replace(',', '.').replace('$', ''))
                    except:
                        price = 0

                    try:
                        img_url = producto.find_element_by_css_selector(
                            'div.prateleira__image img').get_attribute('src')
                    except:
                        img_url = ''

                    query(
                        db, f'INSERT INTO `products`(`name`, `category`, `brand`, `vendor`, `price`, `img_url`) VALUES ("{name}","{category}","{brand}","{vendor}",{price},"{img_url}")')

                # Voy un poco para arriba
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight-2000);")

                # Obtener Paginas
                pages = driver.find_elements_by_class_name('page-number')
                current_page = driver.find_element_by_class_name('pgCurrent')
                print('Se obtuvieron: ', len(items),
                      'en la pagina', current_page.text)

                # Checkeo si es la ultima pagina
                if len(pages) == int(current_page.text):
                    print('Categoria Terminada!')
                    break

                # Navego a la siguiente pagina
                next_page = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"/html/body/div[3]/div/main/div/div/section/div[4]/div/div[3]/div[2]/ul/li[contains(text(), '{str(int(current_page.text) + 1)}')]")))
                next_page.click()

                driver.implicitly_wait(5)

                print('Navegando a pagina', int(current_page.text) + 1)
        except Exception as err:
            print(err)
            errors_file.writelines(f'{line}')
            continue


asyncio.run(main())
