import argparse
import back_modules as bm

FILE_NAME='user_bank_DB'
parser = argparse.ArgumentParser()


parser.add_argument('--card',type=str,default=None,help='card number')
parser.add_argument('--pin',default=None,type=str)
parser.add_argument('--account',default=None,type=str)
parser.add_argument('--name',default=None,type=str)
parser.add_argument('--year',default=None,type=int)

if __name__ == '__main__':
    args=parser.parse_args()
    db_controller=bm.DB_controller(FILE_NAME)
    if args.card!=None and args.pin!=None and args.name!=None and args.year!=None:
        result = db_controller.create_user(args.card,args.pin,args.name,args.year)
        print(result[1])
    else:
        print('Skip user creation')
        
    if args.card!=None and args.account != None:
        result = db_controller.create_account(args.card,args.account)
        print(result[1])
    else:
        print('Skip account creation')