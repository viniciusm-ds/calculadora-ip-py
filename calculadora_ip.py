import streamlit as st  
import ipaddress  

#funcao que converte a mascara de subrede em CIDR
def mascara_para_cidr(mascara_subrede):
    try:
        #converte
        return ipaddress.IPv4Network(f"0.0.0.0/{mascara_subrede}").prefixlen
    except ValueError:
        return None

#funcao para calcular
def calcular_ip(endereco_ip, mascara_subrede):
    try:
        #remove as barras adicionais se tiver
        if mascara_subrede.startswith('/'):
            mascara_subrede = mascara_subrede[1:]
        
        #verifica se a mascara esta no formato original
        if '.' in mascara_subrede: #verifica formato tradicional
            mascara_subrede = mascara_para_cidr(mascara_subrede)
            if mascara_subrede is None:
                raise ValueError("Máscara de sub-rede inválida.")
        
        # Se já estiver no formato CIDR (como /20), não precisa fazer nada
        rede = ipaddress.IPv4Network(f'{endereco_ip}/{mascara_subrede}', strict=False)
        
        primeiro_host = str(list(rede.hosts())[0])
        ultimo_host = str(list(rede.hosts())[-1])
        endereco_rede = str(rede.network_address)
        endereco_broadcast = str(rede.broadcast_address)
        num_hosts = len(list(rede.hosts()))

        #calcula o número de sub-redes
        prefixo_original = rede.prefixlen 
        
        #identifica a classe do ip
        if rede.network_address >= ipaddress.IPv4Address('0.0.0.0') and rede.network_address <= ipaddress.IPv4Address('127.255.255.255'):
            classe = "A"
            prefixo_base = 8
        elif rede.network_address >= ipaddress.IPv4Address('128.0.0.0') and rede.network_address <= ipaddress.IPv4Address('191.255.255.255'):
            classe = "B"
            prefixo_base = 16
        elif rede.network_address >= ipaddress.IPv4Address('192.0.0.0') and rede.network_address <= ipaddress.IPv4Address('223.255.255.255'):
            classe = "C"
            prefixo_base = 24
        else:
            #classe desconhecida
            classe = "Desconhecida"
            prefixo_base = prefixo_original

        #calcula o número de sub-redes possíveis com base no prefixo original e a classe
        if prefixo_original > prefixo_base:
            subredes_possiveis = 2 ** (prefixo_original - prefixo_base)
        else:
            subredes_possiveis = 1 

        if rede.is_private:
            tipo_endereco = "Privado"
        else:
            tipo_endereco = "Público"

        #retorna o erro
        return {
            "endereco_ip": endereco_ip,
            "mascara_subrede": mascara_subrede,
            "endereco_rede": endereco_rede,
            "endereco_broadcast": endereco_broadcast,
            "primeiro_host": primeiro_host,
            "ultimo_host": ultimo_host,
            "num_subredes": subredes_possiveis,
            "num_hosts": num_hosts,
            "tipo_endereco": tipo_endereco,
            "classe_ip": classe
        }
    except ValueError as e:
        #trata algum erro
        return {"erro": str(e)}

def mostrar_resultados():
    endereco_ip = st.text_input("Digite o Endereço IP", "172.16.50.100")
    mascara_subrede = st.text_input("Digite a Máscara de Subrede (ou CIDR, ex: /20)", "255.255.240.0")

    if st.button("Calcular"):
        #verifica se os campos foram preenchidos
        if endereco_ip and mascara_subrede:
            resultados = calcular_ip(endereco_ip, mascara_subrede)

            #identifica erro
            if "erro" in resultados:
                st.error(f"Erro: {resultados['erro']}")
            else:
                #exibindo resultados
                st.subheader("Resultados do Cálculo de IP")
                st.write(f"**Endereço IP**: {resultados['endereco_ip']}")
                st.write(f"**Máscara de Subrede**: {resultados['mascara_subrede']}")
                st.write(f"**Endereço de Rede**: {resultados['endereco_rede']}")
                st.write(f"**Endereço de Broadcast**: {resultados['endereco_broadcast']}")
                st.write(f"**Primeiro Host**: {resultados['primeiro_host']}")
                st.write(f"**Último Host**: {resultados['ultimo_host']}")
                st.write(f"**Número de Sub-redes**: {resultados['num_subredes']}")
                st.write(f"**Número de Hosts por Sub-rede**: {resultados['num_hosts']}")
                st.write(f"**Tipo de Endereço**: {resultados['tipo_endereco']}")
                st.write(f"**Classe do IP**: {resultados['classe_ip']}")

                if st.button("Calcular Novamente"):
                    st.experimental_rerun()

st.title("Calculadora de IP")

#resultados
mostrar_resultados()

#para testar
#pip install streamlit
#python3 -m streamlit run calculadora_ip.py
