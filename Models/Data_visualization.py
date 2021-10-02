import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_df():
    raw_data={'names':['Nick','Ari','Ana','Simp','Nig'],'jan_ir':[1,2,3,4,5],'feb_ir':[2,5,7,9,10],'march_ir':[10,20,30,40,50]}
    df=pd.DataFrame(raw_data,columns=['names','jan_ir','feb_ir','march_ir'])
    df['total']=df['jan_ir']+df['feb_ir']+df['march_ir']
    print(df)

def create_bar_graph():
    col_count=3
    bar_width=0.1

    k_scores=(554,536,538)
    can_scores=(518,523,525)
    chi_scores=(613,570,580)
    fr_scores=(495,505,499)

    index=np.arange(col_count)

    k=plt.bar(index,k_scores,bar_width,alpha=0.3,label='Korea')
    c=plt.bar(index+bar_width,can_scores,bar_width,alpha=0.3,label='Canada')
    chi=plt.bar(index+bar_width*2,chi_scores,bar_width,alpha=0.3,label='China')
    ft=plt.bar(index+bar_width*3,fr_scores,bar_width,alpha=0.3,label='França')

    plt.xlabel("Subjects")
    plt.ylabel("Mean Score")
    plt.title("Test Scores by Country")
    plt.xticks(index+0.3/2, ("Mathematics","Reading","Science"))
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1,1),loc=2)
    plt.show()

create_bar_graph()

def create_lines_graph():
    years=[1,1000,1500,1600,1700,1750,1800,1850,1900,1950,1955,1960,1965,1970,1975]
    pops=[4.1,4.58,5.80,6.82,7.91,10.00,12.62,16.50,25.75,27.58,30.18,33.22,36.82,37.82,40.00]
    deaths=[1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,10.1,11.2,12.3,13.4,14.5,15.6]

    #plt.plot(years,pops,color=(0,1,0))
    #plt.plot(years,deaths,'--',color=(1,0,0))
    lines=plt.plot(years,pops,years,deaths)
    plt.grid(True)
    plt.xlabel("Populations in billion")
    plt.ylabel("Years")
    plt.title("Population Growth")
    plt.show()
    
def create_pie_graph():
    langs=['Python','C','C++','Ruby','Java','PHP','Perl','JavaScript']
    sizes=[33,10,48,15,52,23,7,35]
    separated=(0.1,0,0,0,0,0,0,0)

    plt.pie(sizes,labels=langs,autopct='%1.1f%%',explode=separated)
    plt.title("Languages most used")
    plt.show()
