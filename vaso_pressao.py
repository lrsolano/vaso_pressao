import tabelas as tb
import math

def main(padrao='n'):
    #definição dos bocais padrões
    bocais = {'entrada de fluido':[1,12], 'conexão':[1,3], 'dreno':[1,3],'inspeção':[1,3],'interface':[1,3],
            'saida agua':[1,7],'saida oleo':[1,8],'transmissor':[1,3],
            'saida gas':[1,14],'termopar':[1,14], 'conexao simples':[1,3],'bocal reserva':[1,5],
            'bocal respiro':[1,3],'alivio pressao':[1,3],'disp incendio':[1,4]}
    if padrao.lower() == 's':
        diametro_interno = 1500 #mm
        comprimento = 2400 #mm
        pressao = 30 #bar
        temperatura = 90
        camada_corrosao = 9 #mm
        vento = 15 #m/s
        capacidade = 15 #m^3
        oscilacao = 10 #celsius
        radiografia = 1 # 1 = total 2 = parcial 3 = não radiografado
        tipo = 1 #1 = cilindrico 2 = esferico casco
        tampo = 1 #1 = elipitico 2 = hemisferico
        material = 1 #1 A-285-C #A-515-60 #A-516-60
        densidade_fluido = 1.66
        n_coluna = 28
        
    # Entrada de dados pelo usuario
    else:
        tipo = int(input("Tipo de casco: 1-cilindrico 2-esferico: ")) #1 = cilindrico 2 = esferico casco
        #verifica o tipo para receber os parametros de cada
        if tipo == 1: 
            diametro_interno = float(input("Diametro interno: mm  ")) #mm
            comprimento = float(input("Comprimento: mm  ")) #mm
            tampo = int(input("Tipo de tampo: 1-eliptico 2-hemisferico: "))
        else:
            n_coluna = int(input("Defina o número de colunas: "))
            diametro_interno = float(input("Diametro interno: mm  ")) #mm
        pressao = float(input("Pressão: bar  "))#bar
        temperatura =  int(input("temperatura: °C  "))
        camada_corrosao =  float(input("Camada de corrosão:  mm  ")) #mm
        vento =  float(input("Velocidade do cento:  m/s ")) #m/s
        capacidade =  float(input("Capacidade: m^3  ")) #m^3
        oscilacao =  float(input("Oscilação temperatura: °C  ")) #celsius
        radiografia = int(input("Radiografia: 1-total 2-parcial 3-não radiografado: ")) # 1 = total 2 = parcial 3 = não radiografado
        
        material = int(input("Material utilizado: 1-A285c 2-A51560 3-A51660: ")) #1 A-285-C #A-515-60 #A-516-60
        densidade_fluido = float(input("Densidade do fluido: "))
        for boca in bocais:
            bocais[boca][1] = float(input("Dimensão do bocal {}:  pol  ".format(boca)))
            
    #Define a tensão do material a partir do tipo de material
    if material == 1:
         tensao_resultante= tb.a285c[temperatura]
    elif material == 2:
         tensao_resultante= tb.a51560[temperatura]
    elif material == 3:
        tensao_resultante= tb.a51660[temperatura]
    else:
         print("Material não identificado. Está sendo utilizado o aço A285c")
         tensao_resultante= tb.a285c[temperatura]
    #Define a constante de radiografia
    if radiografia == 1:
        E = 1
    elif radiografia == 2:
        E = 0.85
    elif radiografia == 3:
        E = 0.70
    else:
        print("Radiografia não identificada. Está sendo utilizada não Radiografado")
        E = 0,70
    #calcula os dados para o Tampo
    if tampo == 1 : #eliptico
        r_coroa = 0.9*(diametro_interno)
        r_junta = 0.18*(diametro_interno)
        h = diametro_interno/4
        espessura_tampo_m = ((pressao)*((diametro_interno)/(2*tensao_resultante*E - 0.2*pressao))+camada_corrosao)/10 #espessura minima
        t_corr = espessura_tampo_m*1.25 #espessura corrosão
        t_comercial = tb.espessura(t_corr) #define a chapa comercial para o tampo
        t_nominal = (t_comercial/1.25)/1000 #espessura nominal
        print("Espessura nominal tampo: {}mm".format(t_nominal*1000))
        PMTA = ((2*tensao_resultante*(10**6)*E*t_nominal)/(0.997*(diametro_interno/1000)+0.2*t_nominal))*(10**-5)
        fator_seguranca = PMTA/pressao
        print("Fator de segurança: {}".format(fator_seguranca))   
    elif tampo== 2:  #hemisferico
        r_coroa = (diametro_interno/2)
        r_junta = 8
        h = diametro_interno/2
        espessura_tampo_m = ((pressao)*((diametro_interno)/(2*tensao_resultante*E - 0.2*pressao))+camada_corrosao)/10 #espessura minima
        t_corr = espessura_tampo_m*1.25 #espessura corrosão
        t_comercial = tb.espessura(t_corr) #define a chapa comercial para o tampo
        t_nominal = (t_comercial/1.25)/1000 #espessura nominal
        print("Espessura nominal tampo: {}mm".format(t_nominal*1000))
        PMTA = ((2*tensao_resultante*(10**6)*E*t_nominal)/(0.997*(diametro_interno/1000)+0.2*t_nominal))*(10**-5)
        fator_seguranca = PMTA/pressao
        print("Fator de segurança: {}".format(fator_seguranca))
    else:
        print("Tampo não identificado")
        return False
    #calculo do casco
    if tipo == 1: #cilindrico
        t_casco = (((pressao*(diametro_interno/2))/(tensao_resultante*E - 0.6*pressao)) + camada_corrosao)/10 #espessura minima do casco
        t_casco_comercial = tb.espessura(t_casco) #espessura nominal do casco
        print("Espessura casco comercial: {}mm".format(t_casco_comercial))
        PMTA_casco = ((tensao_resultante*(10**6)*E*(t_casco_comercial/1000))/((diametro_interno/2000)+0.6*(t_casco_comercial//1000)))*(10**-5)
        fator_seguranca_casco =  PMTA_casco/pressao
        print("Fator segurança casco: {}".format(fator_seguranca_casco))
    elif tipo == 2: #esferico
        t_casco = (pressao*diametro_interno/2)/(tensao_resultante*E-0.2*tensao_resultante)/10  #espessura minima do casco
        t_casco_comercial = tb.espessura(t_casco) #espessura nominal do casco
        print("Espessura casco comercial: {}mm".format(t_casco_comercial))
        PMTA_casco = ((tensao_resultante*(10**6)*E*(t_casco_comercial/1000))/((diametro_interno/2000)+0.6*(t_casco_comercial//1000)))*(10**-5)
        fator_seguranca_casco =  PMTA_casco/pressao
        print("Fator segurança casco: {}".format(fator_seguranca_casco))
    else:
        print("Casco não especificado")
        return False
    #Calculo dos bocais
    if tipo == 1: #cilindrico
        esp_bocal_entrada = (((pressao*((bocais['entrada de fluido'][1])/2)*25.4)/(tensao_resultante*E - 0.4*pressao)) + camada_corrosao)/10 #espessura do bocal de entrada de fluido
        esp_bocal_entrada_comercial = tb.espessura(esp_bocal_entrada) #espessura comercial 
        print("Espesura bocal entrada: {}mm".format(esp_bocal_entrada_comercial))
        
        a1 = ((bocais['entrada de fluido'][1]*25.4)*espessura_tampo_m + 2*(t_nominal*1000)*esp_bocal_entrada_comercial)/(1000**2)#m² #area 1
        a2 = ((bocais['entrada de fluido'][1]*25.4)*(t_nominal*1000-espessura_tampo_m)-2*esp_bocal_entrada_comercial*(t_nominal*1000-espessura_tampo_m))/(1000**2)#m² #area 2
        a3 = (5*(t_nominal*1000)*(esp_bocal_entrada_comercial-esp_bocal_entrada))/(1000**2)#m² #area 3
        if (a2+a3)<a1: #verificando se precisa de anel de reforço no bocal de entrada de fluido
            a4 = a1-(a2+a3)+0.001#m
            L = ((a1+a2+a3)/(2*(esp_bocal_entrada_comercial/1000)))+0.001#m
            if (t_nominal*1000)>50:
                print("Não pode ter anel de reforço para o bocal de entrada")
            else:
                print("Anel de reforço entrada: {}mm".format(L*1000))
        for bocal in bocais: #Faz a iteração para cada tipo de bocal
            if bocal == 'entrada de fluido': #verifica se é o bocal de entrata e pula, pois já foi calculado
                continue
            esp_bocal_entrada = (((pressao*((bocais[bocal][1])/2)*25.4)/(tensao_resultante*E - 0.4*pressao)) + camada_corrosao)/10 #espessura minima para o bocal
            esp_bocal_entrada_comercial = tb.espessura(esp_bocal_entrada) #espessura comercial do bocal
            print("Espesura bocal {}: {}mm".format(bocal,esp_bocal_entrada_comercial))
            
            #calculo das aréas para verificação da necessidade do anel de reforço
            a1 = ((bocais[bocal][1]*25.4)*t_casco + 2*(t_casco_comercial)*esp_bocal_entrada_comercial)/(1000**2)#m² 
            a2 = ((bocais[bocal][1]*25.4)*(t_casco_comercial-t_casco)-2*esp_bocal_entrada_comercial*(t_casco_comercial-t_casco))/(1000**2)#m²
            a3 = (5*(t_casco_comercial)*(esp_bocal_entrada_comercial-esp_bocal_entrada))/(1000**2)#m²
            if (a2+a3)<a1:
                a4 = a1-(a2+a3)+0.001#m
                L = ((a1+a2+a3)/(2*(esp_bocal_entrada_comercial/1000)))+0.001#m
                if (t_casco_comercial)>50:
                    print("Não pode ter anel de reforço para o bocal de {}".format(bocal))
                else:
                    print("Anel de reforço {}: {}mm".format(bocal,L*1000)) 
    else: #esferico
        for bocal in bocais:  #Faz a iteração para cada tipo de bocal
            esp_bocal_entrada = (((pressao*((bocais[bocal][1])/2)*25.4)/(tensao_resultante*E - 0.4*pressao)) + camada_corrosao)/10 #espessura minima do bocal
            esp_bocal_entrada_comercial = tb.espessura(esp_bocal_entrada) #espessura comercial do bocal
            print("Espesura bocal {}: {}mm".format(bocal,esp_bocal_entrada_comercial))
            
            #verificação da necessidade do anel de reforço
            a1 = ((bocais[bocal][1]*25.4)*t_casco + 2*(t_casco_comercial)*esp_bocal_entrada_comercial)/(1000**2)#m²
            a2 = ((bocais[bocal][1]*25.4)*(t_casco_comercial-t_casco)-2*esp_bocal_entrada_comercial*(t_casco_comercial-t_casco))/(1000**2)#m²
            a3 = (5*(t_casco_comercial)*(esp_bocal_entrada_comercial-esp_bocal_entrada))/(1000**2)#m²
            if (a2+a3)<a1:
                a4 = a1-(a2+a3)+0.001#m
                L = ((a1+a2+a3)/(2*(esp_bocal_entrada_comercial/1000)))+0.001#m
                if (t_casco_comercial)>50:
                    print("Não pode ter anel de reforço para o bocal de {}".format(bocal))
                else:
                    print("Anel de reforço {}: {}mm".format(bocal,L*1000)) 
    #Pé de apoio
    if tipo == 1: #cilindrico
        #definição dos pés de apoio do casco
        b1 = (60*diametro_interno/2000)**0.5
        A = 0.2*(comprimento/1000)
        l_selas = (comprimento/1000)-2*A
        b2 = b1+(10*t_casco_comercial/1000)
        if tipo == 1 and vento < 100:
            teta = 110+(vento*0.6)
        else:
            teta = 170
        print("Teta: {}".format(teta))
        altura_min = (diametro_interno/2000)/3
        vol_casco = 2*3.14*(diametro_interno/2000)*(t_casco_comercial/1000)*(comprimento/1000)
        vol_tampo = 4*3.14*((((comprimento/1000)**(1.6075))*((h/1000)**(1.6075))+((comprimento/1000)**(1.6075))/3)**(1.6075))*t_nominal
        print("Volume do casco: {}".format(vol_casco))
        print("Volume do tampo: {}".format(vol_tampo))
        if A <= (diametro_interno/4000):
            pass
        y = diametro_interno/3000
        massa = (vol_casco+vol_tampo)*7680
        print("massa do conjunto: {}kg".format(round(massa),0))
        area_chapa = 6*2.4
        area_casco = vol_casco/(t_casco_comercial/100)
        numero_chapas = round(((area_casco/area_chapa)+0.5),0)
        print("Numero de chapas: {}".format(numero_chapas))
        peso = massa * 9.807
        reacao = peso/2
        #definição das constantes Kf e Kg
        if teta < 120:
            k = tb.k_interpo(120)
            k6 = tb.k2_interpo(120)
        elif teta > 165:
            k = tb.k_interpo(165)
            k6 = tb.k2_interpo(165)
        else:
            k = tb.k_interpo(teta)
            k6 = tb.k2_interpo(teta)
        forca = reacao*k
        if comprimento/(diametro_interno/2000) < 8:
            sf = -(reacao/(4*(t_casco_comercial/1000)*b2))-(12*k6*reacao*(diametro_interno/2000))/((comprimento/1000)*(t_casco_comercial/1000)**2)
            print("Sf: {}".format(sf))
        else:
            sf = -(reacao/(4*(t_casco_comercial/1000)*b2))-(3*k6*reacao*(diametro_interno/2000))/((2*t_casco_comercial/1000)**2)
            print("Sf: {}".format(sf))
        sa = 0.66*sf*-1
        print("Sa: {}".format(sa))
        #definição das nervuras
        t_alma = (3*forca)/((comprimento/2000)*sa)
        print("Espessura da alma: {}mm".format(t_alma*1000))
        nervuras = round((2*math.sin(teta*2*3.14/360)*(diametro_interno/2000))+0.5,0)
        print("Numero de nervuras: {}".format(nervuras))
        distancia = (2*math.sin(teta*2.14/360)*(diametro_interno/2000))/nervuras
        print("Distancias entre nervuras: {}".format(distancia))
    elif tipo == 2: #esferico
        comprimento = (diametro_interno/2000)*1.25
        coef_seguranca = 1.2
        vol_casco = ((4*3.14*(diametro_interno/2000)**3)/3)*t_casco_comercial
        massa = 7860*vol_casco
        print("Massa do vaso: {}kg".format(massa))
        peso_fluido = densidade_fluido*vol_casco*9.81
        peso = massa*9.81
        peso_colunas = (n_coluna*7850*(3.14*((0.4**2)-(0.37**2))/(4*comprimento))*9.81)
        peso_acessorios = 0.25*peso_colunas
        peso_cada_coluna = ((peso_fluido+peso+peso_colunas+peso_acessorios)*coef_seguranca)/n_coluna
        inercia = (peso_cada_coluna*(comprimento**2))/(2.046*(3.14**2)*(205*(10**9)))
        diametro_tubo = (64*inercia*3.14)**(1/4)+0.0001
        print("Diâmetro dos tubos: {}mm".format(diametro_tubo*1000))
        espessura_tubo = (diametro_tubo-((diametro_tubo**4)-64*inercia*3.14)**(1/4))/2
        print("Espessura dos tubos: {}mm".format(espessura_tubo*1000))
    else:
        print("Tipo não especificado")
        return False  
    
if __name__ == "__main__":
    opcao = input("Deseja executar com os dados padrões? s/n   ")
    main(opcao)
    