import time
import streamlit as st
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

senha_padrao = "@LUMNIS2025"

st.title("Cadastro rápido de usuários")

texto = st.text_area("Cole aqui os nomes e e-mails (um por linha):", height=200)

if st.button("Cadastrar usuários"):
    usuarios = []
    for linha in texto.strip().split("\n"):
        partes = linha.strip().split()
        email = partes[-1]
        nome_completo = " ".join(partes[:-1])
        nomes = nome_completo.split()
        usuarios.append({
            "nome": nomes[0],
            "sobrenome": " ".join(nomes[1:]),
            "email": email
        })

    chrome_path = r"D:\Lumnis\vscodelumnis\Criar emails automatico\ungoogled-chromium-138.0.7204.142-1_Win64\chrome.exe"
    options = uc.ChromeOptions()
    options.binary_location = chrome_path
    driver = uc.Chrome(headless=False, options=options)

    for user in usuarios:
        driver.get("https://lumnis.app.cativa.digital/auth/register")
        time.sleep(4)

        driver.find_element(By.NAME, "email").send_keys(user["email"])
        driver.find_element(By.NAME, "firstName").send_keys(user["nome"])
        driver.find_element(By.NAME, "lastName").send_keys(user["sobrenome"])
        driver.find_element(By.NAME, "password").send_keys(senha_padrao)

        checkbox = driver.find_element(By.XPATH, "//label[contains(., 'Eu aceito os termos')]//input[@type='checkbox']")
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)

        registrar_btn = driver.find_element(By.XPATH, "//button[.//div[text()='Registrar']]")
        driver.execute_script("arguments[0].click();", registrar_btn)
        time.sleep(5)

    driver.quit()
    st.success("Todos os usuários foram cadastrados com sucesso!")
