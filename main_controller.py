import back_modules as bm
import front_modules as fm

FILE_NAME='user_bank_DB'
db_controller = bm.DB_controller(FILE_NAME)
bank_api=None

dft=(False,)



while True:
    card=card_pin=dft
    print("(Press 'c' to exit the program)")
    while card[0] != True:
        card = fm.input_fnt('Pleas insert your card: ')
    if card[1] == 'c':
        break
    
    while card_pin[0] != True:
        card_pin = fm.input_fnt('Please enter the pin number: ')
    
    if bank_api:
        #api pin number authentication
        authentication = None
        if authentication == False :
            print('api authentication fail, Please try again')
            continue
    else:
        usr=bm.basic_user(card[1],card_pin[1],db_controller)
        card=card_pin=dft
        if usr.status[0] !=True:
            print(usr.status[1])
            continue
        else:
            while True:
                back_step = fm.account_select_fnt(usr)
                if back_step == True:
                    break
                
                while True:
                    print('selected account:',usr.select)
                    for i in usr.transaction_info:
                        print(i)
                    print('balance :',usr.balance)
                    back_step = fm.withdrawal_deposit_fnt(usr)
                    if back_step == True:
                        break
    del usr
            
            
        