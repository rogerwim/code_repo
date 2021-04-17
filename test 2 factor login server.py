import test1
import random
import time
tokens = [{'name': 'internal', 'token': str(time.time()), 'pos': 0, 'id': 44330}]
lookup_t = {}
def lookup(name):
    return tokens[lookup_t[name]]
def fix_ids():
    global tokens
    print("fixing id's of accounts")
    print("current id's:")
    for token in tokens:
        print("id:",token["id"],"name:",token["name"])
    print("fixed id's:")
    for i in range(len(tokens)):
        tokens[i]['id'] = i
        print("id:",tokens[i]["id"],"name:",tokens[i]["name"])
def rebuild_lookup():
    global lookup_t
    print("old lookup table:",lookup_t)
    print("deleting lookup table")
    lookup_t = {}
    print("rebuilding lookup table")
    for  token in tokens:  
        print("found",token['name'],"with id",token['id'])
        lookup_t.update({token['name']:token['id']})
        print("lookup table:",lookup_t)
def new(name):
    global tokens
    global lookup_t
    token = input("enter sync token: ")
    lookup_t.update({name:len(tokens)})
    tokens.append({"name":name,"token":token,"pos":0,"id":len(tokens)})
def set_token(name):
    token = lookup(name)
    test1.init(token["token"])
    test1.next_block(token["pos"])
def gen_next(name,count,i,hide=True):
    global tokens
    token = lookup(name)
    tokens[token["id"]]["pos"] = i
    set_token(name)
    return test1.next_block(count,hide)
def randint(low,high):
    set_token('internal')
    tokens[0]['pos'] += 1
    return test1.randint(low,high,1)[0]
def check():
    name = input("name to login as: ")
    token = lookup(name)
    i = randint(1,10000)
    token2 = input("please provide token with id "+str(i)+": ")
    token1 = gen_next(name,1,i)[0][0]
    if token1 == token2:
        print("token correct")
    else:
        print("token wrong, expected:",token1)
def main():
    global lookup_t
    print("1: make new account")
    print("2: login with an existing account")
    print("3: list accounts")
    print("4: delete account")
    print("5: rebuild lookup table and fix broken id's")
    print("6: reset lookup table and id's")
    a = input("enter choice: ")
    if a == '1':
        name = input("name to make account for: ")
        new(name)
        print("done")
    elif a == '2':
        check()
        print("done")
    elif a == '3':
        for token in tokens:
            print("name:",token["name"])
        print("done")
    elif a == '4':
        name = input("name of account to delete: ")
        token = lookup(name)
        if not token == {}:
            print("deleting",token)
            token2 = tokens.pop(token["id"])
            if not token == token2 or not name == token['name'] or not name == token2['name']:
                print("TAMPERING DETECTED, ABORTING")
                exit()
        else:
            print("account not found")
        fix_ids()
        rebuild_lookup()
        print("done")
    elif a == '5':
        fix_ids()
        rebuild_lookup()
    elif a == '6':
        print("randomizing lookup table and id's")
        for i in range(len(tokens)):
            tokens[i]['id'] = random.randint(0,1000)
            print("id:",tokens[i]["id"],"name:",tokens[i]["name"])
        rebuild_lookup()
        for i in range(len(tokens)):
            tokens[i]['id'] = random.randint(0,1000)
            print("id:",tokens[i]["id"],"name:",tokens[i]["name"])    
    else:
        print("invalid option")
    main()
if __name__ == '__main__':
    fix_ids()
    rebuild_lookup()
    tokens[0]['token'] = gen_next("internal",1,0,False)[0][1]
    main()

        
