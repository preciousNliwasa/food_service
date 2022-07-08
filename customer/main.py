from fastapi import FastAPI,Form,File,UploadFile,responses
from deta import Deta,Drive
import time

app = FastAPI(title = 'General')

base = Deta()

customer_db = base.Base('customer_base')
account_db = base.Base('amount_in_account')
food_db = base.Base('sahara_food')
menu = base.Base('on_the_menu')
order_db = base.Base('ordering')

user_operations = base.Base('operation')

meal_photos = Drive('meal_pics')

wai = '''def time_deplo():
    
    date1 = time.ctime()
    
    date1_split = date1.split(' ')
    
    time1 = date1_split[3].split(':')
    
    time1[0] = str(int(time1[0]) + 2)
    
    time_append =  time1[0] + ':' + time1[1] + ':' + time1[2]
    
    date1_split[3] = time_append
    
    date_final = date1_split[0] + ' ' + date1_split[1] + ' ' + date1_split[2] + ' ' + date1_split[3] + ' ' +date1_split[4]

    return date_final'''

@app.get('/',tags = ['Home'])
async def home():
    return 'welcome'

@app.post('/create_customer/',tags = ['Customer'])
async def create_customer(full_name : str = Form(...),email : str = Form(...),phone_number : str = Form(...),location : str = Form(...)):
    
    return customer_db.put({'Full Name':full_name,'Email':email,'Phone Number':'whatsapp:+{}'.format(phone_number),'Location':location})

@app.get('/get_customers/',tags = ['Customer'])
async def get_customers():
    return customer_db.fetch()


@app.post('/account/',tags = ['Account'])
async def deposit(full_name : str = Form(...),amount : str = Form(...)):
    return account_db.put({'Full Name':full_name,'Amount':amount,'Time':time.asctime()})

@app.get('/account_balances/',tags = ['Account'])
async def account_balances():
    return account_db.fetch()

@app.post('/enter_food/',tags = ['Food'])
async def enter_food(food : str = Form(...),price : str = Form(...),description : str = Form(...)):
    
    return food_db.put({'Food':food,'Price':price,'Description':description})

@app.get('/get_food/',tags = ['Food'])
async def get_food():
    return food_db.fetch()

@app.put('/update_price/',tags = ['Food'])
async def update_food(food : str = Form(...),price : str = Form(...),description : str = Form(...),key : str = Form(...)):
    
    food_ = food_db.get(key)
    if food_:
        return food_db.put({'Food':food,'Price':price,'Description':description},key)
    
    return {'meal not found'}

@app.delete('/delete_meal_offered/{key}',tags = ['Food'])
async def deleting_menu_offered(key : str):
    specific = food_db.get(key)
    
    if specific:
        food_db.delete(key)
        return {'meal deleted'}
    
    return {'meal not available to delete'}

@app.post('/enter_meal_photo/',tags = ['Food'])
async def enter_meal_photo(file : UploadFile = File(...)):
    return meal_photos.put(file.filename,file.file)

@app.get('/get_meal_photos/',tags = ['Food'])
async def get_meal_photos():
    return meal_photos.list()

@app.get("/stream/{name}",tags = ['Food'])
async def stream_meal_photos(name):
    imag = meal_photos.get(name)
    return responses.StreamingResponse(imag.iter_chunks(),media_type ="image/jpg")

@app.delete('/delete_meal_photo/{name}',tags = ['Food'])
async def delete(name : str):
    imag = meal_photos.get(name)
    
    if imag:
        meal_photos.delete(name)
        return {'photo deleted'}
    
    return {'photo not available to delete'}

@app.post('/on_the_menu/',tags = ['Menu'])
async def on_the_menu(food : str = Form(...),key : str = Form(...)):
    
    meal_ = food_db.get(key)
    
    if meal_:
        
        return menu.put({'Food':food,'Time':time.ctime()})
        
    return {'add not allowed'}

@app.get('/get_menu/',tags = ['Menu'])
async def get_menu():
    return menu.fetch()

@app.delete('/delete_menu_meal/{key}',tags = ['Menu'])
async def deleting_menu_meal(key : str):
    specific = menu.get(key)
    
    if specific:
        menu.delete(key)
        return {'meal deleted'}
    
    return {'meal not available to delete'}

@app.post('/order/',tags = ['Order'])
async def order(phone_number : str = Form(...),food : str = Form(...),price : str = Form(...)):
    return order_db.put({'Phone Number':phone_number,'Food':food,'Price':price,'Time':time.ctime()})

@app.get('/get_orders/',tags = ['Order'])
async def get_orders():
    return order_db.fetch()

@app.post('/post_operations/',tags = ['Operations'])
async def post_operations(user : str = Form(...),message : str = Form(...),operation : str = Form(...)):
    return user_operations.put({'User':user,'Message':message,'Operation':operation,'time' : time.ctime()})
    
@app.get("/get_all_operations",tags = ['Operations'])
async def get_all():
    all_operations = user_operations.fetch()
    return all_operations