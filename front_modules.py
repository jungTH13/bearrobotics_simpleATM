import back_modules as bm

dft=(False,)

def input_fnt(input_str:str='',login=False):
    #print("(Press 'c' to exit the program)")
    string = input(input_str)
    print()
    if len(string) == 0:
        return dft
    string=string.split()
    if len(string)>1:
        print('input is invalid')
        return (False,'input is invalid')
    else:
        #if string[0] == 'c':
        #    exit()
        return (True,string[0])
    
    
def account_select_fnt(usr:bm.basic_user):
    select_input=dft
    print(f"Please select an account to trade")
    for i in usr.accounts:
        print(f'{i}:',usr.accounts[i])
    while select_input[0] !=True:
        print("'p': previous step")
        select_input=input_fnt('Enter the desired account index: ')
        if select_input[0] ==True and select_input[1]=='p':
            return True
        
        if not select_input[1].isnumeric():
            print('Please enter a number')
            select_input=dft
        elif int(select_input[1]) in usr.accounts.keys():
            usr.select=int(select_input[1])
            return (True,'Account has been selected')
        else:
            print('Enter the wrong number')
            select_input=dft
            
def withdrawal_deposit_fnt(usr:bm.basic_user):
    select_input=dft
    print(f"1 : withdrawal, 2 : deposit")
    while select_input[0] != True:
        print("'p': previous step")
        select_input=input_fnt()
        if select_input[0] ==True and select_input[1]=='p':
            return True
        
        if not select_input[1].isnumeric():
            print('Please enter a number')
            select_input=dft
        elif int(select_input[1]) in [1,2]:
            if int(select_input[1]) ==1:
                amount=input_fnt('withdrawal amount: ')
                if amount[0] != True:
                    print(amount[1])
                else:
                    if (not amount[1].isnumeric()) or int(amount[1])<=0:
                        print('Be sure to enter a number above 0!')
                    else:
                        result=usr.withdrawal(int(amount[1]))
                        print(result[1])
            elif int(select_input[1]) ==2:
                amount=input_fnt('deposit amount: ')
                if amount[0] != True:
                    print(amount[1])
                else:
                    if (not amount[1].isnumeric()) or int(amount[1])<=0:
                        print('Be sure to enter a number above 0!')
                    else:
                        result=usr.deposit(int(amount[1]))
                        print(result[1])
        else:
            print('Enter the wrong number')
            select_input=dft