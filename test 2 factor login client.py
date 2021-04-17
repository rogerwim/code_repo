import test1
import random
# for testing
tokens = [{'name': 'a', 'token': 'c2862fe145d9e4a1cb4fe9a790b32ea0da9c60f4b07f007be612005e3cfc03c5', 'pos': 0, 'id': 0}, {'name': 'b', 'token': 'dea4221bfde4654acdbce3367b9ef8a77df6ccfadd64ea3ced093d3b78c6cde4', 'pos': 0, 'id': 1}, {'name': 'c', 'token': '147f703e010745118d384c5c71b9f873f3e26d532ee3c5a2bcac5f45d9dff10e', 'pos': 0, 'id': 2}, {'name': 'd', 'token': 'f75eea71222db0ed953563f29aa55fa4c805c379b904caa733fb00561e84600a', 'pos': 0, 'id': 3}, {'name': 'e', 'token': '29fc2acfb540ea3b817fc74386edc055b1115093b22d0117d31e580290addf75', 'pos': 0, 'id': 4}, {'name': 'f', 'token': '84167e0c284a2f178a0191822a2cee68fb9b3c4cc8089ac8ff05abd16bee5b17', 'pos': 0, 'id': 5}, {'name': 'g', 'token': '1496d4445961c751d92ce2b872cca8386a27642b2c21dff83c6b2d68f44d1cdb', 'pos': 0, 'id': 6}, {'name': 'h', 'token': '7fab2c6660b6841d745c8f5ee424b81ddb5ebc9dbd7af14733355ed7a393719c', 'pos': 0, 'id': 7}, {'name': 'i', 'token': '1f785d9a22bca53d3ce2f76895d1357f863c8e0160ca8eb85562d3cfacd2a021', 'pos': 0, 'id': 8}, {'name': 'j', 'token': '4404119c80d906e708150b801ea34cb6639983ebf6187c27298e05277cf6a8a5', 'pos': 0, 'id': 9}]
blacklist = []
lookup_t = {}
def lookup(name):
    try:
        return tokens[lookup_t[name]]
    except KeyError:
        return {}
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
    token = test1.gen()
    tokens.append({"name":name,"token":token,"pos":0,"id":0})
    #print("sync token: ", token)
    fix_ids()
    rebuild_lookup()
def set_token(name):
    token = lookup(name)
    test1.init(token["token"])
    test1.next_block(token["pos"])
def gen_next(name,count,hide_seed=True):
    global tokens
    token = lookup(name)
    set_token(name)
    tokens[token["id"]]["pos"] += 1
    return test1.next_block(count,hide_seed)
def get_token():
    name = input("name to generate token for: ")
    token = lookup(name)
    pos = int(input("id to generate token for: "))
    if pos not in blacklist:
        token["pos"] = pos
        print(gen_next(name,1)[0][0])
        blacklist.append(pos)
    else:
        print("already used token")
def get_token_2(name,pos,hide):
    token = lookup(name)
    token["pos"] = pos
    print(gen_next(name,1,hide)[0])
    token["pos"] = pos
    return gen_next(name,1,hide)[0]
def get_sync_token(name):
    global blacklist
    if not blacklist == []:
        print(max(blacklist))
        sync_token = get_token_2(name,max(blacklist),False)[1]
        blacklist = []
        lookup(name)["token"] = sync_token
        print("sync token:",sync_token)
    else:
        sync_token = get_token_2(name,0,False)[1]
        blacklist = []
        lookup(name)["token"] = sync_token
        print("sync token:",sync_token)
def main():
    global lookup_t
    print("1: make new account")
    print("2: generate sync token")
    print("3: login with an existing account")
    print("4: list accounts")
    print("5: delete account")
    print("6: rebuild lookup table and fix broken id's")
    print("7: reset lookup table and id's")
    a = input("enter choice: ")
    if a == '1':
        name = input("name to make account for: ")
        new(name)
        print("done")
    elif a == '2':
        name = input("name to get sync token for: ")
        get_sync_token(name)
        print("done")
    elif a == '3':
        get_token()
        print("done")
    elif a == '4':
        for token in tokens:
            print("name:",token["name"])
        print("done")
    elif a == '5':
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
    elif a == '6':
        fix_ids()
        rebuild_lookup()
    elif a == '7':
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
    main()
