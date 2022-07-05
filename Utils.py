import re
PRICE_CHART=[[65, 65, 70, 75],[12500, 13000, 15000, 17500]]
PRICE_BAND=[[500, 1000, 1500],[100000, 200000, 300000]]

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))
def has_point(inputString):
    return bool(re.search(r'[.]', inputString))

def PrepareMSG(Pre_Message_text):
    idx=Pre_Message_text.find(' ')
    if idx==-1:
        return None
    Message_text=Pre_Message_text[idx+1:]
    return Message_text
def removePoint(nl):

    str_new_price=''
    for n in nl[-1].split('.'):
        str_new_price=str_new_price+n
    # print(str_new_price)
    new_price=str_new_price
    return new_price



def regMessage(Chat_Id):
    print(f'''Mensaje Recibido
de: {Chat_Id}''')



def _rentability(old_price,currency,PRICE_CHART=PRICE_CHART,PRICE_BAND=PRICE_BAND):
    i_curr= 0 if currency=='USD' else 1
    
    if old_price<PRICE_BAND[i_curr][0]:
        final_price=old_price+PRICE_CHART[i_curr][0]

    elif old_price<PRICE_BAND[i_curr][1]:
        final_price=old_price+PRICE_CHART[i_curr][1]

    elif old_price<PRICE_BAND[i_curr][2]:
        final_price=old_price+PRICE_CHART[i_curr][2]

    else:
        final_price=old_price+PRICE_CHART[i_curr][3]

    return final_price


def _numericResponse(removed,nl,currency):

    if removed:
        final_price=_rentability(int(nl[-1]),currency)
        final_response=str(final_price) + ' ULTIMO'
        # ultimo+=1


    # 'print (int(nl[-1])+60 , nl[-1])
    # 'print(nl[-1])
    # nl[-1]=int(nl[-1])+60
    # 'print(nl[-1])
    else:
        final_price=_rentability(int(nl[-1]),currency)
        final_response=str(final_price)
        # libre+=1
    return final_response
# elif nl[-1].find('*ULT')!=-1:
#     print(nl[-1],nl[-2],nl[-3])
def eraseFooter():
    
    return True

def addFooter(Response_text_line):
    return Response_text_line
    pass

def manageFooter(new_response,last_line):
    new_footer='''
🔥A pedido con entrega de 3 a 5 días hábiles
📦 Equipos 100% NUEVOS en caja sellada.
📝 Garantia por 3 meses.
🌟Se retira por nuestra oficina en el San Juan o te lo enviamos a cualquier lugar del país. Transporte a coordinar
💳Formas de Pago:
    💸Pesos en efectivo (TC del día)
    💰Dolares en efectivo
    💎Criptomonedas (USDT +5%)'''

    for line in enumerate(new_response):
        print(line)
    
    return 0
def setCounters():
    new_response=[]
    Response_text_line=''
    ultimo=0
    libre=0
    todojunto=0
    usd_atras=0
    con_punto=0
    priced_lines=[]
    return new_response, Response_text_line, ultimo, libre, todojunto, usd_atras, con_punto, priced_lines

def presetTextByCurrency(Message_text, currency):
    New_Message_text = Message_text.replace('*','')
    New_Message_text = New_Message_text.replace('🔥','')
    New_Message_text = New_Message_text.replace('.-','')
    if currency=='USD':
        New_Message_text = New_Message_text.replace('USD','u$')
        New_Message_text = New_Message_text.replace('U$','u$')
    return  New_Message_text.splitlines()

def _getFirstPricedLine(priced_lines,new_response):
    spaces_counter=0
    if len(priced_lines)>1:    
        for i in range(priced_lines[0],priced_lines[1]):
            # print(new_response[i])
            if len(new_response[i])==0:
                spaces_counter+=1
        price_line_length=priced_lines[1]-(priced_lines[0]+spaces_counter)
        first_line=priced_lines[0]+1-(price_line_length)
        print(f'largo de línea:{price_line_length}, separados por:{spaces_counter} da un inicio en:{first_line}')
        return first_line
    else:
        return 1

