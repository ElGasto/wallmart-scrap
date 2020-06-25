from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.maximize_window()
action = ActionChains(driver)

driver.get("https://www.walmart.com.ar/")

# Me muevo hacia el boton de categorias
categorias_button = driver.find_element_by_class_name("header-categories-nav")
action.move_to_element(categorias_button).perform()

# Guardo todas las subcategorias
walmart_categories = open('./walmart_categories.txt', 'w')
subcategorias = driver.find_elements_by_class_name(
    "header-categories-nav__categorie-parent")
for subcategoria in subcategorias:
    # print(subcategoria.find_element_by_tag_name('a').get_attribute('href'))
    walmart_categories.write(subcategoria.find_element_by_tag_name(
        'a').get_attribute('href')+'\n')


driver.close()

# #Identifico las categorias
# categorias_items = driver.find_elements_by_class_name("header-categories-nav__dropdown-item os-windows")
# #Por cada categoria:
# for categoria in categorias_items:
#     action.move_to_element(categoria).perform()


# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
