#pylint: disable=too-many-function-args
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 120

name = 'creciSpider'
start_urls = ['https://servico.creci-rj.gov.br/spw/ConsultaCadastral/TelaConsultaPubCompleta.aspx']

profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True
profile.assume_untrusted_cert_issuer = False
profile.set_preference('security.tls.version.max', 2)
profile.set_preference('security.tls.version.min', 1)
cap = DesiredCapabilities().FIREFOX
cap["marionete"] = False
opts = Options()
opts.headless = True
driver = webdriver.Firefox(
    firefox_profile=profile,
    capabilities=cap,
    options=opts
)

driver.get(start_urls[0])

tipoPesquisa = driver.find_element_by_id('cbousuario_I')
tipoPesquisa.send_keys("Profissional")

tipoBusca = driver.find_element_by_id('ContentPlaceHolder1_Callbackconsulta_cboTipoBusca_I')
tipoBusca.send_keys("Num. Registro")

cidade = driver.find_element_by_id('ContentPlaceHolder1_Callbackconsulta_cboCidade_I')
cidade.send_keys("RIO DE JANEIRO")

try:
    selectedCidade = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_Callbackconsulta_cboCidade_DDD_L_LBI370T0'))
    )
    selectedCidade.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.invisibility_of_element((By.XPATH, "//div[@class='spinner']"))
    )

    pesquisarBtn = driver.find_element_by_id('ContentPlaceHolder1_Callbackconsulta_btnConsultaTotal')
    pesquisarBtn.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.invisibility_of_element((By.XPATH, "//div[@class='spinner']"))
    )

    rowsPerPage = driver.find_element_by_id("ContentPlaceHolder1_Callbackconsulta_gridConsulta_DXPagerBottom_DDB")
    rowsPerPage.click()

    comboRowsPerPage = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_Callbackconsulta_gridConsulta_DXPagerBottom_PSP_DXME_"))
    )
    select200 = comboRowsPerPage.find_element_by_xpath('//li[div[span[contains(text(), "200")]]]')
    select200.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.invisibility_of_element((By.XPATH, "//div[@class='spinner']"))
    )

    imgNext = driver.find_element_by_xpath("//img[@class='dxWeb_pNext_MetropolisBlue']")
    rowsPerPage = imgNext.find_element_by_xpath('..')

    while rowsPerPage is not None:
        rows = driver.find_elements_by_class_name("dxgvDataRow_MetropolisBlue")
        for row in rows:
            values = row.find_elements_by_class_name("letrasistema")
            imobiliaria = {
                'no_registro': values[0].text,
                'nome': values[1].text,
                'categoria': values[2].text,
                'categoria2': values[3].text,
                'situacao': values[4].text
            }
            print(imobiliaria)
        rowsPerPage.click()
        WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.invisibility_of_element((By.XPATH, "//div[@class='spinner']"))
        )
        imgNext = driver.find_element_by_xpath("//img[@class='dxWeb_pNext_MetropolisBlue']")
        rowsPerPage = imgNext.find_element_by_xpath('..')

finally:
    driver.quit()