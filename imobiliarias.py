# pylint: disable=too-many-function-args
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 120

name = 'imobiliariasSpider'
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

with open('imobiliarias.csv', 'w') as csvfile:
    w = csv.DictWriter(csvfile, fieldnames=[
        'numero_registro',
        'nome',
        'situacao_cadastral',
        'endereco',
        'bairro',
        'cidade',
        'cep',
        'telefone',
        'responsavel_tecnico'
    ])
    w.writeheader()

    driver.get(start_urls[0])

    selectTipoPesquisa = driver.find_element_by_id('cbousuario_B-1')
    selectTipoPesquisa.click()
    comboTipoPesquisa = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.ID, "cbousuario_DDD_L_LBT"))
    )
    selectPJ = comboTipoPesquisa.find_element_by_xpath("//tr[td[contains(text(), 'Pessoa Jurídica')]]")
    selectPJ.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.invisibility_of_element((By.ID, "ContentPlaceHolder1_Callbackconsulta_LPV"))
    )

    selectTipoBusca = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_Callbackconsulta_cboTipoBusca2_I"))
    )
    selectTipoBusca.click()
    comboTipoBusca = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.ID, "ContentPlaceHolder1_Callbackconsulta_cboTipoBusca2_DDD_L"))
    )
    select_cnpj = comboTipoBusca.find_element_by_id("ContentPlaceHolder1_Callbackconsulta_cboTipoBusca2_DDD_L_LBI2T0")
    select_cnpj.click()

    cidade = driver.find_element_by_id('ContentPlaceHolder1_Callbackconsulta_cboCidade_I')
    cidade.send_keys("RIO DE JANEIRO")

    pesquisarBtn = driver.find_element_by_id('ContentPlaceHolder1_Callbackconsulta_btnConsultaTotal_CD')
    pesquisarBtn.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.invisibility_of_element((By.XPATH, "//div[@class='spinner']"))
    )

    rows_per_page = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_Callbackconsulta_dtconsultaempresa_PGT_PSI"))
    )
    rows_per_page.click()

    combo_rows_per_page = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.ID, "ContentPlaceHolder1_Callbackconsulta_dtconsultaempresa_PGT_PSP_DXME_"))
    )
    select20 = combo_rows_per_page.find_element_by_xpath('//li[div[span[contains(text(), "20")]]]')
    select20.click()

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.invisibility_of_element((By.ID, "ContentPlaceHolder1_Callbackconsulta_dtconsultaempresa_LPV"))
    )

    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.invisibility_of_element((By.ID, "ContentPlaceHolder1_Callbackconsulta_dtconsultaempresa_LD"))
    )

    img_next = driver.find_element_by_xpath("//img[@class='dxWeb_pNext_MetropolisBlue']")
    rows_per_page = img_next.find_element_by_xpath('..')

    while rows_per_page is not None:
        table_results = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_Callbackconsulta_dtconsultaempresa_ICell"))
        )
        rows = table_results.find_elements_by_xpath(".//td[@class= 'dxdvItem_MetropolisBlue']/div")
        print(len(rows))
        for row in rows:
            values = row.find_elements_by_xpath(".//div/span")
            imobiliaria = {
                'numero_registro': values[0].text,
                'nome': values[1].text,
                'situacao_cadastral': values[3].text,
                'endereco': values[5].text,
                'bairro': values[7].text,
                'cidade': values[9].text,
                'cep': values[11].text,
                'telefone': values[13].text,
                'responsavel_tecnico': values[15].text
            }
            print(imobiliaria)
            w.writerow(imobiliaria)
        rows_per_page.click()
        WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.invisibility_of_element((By.ID, "ContentPlaceHolder1_Callbackconsulta_dtconsultaempresa_LPV"))
        )

        WebDriverWait(driver, DEFAULT_TIMEOUT).until(
            EC.invisibility_of_element((By.ID, "ContentPlaceHolder1_Callbackconsulta_dtconsultaempresa_LD"))
        )

        img_next = driver.find_element_by_xpath("//img[@class='dxWeb_pNext_MetropolisBlue']")
        rows_per_page = img_next.find_element_by_xpath('..')
    
driver.close()