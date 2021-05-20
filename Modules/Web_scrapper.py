from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO

def get_name():
    url='https://www.youtube.com/watch?v=NkM4CL3vJ9A'
    r=requests.get(url)
    text=r.text
    name=text[text.find('\\"title\\":\\"')+12:]
    name=name[:name.find('\\"')]
    print(name)

def get_city():
    url = "https://www.meuip.com.br/tools-geo.php"
    r = requests.get(url)

    #if r.status_code==200:
    i = r.text.find('<form method="post">')+20
    text = r.text[i:]
    text = text[text.find("<br />")+8:]
    text = text[:text.find("<br />")-1]

    text = text.split("\n")[1:]

    return text[4]

def get_dados():
    search=input('Buscar por: ')
    params={'q':search}
    r=requests.get('http://www.bing.com/search',params=params)

    soup=BeautifulSoup(r.text,"html.parser")
    #results=soup.find("ol",{'id':'b_results'})
    links=soup.findAll('li',{'class':'b_algo'})
    print(links)

    for item in links:
        item_text=item.find('a').text
        item_href=item.find('a').attrs["href"]

        if item_text and item_href:
            print(item_text)
            print(item_href)
            '''
            try:
                print('Summary: ',item.find("a").parent.parent.find('p').text)
            except:
                pass'''
            children=item.children #ver todas as folhas
            for child in children:
                print(child)
            print()

def get_images():
    search=input('Buscar por: ')
    params={'q':search}
    r=requests.get('http://www.bing.com/images/search',params=params)

    soup=BeautifulSoup(r.text,"html.parser")
    links=soup.findAll('a',{'class':'thumb'})

    for item in links:
        try:
            img_obj=requests.get(item.attrs['href'])
            print(item.attrs['href'])
            title=item.attrs['href'].split('/')[-1]
            image=Image.open(BytesIO(img_obj.content))
            image.save('./Imagens/'+title,image.format)
        except:
            pass

def get_prices(search):
    params={'q':search}
    r=requests.get('https://www.zoom.com.br/search',params=params)

    soup=BeautifulSoup(r.text,"html.parser")
    links=soup.findAll('div',{'class':'cardBody'})
    links2=soup.findAll('div',{'class':'cardFooter'})
    index=0
    lista=[]
    for item in links:
        title=item.find('a').attrs['title']
        print(item.find('a').attrs['title'])
        price=str(item.find('span',{'class':'customValue'}))
        price=price[50:price.find('</span>')]

        link=str(links2[index].find('a',{'class':'merchantName'}))
        link=link[link.find('>')+1:link.find('</a>')]
        index+=1
        print(link)
        print(price)
        print()
        price=price.replace('R$ ','')
        if price.find('.')!=-1:
            price=price.replace('.','')
        lista.append((title,link,int(price)))
    return lista

def adequa(string):
    string=string[1:len(string)-1]
    new_string=''
    block_read=False
    for letter in string:
        if letter=='<':
            block_read=True
        elif letter=='>' and block_read:
            block_read=False
        elif not block_read:
            new_string=new_string+letter
    string=new_string
    new_string=''
    block_read=False
    for letter in string:
        if letter=='[':
            block_read=True
        elif letter==']' and block_read:
            block_read=False
        elif not block_read:
            new_string=new_string+letter

    return new_string

def convert_to_list(string):
    lista=[]
    string=string.replace('[','')
    string=string.replace(']','')
    st=''
    for letter in string:
        if letter!=',':
            st=st+letter
        else:
            lista.append(st)
            st=''
    return lista

def choosed_link(link):
    r=requests.get(link)

    soup=BeautifulSoup(r.text,"html.parser")
    texts=str(soup.findAll('p'))
    return adequa(texts)

def make_pretty(string):
    new_string=''
    count=0
    for letter in string:
        new_string+=letter
        count+=1
        if count==79:
            count=0
            new_string+='\n'
    return new_string

def try_search_in_another(search):
    params={'q':search}
    r=requests.get('http://www.bing.com/search',params=params)

    soup=BeautifulSoup(r.text,"html.parser")
    boxs=soup.findAll('li',{'class':'b_algo'})
    dic=[]
    for box in boxs:
        x={}
        x['link']=box.find('a').attrs['href']
        x['text']=box.find('p')
        dic.append(x)

    arq=open('Pesquisas/'+search+'.txt','w',encoding="utf-8")
    search=search.split()
    maior=0
    pesquisa=''
    for x in dic:
        #print(x['text'])
        string=choosed_link(x['link'])
        count=0
        for item in search:
            if string.find(item)!=-1:
                count+=1
        if count>maior:
            maior=count
            pesquisa=string
        arq.write('\n'+x['link']+'\n')
        arq.write(string+'\n')
    arq.close()
    return pesquisa

def search_in_another(search):
    for _ in range(1000):
        string=try_search_in_another(search)
        if string!='':
            return string

def get_on_wiki(search):
    url='https://pt.wikipedia.org/wiki/'+search.replace(' ','_')
    r=requests.get(url)

    soup=BeautifulSoup(r.text,"html.parser")
    links=soup.findAll('p')
    headlines=soup.findAll('span',{'class':'mw-headline'})
    headlines=adequa(str(headlines))
    headlines=convert_to_list(headlines) #encontrar um jeito de por na string


    string=str(links)
    string=adequa(string)

    arq=open('Pesquisas/'+search+'.txt','w',encoding="utf-8")
    arq.write(string)
    arq.close()

    if string.find('A Wikipédia não possui um artigo com este nome exato.')!=-1:
        print('Não existe na wikipedia')
        string=search_in_another(search)
        arq=open('Pesquisas/Best_'+search+'.txt','w',encoding="utf-8")
        arq.write(make_pretty(string))
        arq.close()

        arq=open('Pesquisas/'+search+'.txt','r',encoding="utf-8")
        text=arq.read()
        arq.close()

        arq=open('Pesquisas/'+search+'.txt','w',encoding="utf-8")
        arq.write(make_pretty(text))
        arq.close()

        

    return string[0:600+string[600:].find('.')+1]

def try_get_weather(location,more=False):
    url='http://www.bing.com/search'
    location='clima em '+location
    
    params={'q':location}
    
    r=requests.get(url,params=params)

    soup=BeautifulSoup(r.text,'html.parser')
    
    temperature_atual=str(soup.find('div',{'class':'wtr_currTemp b_focusTextLarge'}))
    temperature_max=str(soup.find('div',{'class':'wtr_high'}))
    temperature_min=str(soup.find('div',{'class':'wtr_low'}))
    clima=str(soup.find('div',{'class':'wtr_caption'}))
    umidade=str(soup.find('div',{'class':'wtr_currHumi'}))

    tomorrow=soup.find('div',{'class':'wtr_forecastDay wtr_noselect wtr_tab_sel'})
    next_days=soup.findAll('div',{'class':'wtr_forecastDay wtr_noselect'})

    data_next_days=[]

    string=tomorrow.attrs['aria-label']
    string=string.replace(' ','_')
    string=string.replace(',',' ')
    string=string.split()
    new_string={}
    ordem=['prob_chuva','máxima-mínima','clima','dia']
    for item in string:
        x=item.replace('_',' ')
        if x[0]==' ':
            x=x[1:]
        if x.find('Possibilidade')!=-1:
            x=x+'%'
                
        new_string[ordem.pop()]=x

    data_next_days.append(new_string)
    #dic={}
    for day in next_days:
        string=day.attrs['aria-label']
        string=string.replace(' ','_')
        string=string.replace(',',' ')
        string=string.split()
        new_string={}
        ordem=['prob_chuva','máxima-mínima','clima','dia']
        for item in string:
            x=item.replace('_',' ')
            if x[0]==' ':
                x=x[1:]
            if x.find('Possibilidade')!=-1:
                x=x+'%'
            new_string[ordem.pop()]=x
        
        data_next_days.append(new_string)

    temperature_atual=temperature_atual[temperature_atual.find('>')+1:]
    temperature_atual=temperature_atual[:temperature_atual.find('<')]+'° Celsius'

    temperature_max=temperature_max[temperature_max.find('<span>')+6:]
    temperature_max=temperature_max[:temperature_max.find('</span>')]+' Celsius'

    temperature_min=temperature_min[temperature_min.find('>')+1:]
    temperature_min=temperature_min[:temperature_min.find('<')]+' Celsius'

    clima=clima[clima.find('>')+1:]
    clima=clima[:clima.find('<')]

    umidade=umidade[umidade.find('>')+1:]
    umidade=umidade[:umidade.find('<')]
    umidade=umidade.replace(':',' é de ')

    st='A temperatura atual é de '+temperature_atual+', com uma máxima de '+temperature_max+' e mínima de '+temperature_min+', está '+clima+' e a '+umidade
    if not more:
        return st
    else:
        return data_next_days
    
def get_weather(location,more=False):
    response = ""
    for _ in range(0,50):
        try:
            response = try_get_weather('natal',more=more)
            return response
        except:
            pass
    return "O módulo de clima está desatualizado"

def get_news():
    url = "https://news.google.com/topics/CAAqLAgKIiZDQkFTRmdvSkwyMHZNR1ptZHpWbUVnVndkQzFDVWhvQ1FsSW9BQVAB?hl=pt-BR&gl=BR&ceid=BR%3Apt-419"
    r = requests.get(url)

    soup = BeautifulSoup(r.text,'html.parser')
    titles = soup.findAll({'h4':{'class':'ipQwMb ekueJc RD0gLb'}})
    news = []
    for i,title in enumerate(titles):
        news.append(title.text)
    return news

def get_only_temp(location):
    data = get_weather(location)
    data = data[data.find("atual")+11:data.find(",")-1]
    return data

def cotacao_moeda(moeda):
    url=''
    if moeda=='dólar':
        url='https://economia.uol.com.br/cotacoes/cambio/dolar-comercial-estados-unidos/'
    elif moeda=='euro':
        url='https://economia.uol.com.br/cotacoes/cambio/euro-uniao-europeia/'
    elif moeda=='libra':
        url='https://economia.uol.com.br/cotacoes/cambio/libra-esterlina-reino-unido/'

    r=requests.get(url)
    
    soup=BeautifulSoup(r.text,'html.parser')
    #cotacao=soup.findAll('span',{'class':'chart-info-val ng-binding'})
    cotacao=str(soup.find('input',{'name':'currency2'}))
    cotacao=cotacao[cotacao.find('value="')+7:cotacao.find('/>')-1]
    cotacao='A cotação do '+moeda+' é de '+cotacao
    return cotacao

def translate(search,lang):
    from selenium import webdriver
    from time import sleep

    if lang.lower()=='inglês':
        lang='en'
    elif lang.lower()=='espanhol':
        lang='es'
    elif lang.lower()=='italiano':
        lang='it'
    elif lang.lower()=='francês':
        lang='fr'

    options=webdriver.FirefoxOptions()
    options.add_argument('lang=pt-br')
    driver=webdriver.Firefox(executable_path=r'./geckodriver.exe')

    url="https://translate.google.com/?rlz=1C1PDZP_pt-BRBR814BR814&um=1&ie=UTF-8&hl=en&client=tw-ob#view=home&op=translate&sl=pt&tl="+lang+"&text="+search.replace(' ','%20')
    driver.get(url)

    sleep(15)

    elemento=driver.find_element_by_xpath('//span[@class="tlid-translation translation"]')
    elemento.find_element_by_xpath('..')

    translated=elemento.get_attribute('innerHTML')
    translated=translated[translated.find('>')+1:]
    translated=translated[:translated.find('<')]
    return translated

def get_distance_btw(partida,destino):
    from selenium import webdriver
    from time import sleep

    options=webdriver.FirefoxOptions()
    options.add_argument('lang=pt-br')
    driver=webdriver.Firefox(executable_path=r'./geckodriver.exe')

    driver.get('https://www.google.com.br/maps/dir///@-5.9226788,-35.2747188,15z')

    sleep(20)
    inputs=driver.find_elements_by_xpath('//input[@class="tactile-searchbox-input"]')
    inputs[0].click()
    inputs[0].send_keys(partida)

    sleep(5)
    inputs[1].click()
    inputs[1].send_keys(destino)

    sleep(5)
    search=driver.find_elements_by_xpath('//button[@class="searchbox-searchbutton"]')
    search[1].click()

    sleep(10)
    vias=driver.find_elements_by_xpath('//div[@class="section-directions-trip-description"]')
    index=0
    for via in vias:
        objects=via.find_element_by_xpath('..')
        children=objects.find_elements_by_xpath('.//*')
        for child in children:
            if child.get_attribute('class')=='section-directions-trip-numbers':
                x=child.find_element_by_xpath('..')
                x=str(x.get_attribute('innerHTML'))
                #print(x,'*')
                if x.find('span jstcache')!=-1 and x.find('"7.section-directions-trip-duration"')==-1:
                    tempo=x[x.find('span jstcache'):]
                    tempo=tempo[tempo.find('>')+1:]
                    tempo=tempo[:tempo.find('<')]

                    distance=x[:x.find(' km')]
                    distance=distance[::-1]
                    distance=distance[:distance.find('>')]
                    distance=distance[::-1]
                    distance=distance+' km'
                    print('tempo: ',tempo,distance,'de carro')
                elif x.find('"7.section-directions-trip-duration"')!=-1:
                    tempo=x[x.find('7.section-directions-trip-duration'):]
                    tempo=tempo[tempo.find('>')+1:]
                    tempo=tempo[:tempo.find('<')]

                    distance=x[:x.find(' km')]
                    distance=distance[::-1]
                    distance=distance[:distance.find('>')]
                    distance=distance[::-1]
                    distance=distance+' km'
                    print('tempo: ',tempo,distance,'a pé')
            else:
                x=child.find_element_by_xpath('..')
                if x.get_attribute('id')=='section-directions-trip-title-'+str(index):
                    y=x.find_element_by_xpath('..')
                    location=str(y.get_attribute('innerHTML'))
                    if location.find('via')!=-1:
                        location=location[location.find('via')+3:]
                        location=location[:location.find('</span>')]

                        location=location[location.find('>')+1:]

                        print('Via: ',location)
                    elif location.find('Trajeto mais rápido, com trânsito normal')!=-1:
                        location=location[location.find('Trajeto mais rápido, com trânsito normal'):]
                        location=location[:location.find('</span>')]

                        location=location[location.find('>')+1:]

                        print('Via: ',location)

        index+=1