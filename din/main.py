from fastapi import FastAPI
from deta import Deta
import time
import numpy as np
import pandas as pd
import requests


app = FastAPI(title = 'Aladdinx API')

base = Deta()

response = {
            
            'asking for identity':['Am a piece of code written by a stupid person who goes by the name precious nliwasa,You want to contact him?,0996537633 thats his phone number'],
            'time of operation':['We operate 24 hours,but we deliver meals from 11 am to 1 pm and 6 pm to 7 pm'],
            'places of operation':['We operate around Chikanda and campus'],
            'HQ':['We are based in Mumba 5'],
            'how to register':['For registration,visit our website,by clicking www.sahara.com'],
            'compliment':[np.random.choice(['thanks','welcome','anytime'])],
            'complaint':['Sorry,I m not allowed to handle complaints yet,but if you want to make a complaint visit our official website www.sahara.com']
            
            }

average_time_for_delivery = {
        'chikanda rular':'30 minutes',
        'chikanda urban':'15 minutes',
        'mumba':'15 minutes',
        'makata':'20 minutes',
        'kanjedza':'20 minutes',
        'lubani':'30 minutes',
        'chilembwe':'10 minutes',
        'dunduzu':'5 minutes',
        'umodzi':'5 minutes',
        'sangala':'10 minutes',
        'chirunga':'30 minutes',
        'tchaka':'30 minutes',
        'mbelwa':'20 minutes',
        'shakespeare':'10 minutes',
        'khondowe':'5 minutes',
        'kenyatta':'40 minutes',
        'mulunguzi':'45 minutes',
        'kwacha':'25 minutes',
        'kamuzu':'10 minutes',
        'gweru':'10 minutes',
        'beit trust':'10 minutes',
        'kachere':'20 minutes',
        'chingwe':'20 minutes'
        
        }
        
        
wai = ''' def time_deplo():
    
    date1 = time.asctime()
    
    date1_split = date1.split(' ')
    
    time1 = date1_split[3].split(':')
    
    time1[0] = str(int(time1[0]) + 2)
    
    time_append =  time1[0] + ':' + time1[1] + ':' + time1[2]
    
    date1_split[3] = time_append
    
    date_final = date1_split[0] + ' ' + date1_split[1] + ' ' + date1_split[2] + ' ' + date1_split[3] + ' ' +date1_split[4]

    return date_final'''

def registered_if(phone_number):
    
    jso = requests.get(url = 'https://x8hokg.deta.dev/get_customers')
    db = pd.DataFrame(jso.json()['_items'])
    
    if phone_number in db['Phone Number'].values:
        
        response =  True
    
    else:
        
        response = False
    
    return response

def time_of_delivery(user):
    
    jso = requests.get(url = 'https://x8hokg.deta.dev/get_customers')
    db = pd.DataFrame(jso.json()['_items'])
    
    if registered_if(user) == True:        
        location_ = db.loc[db['Phone Number'] == user,['Location']]
        location_ = location_['Location'][0]
    
        return 'Your food will be delivered within {} from the time you will or have made an order'.format(average_time_for_delivery[location_])
    
    else:
        
        return 'Open an account first,to be able to make orders'

def about_payment(phone_number):
    
    if registered_if(phone_number) == True:
        
        response = 'log into your sahara account by visiting www.sahara.com, then deposit any amount you want starting with 10,000 kwacha'
        
        return response
    
    else:
        
        response = 'First of all you need to open a sahara account by visiting www.sahara,then deposit any amount you want starting with 10,000 kwacha once you log into your account'
        
        return response
        

def responses(category):
    
    return response[category]


def greeting_response(phone_number):
    
    night = list(range(19,24))
    morning = list(range(1,13))
    # afternoon = list(range(13,19)) 
    
    jso = requests.get(url = 'https://x8hokg.deta.dev/get_customers')
    db = pd.DataFrame(jso.json()['_items'])
    
    if time.ctime().split(' ')[3].split(':')[0] in night:
        
        if phone_number in db['Phone Number'].values:
            
            name_ = db.loc[db['Phone Number'] == phone_number,['Full Name']]
            name_ = name_['Full Name'][0]
            response = np.random.choice(['good evening {}, I am Aladin,a customer service for sahara restaurant.what can i do for you today'.format(name_),'Hii {}, I am Aladin,a customer service for sahara restaurant.what can i do for you today'.format(name_),'Hello {}, I am Aladin,a customer service for sahara restaurant.what can i do for you today'.format(name_)])
    
        else:
            
            response = np.random.choice(['good evening, I am Aladin,a customer service for sahara restaurant. You are not registered for our service yet,please visit www.sahara.com to register. But you can still use this platform to access some info about us','Hii , I am Aladin,a customer service for sahara restaurant. You are not registered for our service yet,please visit www.sahara.com to register. But you can still use this platform to access some info about us','Hello, I am Aladin,a customer service for sahara restaurant. You are not registered for our service yet,please visit www.sahara.com to register. But you can still use this platform to access some info about us'])
            
    elif time.ctime().split(' ')[3].split(':')[0] in morning:
        
        if phone_number in db['Phone Number'].values:
            
            name_ = db.loc[db['Phone Number'] == phone_number,['Full Name']]
            name_ = name_['Full Name'][0]
            response = np.random.choice(['good morning {}, I am Aladin,a customer service for sahara restaurant.what can i do for you today'.format(name_),'Hii {}, I am Aladin,a customer service for sahara restaurant.what can i do for you today'.format(name_),'Hello {}, I am Aladin,a customer service for sahara restaurant.what can i do for you today'.format(name_)])
    
        else:
            
            response = np.random.choice(['good morning, I am Aladin,a customer service for sahara restaurant. You are not registered for our service yet,please visit www.sahara.com to register. But you can still use this platform to access some info about us','Hii , I am Aladin,a customer service for sahara restaurant. You are not registered for our service yet,please visit www.sahara.com to register. But you can still use this platform to access some info about us','Hello, I am Aladin,a customer service for sahara restaurant. You are not registered for our service yet,please visit www.sahara.com to register. But you can still use this platform to access some info about us'])
            
    else:
        
        if phone_number in db['Phone Number'].values:
            
            name_ = db.loc[db['Phone Number'] == phone_number,['Full Name']]
            name_ = name_['Full Name'][0]
            response = np.random.choice(['good afternoon {}, I am Aladin,a customer service for sahara restaurant.what can i do for you today'.format(name_),'Hii {}, I am Aladin,a customer service for sahara restaurant.what can i do for you today'.format(name_),'Hello {}, I am Aladin,a customer service for sahara restaurant.what can i do for you today'.format(name_)])
    
        else:
            
            response = np.random.choice(['good afternoon, I am Aladin,a customer service for sahara restaurant. You are not registered for our service yet,please visit www.sahara.com to register. But you can still use this platform to access some info about us','Hii , I am Aladin,a customer service for sahara restaurant. You are not registered for our service yet,please visit www.sahara.com to register. But you can still use this platform to access some info about us','Hello, I am Aladin,a customer service for sahara restaurant. You are not registered for our service yet,please visit www.sahara.com to register. But you can still use this platform to access some info about us'])
            
    return response

@app.get('/')
async def home():
    
    return {'welcome'}

@app.get('/get_response/',tags = ['Responses'])
async def get_response(operation : str,user : str):
    
    if operation in list(response.keys()):
        return responses(operation)
    
    elif operation == 'greeting':
        
        return [greeting_response(user)]
    
    elif operation == 'if registered':
        
        if registered_if(user) == True:
            
            response_reg =  'Hey buddy, it seems you are registered'
            return [response_reg]
        
        else:
            
            response_reg = 'oops, It looks like you havent registered yet, Visit www.sahara.com for the registration'
            return [response_reg]
        
    elif operation == 'about payment':
        
        return [about_payment(user)]
    
    elif operation == 'food served': 
        
        jso = requests.get(url = 'https://x8hokg.deta.dev/get_food')
        db = pd.DataFrame(jso.json()['_items'])
        return ['Here is the table of meals we serve and their prices: \n .................................... \n' + str(db[['Food','Price']])]

    elif operation == 'on the menu':
        
        jso = requests.get(url = 'https://x8hokg.deta.dev/get_menu')

        db = pd.DataFrame(jso.json()['_items'])
        
        user_request_time = time.ctime()
        
        time_split  = user_request_time.split(' ')
        
        day =time_split[0]
        month = time_split[1]
        date = time_split[2]
        year = time_split[4]
        
        db2 = db.loc[db['Time'].str.startswith('{} {} {}'.format(day,month,date)) & db['Time'].str.endswith('{}'.format(year))]
    
        return ['Here is the menu : \n .................................... \n' + str(db2.reset_index()[['Food']])]
    
    elif operation == 'amount in account':
        
        if registered_if(user) == True:
            
            jso = requests.get(url = 'https://x8hokg.deta.dev/get_customers')
            db = pd.DataFrame(jso.json()['_items'])
            
            jso2 = requests.get(url = 'https://x8hokg.deta.dev/account_balances')
            db2 = pd.DataFrame(jso2.json()['_items'])
        
            name_ = db.loc[db['Phone Number'] == user,['Full Name']]
            name_ = name_['Full Name'][0]
        
            db_balance_ = db2.loc[db2['Full Name'] == name_]
            db_balance_.Time = pd.to_datetime(db_balance_.Time)
                    
            db_balance2 = db_balance_.loc[db_balance_['Time'] == max(db_balance_.Time)]
            balance_ = db_balance2['Amount'].values[0]
            
            return ['{},your balance is {}'.format(name_,balance_)]
        
        else:
            
            return ['Sorry,you do not have an account yet']
        
    else:
        
        return [time_of_delivery(user)]
        
        
        
        
        