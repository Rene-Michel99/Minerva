import pymongo
from pymongo import MongoClient as MC

class DB:
    def __init__(self):
        client=MC()             #cria a conexão
        self.VDb=client.VeronikaDB   #conecta ao BD

    def getAge(self):
        info = self.VDb.Info
        age = info.find({"_id":"#dd880"})[0]
        return age["age"]

    def update_last_shutdown(self,date):
        info = self.VDb.Info
        data = info.find({"_id":"#dd880"})[0]
        info.update_one(data,{"$set":{"last_work":date}})


    def find_expense(self,data):
        Expenses=self.VDb.Expenses
        if Expenses.count_documents({'Data':data})>0:
            return True
        else:
            return False

    def insert_expenses(self,data):
        Expenses=self.VDb.Expenses
        if Expenses.estimated_document_count()==0:
            _id=Expenses.estimated_document_count()
            data['_id']=_id
            Expenses.insert_one(data)
        else:
            if Expenses.count_documents({'Data':data['Data']})>0:
                last_expense=Expenses.find_one({'Data':data['Data']})
                copy=Expenses.find_one({'Data':data['Data']})
                last_expense['Total de entrada']+=data['Entrada+']
                last_expense['Despesas total']+=data['Despesas total']
                last_expense['Quantia restante']-=data['Despesas total']
                last_expense['Despesas']+=data['Despesas']
                Expenses.update_one(copy,{"$set":last_expense})
            else:
                _id=Expenses.estimated_document_count()
                data['_id']=_id
                Expenses.insert_one(data)
    
    def get_next_weather(self,day):
        Weather=self.VDb.Weather
        x=Weather.find({'dia':{'$regex':day}})
        return x[0]

    def insert_in_weather(self,data,date_today):
        Weather=self.VDb.Weather
        _id=Weather.estimated_document_count()
        
        Weather.delete_many({})

        _id=Weather.estimated_document_count()
        Weather.insert_one({'_id':_id,'last_updated':date_today})
        for item in data:
            _id=Weather.estimated_document_count()
            item['_id']=_id
            Weather.insert_one(item)

    def get_last_upadte_weather(self):
        Weather=self.VDb.Weather
        updated=Weather.find()

        if updated==[]:
            return None
        else:
            for item in updated:
                if 'last_updated' in item:
                    return item['last_updated']

    def find_in_reminders(self,date):
        Reminders=self.VDb.Reminders    #acessa a coleção
        if Reminders.count_documents({'date':date})==0:
            return 0
        results=Reminders.find({'date':date})
        descrs=[]
        for result in results:
            descrs.append(result['descr'])
        return descrs

    def delete_in_reminders(self,date):
        Reminders=self.VDb.Reminders
        Reminders.delete_many({'date':date})

    def insert_in_reminders(self,date,descr):
        Reminders=self.VDb.Reminders
        index=Reminders.estimated_document_count()
        reminder={'_id':index,'date':date,'descr':descr}
        id=Reminders.insert_one(reminder).inserted_id
        print(id)

bd = DB()
bd.getAge()