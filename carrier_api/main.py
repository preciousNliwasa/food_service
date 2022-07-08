from fastapi import FastAPI
import requests
import phonenumbers
from phonenumbers import carrier

app = FastAPI(title = 'Carrier')

    
@app.get('/')
async def home():
    return {'hello'}

def env():
    
    customers = requests.get(url = 'https://x8hokg.deta.dev/get_customers/')
    
    phones = []
    
    for i in  range(len(customers.json()['_items'])):
        phones.append(customers.json()['_items'][i]['Phone Number'])

    phone_ = []
    
    for i in phones:
        phone_.append(phonenumbers.parse(i.split(':')[1]))
        
    network = []
    
    for i in phone_:
        network.append(carrier.name_for_number(i,'en'))
    
    return network

@app.get('/labels')
async def labels():
    
    return env()

