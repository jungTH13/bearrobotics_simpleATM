import sqlite3
import hashlib
import os
import datetime



class DB_controller():
    def __init__(self,file_name:str):
        self._conn=sqlite3.connect(os.path.join(os.getcwd(), file_name))
        self._cur=self._conn.cursor()
        self.__hash_fnt=hashlib.sha256()
        self.__file_name=file_name
        
        self._cur.execute(f"""CREATE TABLE IF NOT EXISTS {file_name}(
                                                card_number VARCHAR(16) PRIMARY KEY,
                                                pin_hash VARCHAR(64),
                                                name VARCHAR(50),
                                                year INT
                                                )
                                                """)
        self._cur.execute(f"""CREATE TABLE IF NOT EXISTS account(
                                                account_id VARCHAR PRIMARY KEY,
                                                card_number VARCHAR(16),
                                                balance INT,
                                                CONSTRAINT card FOREIGN KEY(card_number)
                                                REFERENCES {file_name}(card_number)
                                                )
                                                """)
        self._cur.execute("""PRAGMA foreign_keys=1 """)
        
    
    def time(self):
        T=datetime.datetime.now()
        t=str(T.year)
        for n in [T.month,T.day,T.hour,T.minute,T.second]:
            if n<10:
                t+='0'+str(n)
            else:
                t+=str(n)
        t+=f'.{T.microsecond}'
        
        return float(t)
    
    def authentication(self,card:str,hash:str,account=None):
        db_card = self._cur.execute(f"""select card_number,name from {self.__file_name} where pin_hash="{hash}" """).fetchone()
        if None == db_card:
            return (False,'pin code is wrong')
        else:
            if card == db_card[0]:
                if account == None:
                    accounts={n:{'account':d[0],'balance':d[1]} for n,d in enumerate(self._cur.execute(f"""select account_id,balance from account where card_number="{db_card[0]}" """).fetchall())}
                    return (True,[db_card[1],accounts])
                else:
                    assert type(account) == str
                    accounts=self._cur.execute(f"""select balance from account where card_number="{db_card[0]}" and account_id="{account}" """).fetchone()
                    if accounts == None:
                        return (False,'Account not found')
                    else:
                        return (True,{'balance':accounts[0]})
            else:
                return (False,'card number is wrong')
            
    def create_user(self,card:str,pin:int,name:str,year:int):
        try:
            self.__hash_fnt.update(pin.encode('utf-8'))
            pin_hash=self.__hash_fnt.hexdigest()
            self.__hash_fnt.update('0'.encode('utf-8'))
            self._cur.execute(f"insert into {self.__file_name} VALUES('{card}','{pin_hash}','{name}','{year}')")
        except Exception as err:
            self._conn.rollback()
            return (False,'User Creation Error'+', '+str(err))
        
        self._conn.commit()
        return (True,'User Creation Successful')
    
    def create_account(self,card:str,account_id:str):
        search=self._cur.execute(f"""select account_id from account where account_id={account_id} """).fetchone()
        search_card=self._cur.execute(f"""select card_number from {self.__file_name} where card_number={card} """).fetchone()
        if None != search:
            return (False,'exsts account_id')
        elif search_card ==None:
            return (False,'Card number does not exist')
        else:
            try:
                self._cur.execute(f"insert into account VALUES('{account_id}','{card}','{0}')")
            except Exception as err:
                self._conn.rollback()
                return (False,'account Creation Error'+', '+err)
            
            stats = self.__create_transaction(account_id)
            if stats[0] == False:
                self._conn.rollback()
                return stats
            else:
                self._conn.commit()
                return (True,'account Creation Successful')
        
    def __create_transaction(self,account_id:str):
        table_list=[x[0] for x in self._cur.execute("SELECT name FROM sqlite_master WHERE type='table' ").fetchall()]
        if account_id in table_list:
            return (False,'transaction Creation fail(id exsts)')
        else:
            self._cur.execute(f"""CREATE TABLE "{account_id}"(
                                                    transaction_id int PRIMARY KEY,
                                                    time FLOAT,
                                                    type VARCHAR(16),
                                                    withdrawal INT,
                                                    deposit INT,
                                                    balance INT
                                                    )
                                                    """)
            self._cur.execute(f"""insert into "{account_id}" VALUES(0,{self.time()},'deposit',null,null,{0})""")
            self._conn.commit()
            return (True,'transaction Creation Successful')
        
    def view_transaction(self,account:str,count=10):
        transaction_info = self._cur.execute(f"""select * from "{account}" order by transaction_id DESC limit {count} """).fetchall()
        return transaction_info
    
    def view_accounts(self,card:str):
        account_info={n:{'account':d[0],'balance':d[1]} for n,d in enumerate(self._cur.execute(f"""select account_id,balance from account where card_number="{card}" """).fetchall())}
        return account_info
    
    def withdrawal(self,card:str,pin:str,account:str,amount:int):
        state = self.authentication(card,pin,account)
        if state[0] == False:
            return (False,'authentication fail'+', '+state[1])
        else:
            last_transaction=self._cur.execute(f"""select transaction_id,balance from "{account}" order by transaction_id DESC limit 1 """).fetchone()
            if last_transaction[1] == state[1]['balance']:
                if last_transaction[1] >= amount:
                    self._cur.execute(f"insert into '{account}' VALUES('{last_transaction[0]+1}','{self.time()}','withdrawal',{amount},null,{last_transaction[1] - amount})")
                    self._cur.execute(f"""update account set balance = {last_transaction[1] - amount} where account_id={account} """)
                    self._conn.commit()
                    return (True,'transaction success')
                else:
                    return (False,'insufficient balance')
                
    def deposit(self,card:str,pin:str,account:str,amount:int):
        state = self.authentication(card,pin,account)
        if state[0] == False:
            return (False,'authentication fail'+', '+state[1])
        else:
            last_transaction=self._cur.execute(f"""select transaction_id,balance from "{account}" order by transaction_id DESC limit 1 """).fetchone()
            if last_transaction[1] == state[1]['balance']:
                self._cur.execute(f"insert into '{account}' VALUES('{last_transaction[0]+1}','{self.time()}','deposit',null,{amount},{last_transaction[1] + amount})")
                self._cur.execute(f"""update account set balance = {last_transaction[1] + amount} where account_id={account} """)
                self._conn.commit()
                return (True,'transaction success')

                
                
            
            
class user():
    def __init__(self, card:str, pin:str,db_controller:DB_controller):
        self._db_controller=db_controller
        self._state=self.info_authentication(card,pin)
        self._card=None
        self._accounts=None
        self.name=None
        
        if self._state[0] == False:
            self._accounts='authentication fail'
        else:
            self._card = card
            self.name=self._state[1][0]
            self._accounts=self._state[1][1]
            self._state=(True,'authentication success')
            
        
    def info_authentication(self, card:str, pin:str):
        if len(card)!=16 or sum([False if n.isnumeric() else True for n in card ]):
            return (False,'Card number error')
        if len(pin) >16 or sum([False if n.isnumeric() else True for n in card ]):
            return (False,'pin number error')
        
        hash_m=hashlib.sha256()
        hash_m.update(pin.encode('utf-8'))
        self._pin=hash_m.hexdigest()
        return self._db_controller.authentication(card,self._pin)
        
    
        
        
        
class basic_user(user):
    def __init__(self,card:str, pin:str,db_controller:DB_controller):
        self.view_count=10 #계좌 입출금 내역 조회 개수
        self._select=None #선택 계좌번호 정보 
        self._transaction_info=None #해당 계좌의 입출금 내역 정보
        self._balance=None
        
        super().__init__(card,pin,db_controller)
        self._status=self._state
        
        
        
    @property
    def status(self):
        return self._status
    
    @property
    def select(self):
        return self._select
    
    @property
    def transaction_info(self):
        self.info_update()
        return self._transaction_info
    
    @property
    def balance(self):
        self.info_update()
        return self._balance
    
    @property
    def accounts(self):
        self.info_update()
        return self._accounts
    
    @property
    def card(self):
        return self._card
    
    @select.setter
    def select(self,s:int):
        if s<len(self.accounts) and s>=0:
            self._select=self.accounts[s]['account']
            self.info_update()

    def info_update(self):
        if None != self._card:
            self._accounts = self._db_controller.view_accounts(self._card)
        if None != self._select: 
            self._transaction_info= self._db_controller.view_transaction(self._select,self.view_count)
            self._balance=self._transaction_info[0][-1]
        
    def withdrawal(self,amount:int):
        if self._select != None:
            if type(amount) != int:
                return (False,'not a number')
            state = self._db_controller.withdrawal(self._card,self._pin,self.select,amount)
            if state[0] == True :
                self.info_update()
                return state
            else:
                return state
        else:
            return (False,'not selected account')
    
    def deposit(self,amount:int):
        if self._select != None:
            if type(amount) != int:
                return (False,'not a number')
            state = self._db_controller.deposit(self._card,self._pin,self.select,amount)
            if state[0] == True :
                self.info_update()
                return state
            else:
                return state
        else:
            return (False,'not selected account')
        
        
        
    
            
    
        
    
    
    
