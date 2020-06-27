#pylint: disable=too-many-function-args
import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 120

class CreciSpider(scrapy.Spider):
    name = 'creciSpider'
    start_urls = ['https://servico.creci-rj.gov.br/spw/ConsultaCadastral/TelaConsultaPubCompleta.aspx']

    def __init__(self):
        cap = DesiredCapabilities().FIREFOX
        cap["marionete"] = False
        opts = Options()
        opts.headless = True
        self.driver = webdriver.Firefox(capabilities=cap, options=opts)

    def parse(self, response):
        self.driver.get(response.url)

        tipoPesquisa = self.driver.find_element_by_id('cbousuario_I')
        tipoPesquisa.send_keys("Profissional")


        tipoBusca = self.driver.find_element_by_id('ContentPlaceHolder1_Callbackconsulta_cboTipoBusca_I')
        tipoBusca.send_keys("Num. Registro")

        cidade = self.driver.find_element_by_id('ContentPlaceHolder1_Callbackconsulta_cboCidade_I')
        cidade.send_keys("RIO DE JANEIRO")

        try:
            selectedCidade = WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_Callbackconsulta_cboCidade_DDD_L_LBI370T0'))
            )
            selectedCidade.click()

            WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
                EC.invisibility_of_element((By.XPATH, "//div[@class='spinner']"))
            )

            pesquisarBtn = self.driver.find_element_by_id('ContentPlaceHolder1_Callbackconsulta_btnConsultaTotal')
            pesquisarBtn.click()

            WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
                EC.invisibility_of_element((By.XPATH, "//div[@class='spinner']"))
            )

            rowsPerPage = self.driver.find_element_by_id("ContentPlaceHolder1_Callbackconsulta_gridConsulta_DXPagerBottom_DDB")
            rowsPerPage.click()

            comboRowsPerPage = WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_Callbackconsulta_gridConsulta_DXPagerBottom_PSP_DXME_"))
            )
            select200 = comboRowsPerPage.find_element_by_xpath('//li[div[span[contains(text(), "200")]]]')
            select200.click()

            WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
                EC.invisibility_of_element((By.XPATH, "//div[@class='spinner']"))
            )

            imgNext = self.driver.find_element_by_xpath("//img[@class='dxWeb_pNext_MetropolisBlue']")
            rowsPerPage = imgNext.find_element_by_xpath('..')

            while rowsPerPage is not None:
                rows = self.driver.find_elements_by_class_name("dxgvDataRow_MetropolisBlue")
                for row in rows:
                    values = row.find_elements_by_class_name("letrasistema")
                    yield {
                        'no_registro': values[0].text,
                        'nome': values[1].text,
                        'categoria': values[2].text,
                        'categoria2': values[3].text,
                        'situacao': values[4].text
                    }
                rowsPerPage.click()
                WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
                    EC.invisibility_of_element((By.XPATH, "//div[@class='spinner']"))
                )
                imgNext = self.driver.find_element_by_xpath("//img[@class='dxWeb_pNext_MetropolisBlue']")
                rowsPerPage = imgNext.find_element_by_xpath('..')

        finally:
            self.driver.quit()