#%%
import pandas as pd
from pandas.core.algorithms import value_counts
from pandas import to_numeric, to_datetime, get_dummies
pd.set_option('display.max_columns', None)

#%%
twingle1 = pd.read_csv('data/01_a_twingle_Seebrücke_2018-2019.csv',sep=';')
twingle2 = pd.read_csv('data/01_b_twingle_Seebrücke_2020_1.csv',sep=';')
twingle3 = pd.read_csv('data/01_c_twingle_Seebücke_2020_2.csv',sep=';')
twingle_dauer = pd.read_csv('data/02_twingle_Dauerspende.csv',sep=';')
twingle_Winter = pd.read_csv('data/03_twingle_Winterkampagne.csv',sep=';')
twingle_united = pd.read_csv('data/04_twingle_UnitedWeShare.csv',sep=';')
Fundbox_2020 = pd.read_csv('data/FundraisingBox_Donations_2020_non_anonymized.csv',sep=';',encoding='latin1')

#TODO Sort out going out payments from the bank transfert
#TODO Sort donation from grants (in bank transfert)
Transfert_1 = pd.read_excel('data/Kontoauszüge Seebrücke 2020.xlsx')
Transfert_2 = pd.read_excel('data/Kontoauszüge 2018-2019.xlsx',header=1)

#%%
# Select usefull twingle data
twingle_df = pd.concat([twingle1,twingle2,twingle3,twingle_dauer,twingle_Winter,twingle_united])
twingle_df = twingle_df[['timestamp','amount','recurring','donation_rhythm','user_city','user_country','user_email','user_company']]
twingle_df.columns = ['donated_at','amount','by_recurring','interval','city','country','email_address','company_name']

#%%
#Modify donation_rhythm to monthy interval
twingle_df['donation_rhythm'].value_counts()

twingle_df['donation_rhythm'] = twingle_df['donation_rhythm'].str.replace('yearly','12').copy()
twingle_df['donation_rhythm'] = twingle_df['donation_rhythm'].str.replace('quarterly','3').copy()
twingle_df['donation_rhythm'] = twingle_df['donation_rhythm'].str.replace('monthly','1').copy()
twingle_df['donation_rhythm'] = twingle_df['donation_rhythm'].str.replace('one_time','').copy()
twingle_df['donation_rhythm'] = to_numeric(twingle_df['donation_rhythm'],downcast='integer').copy()

#modify to timestamp
twingle_df['timestamp'] = to_datetime(twingle_df['timestamp'])

#%%
# Select usefull Fundbox data
Fundbox_df = Fundbox_2020[['donated_at','amount','by_recurring','interval','city','country','email_address','company_name']]
Fundbox_df['donated_at'] = to_datetime(Fundbox_df['donated_at']).copy()
#%%
#Merge Twingle and Fundbox data
#TODO Add Transfert data
df = pd.concat([twingle_df,Fundbox_df],ignore_index=True)
#%%
#Factorise email to annonymize the dataset 
cat = df['email_address'] 
codes, uniques = pd.factorize(cat)  
df['person_id'] = codes

#%%
#Clean the amount col 

Transfert_1['Betrag'] = Transfert_1['Betrag'].str.replace('Euro','')
Transfert_1['Betrag'] = Transfert_1['Betrag'].str.replace(' ','')
Transfert_1['Betrag'] = Transfert_1['Betrag'].str.replace(',','')
Transfert_1['Betrag'] = to_numeric(Transfert_1['Betrag'])

#%%
#Considering that only 15 person transferred money more than once, for simplicity, I will count every transfert as a one time donation
Transfert_1['Kontoinhaber*in'].value_counts()



#%%

#! Fundbox gives person_id
#Fundbox1 = pd.read_csv('data/05_FundraisingBox_Seebruecke_Spende.csv',sep=';')
#Fundbox2 = pd.read_csv('data/06_FundraisingBox_Seebuecke_donations.csv',sep=';')
#Fundbox3 = pd.read_csv('data/07_FundraisingBox_Seebruecke_foerdern_Newsletter.csv',sep=';')
#Fundbox4 = pd.read_csv('data/08_FundraisingBox_Seebruecke_Winterkampagne.csv',sep=';')
#Fundbox5 = pd.read_csv('data/09_FundraisingBox_Seebruecke_winter_donation_campaign.csv',sep=';')
#! Strange one
#Fundbox6 = pd.read_csv('data/10_FundraisingBox_Seebruecke_foerdern_Social_Media.csv',sep=';',encoding='cp1252')
#Fundbox7 = pd.read_csv('data/11_FundraisingBox_Seebruecke_foerdern_der_freitag.csv',sep=';')