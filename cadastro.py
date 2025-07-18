import streamlit as st
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# ====== CONFIGURAÇÕES ======
chrome_path = r"D:\Lumnis\vscodelumnis\Criar emails automatico\ungoogled-chromium-138.0.7204.142-1_Win64\chrome.exe"
senha_padrao = "@LUMNIS2025"
url_registro = "https://lumnis.app.cativa.digital/auth/register"

# ====== INTERFACE ======
st.set_page_config(page_title="Cadastro na Comunidade Lumnis", layout="centered")
st.title("Cadastro de Usuários na Comunidade Lumnis")
st.write("Cole abaixo os nomes e e-mails (um por linha):")

# Entrada de texto
entrada = st.text_area("Exemplo: Milton Rosa miltonluizrosa62@gmail.com", height=200)

# Processa entrada e mostra preview
usuarios = []
if entrada.strip():
    for linha in entrada.strip().split("\n"):
        partes = linha.strip().split()
        if len(partes) < 2:
            continue
        email = partes[-1]
        nome_completo = " ".join(partes[:-1])
        nomes = nome_completo.split()
        if len(nomes) < 2:
            continue
        usuarios.append({
            "nome": nomes[0],
            "sobrenome": " ".join(nomes[1:]),
            "email": email
        })

    # Preview
    st.subheader("Usuários extraídos:")
    for u in usuarios:
        st.markdown(f"- **{u['nome']} {u['sobrenome']}** — {u['email']}")

# Botão para cadastrar
if st.button("Cadastrar usuários"):
    if not usuarios:
        st.warning("Nenhum usuário válido encontrado.")
    else:
        st.info("Iniciando o processo de cadastro...")

        # Inicia navegador
        options = uc.ChromeOptions()
        options.binary_location = chrome_path
        driver = uc.Chrome(headless=False, options=options)

        for user in usuarios:
            try:
                st.write(f"➡️ Cadastrando: **{user['nome']} {user['sobrenome']}**")

                driver.get(url_registro)
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

                st.success(f"✅ {user['email']} cadastrado com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao cadastrar {user['email']}: {str(e)}")

        driver.quit()
        st.success("🎉 Cadastro finalizado!")

        # Gera mensagens de boas-vindas por usuário
        st.subheader("Mensagens de boas-vindas para copiar e enviar:")

        for user in usuarios:
            mensagem = f"""\
Olá! 👋

Seu acesso à Comunidade Lumnis foi criado com sucesso.
Use os dados abaixo para fazer login:

E-mail: {user['email']}
Senha: {senha_padrao}

🌐 Acesse agora:
https://lumnis.app.cativa.digital/

⚠️ Recomendamos que você altere sua senha após o primeiro acesso.
Bem-vindo(a) à Lumnis! 🚀
"""
            with st.expander(f"Mensagem para {user['email']}"):
                st.code(mensagem, language="markdown")
