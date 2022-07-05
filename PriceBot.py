import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler , Filters
import re
from Utils import has_numbers, has_point, PrepareMSG, removePoint, regMessage, _rentability, _numericResponse, eraseFooter, addFooter, manageFooter, setCounters, presetTextByCurrency, _getFirstPricedLine

with open('PricingToken.txt','r') as f:
    TOKEN=f.read()
    f.close()
PRICE_CHART=[[65, 65, 70, 75],[12500, 13000, 15000, 17500]]
PRICE_BAND=[[500, 1000, 1500],[100000, 200000, 300000]]


def _ManageData(Message_text,currency):
    
    Response_text = presetTextByCurrency(Message_text, currency)
    
    new_response, Response_text_line, ultimo, libre, todojunto, usd_atras, con_punto, priced_lines = setCounters()
    footer_has_started= False
    for idx, line in enumerate(Response_text):
        nl=line.split()
        new_response.append(nl)
        removed=False
        
        if not footer_has_started:
      
            if len(nl)>0:
                # print(str(nl[-1]))
                if nl[-1].find('ULTIMO')!=-1:
                    # print(nl[-1])
                    nl.remove('ULTIMO')

                    removed=True
            
                
                if (nl[-1].isnumeric()):

                    new_response[-1][-1]=_numericResponse(removed,nl,currency)
                    priced_lines.append(idx)
                    libre+=1

                elif nl[-1].find('$')!=-1:
                    # print(nl[-1],nl[-1].find('u$'),len(nl[-1])-1)
                    if removed:
                        old_price=int(nl[-1][nl[-1].find('u$')+2:len(nl[-1])])
                        
                        new_price=_rentability(old_price, currency)
                        
                        new_response[-1][-1]='u$ '+str(new_price)+ ' ULTIMO'
                        priced_lines.append(idx)
                        ultimo+=1
                        todojunto+=1

                    else:
                        try:
                            if nl[-1].find('u$')!=-1:
                                old_price=int(nl[-1][nl[-1].find('u$')+2:len(nl[-1])])
                                new_price=_rentability(old_price, currency)
                                new_response[-1][-1]='u$ '+str(new_price)
                                priced_lines.append(idx)
                            elif nl[-1].find('$')!=-1:

                                if nl[-1].find('.')!=-1:
                                    new_price = removePoint(nl)

                                old_price=int(new_price[new_price.find('$')+1:len(new_price)])
                                new_price=_rentability(old_price, currency)
                                new_response[-1][-1]='$ '+str(new_price)
                                priced_lines.append(idx)
                            todojunto+=1

                        except ValueError:
                            try:
                                nl.remove('u$')
                                old_price=int(nl[-1])
                                new_price=_rentability(old_price, currency)
                                new_response[-1][-1]='u$ '+str(new_price)
                                priced_lines.append(idx)
                                usd_atras+=1
                            except ValueError:
                                # print(nl[-1].split('.'))
                                str_new_price=''
                                for n in nl[-1].split('.'):
                                    str_new_price=str_new_price+n
                                old_price=int(str_new_price)
                                new_price=_rentability(old_price, currency)
                                new_response[-1][-1]='u$ '+str(new_price)
                                priced_lines.append(idx)
                                con_punto+=1
                elif has_numbers(nl[-1]) and has_point(nl[-1]):
                    # print(nl[-1])
                    old_price=int(removePoint(nl))
                    new_price = _rentability(old_price, currency)
                    new_response[-1][-1]='u$ '+str(new_price)
                    priced_lines.append(idx)
                    con_punto+=1

                # elif nl[-1].find('*')!=-1 and nl[-1].find('USD')!=-1:
                #     new_price=int(nl[-1][nl[-1].find('USD')+3:len(nl[-1])-1])+Rentability
                #     new_response[-1][-1]='u$ '+str(new_price)
                # elif line.find('*USD ')!=-1:
                #     for w_idx, word in enumerate(nl):
                #         if word.find('USD')!=-1:
                #             nl[]
                


                    pass
                    
                elif str(nl[-1]) == 'HIGH-TECH_' or str(nl[-1]) == 'HIGH-TECH':
                    high_tech=True
                    new_response[-1][-1]='CRIPTO PLACE'
                
                elif str(nl[-1]) == 'Inmediata' or str(nl[-1]) == 'INMEDIATA' or str(nl[-1]) == 'Inmediata.' or str(nl[-1]) == 'INMEDIATA.':

                    if str(nl[-2]) == '▪️ENTREGA':
                        footer_has_started =eraseFooter()
                    else:
                        new_line=nl[0]+'A pedido con entrega de 3 a 5 días hábiles'
                        new_response[-1]=new_line.splitlines()
                elif str(nl[-1]) == 'CABA.':
                    new_line=nl[0]+' retira por nuestra oficina en el San Juan o te lo enviamos a cualquier lugar del país. Transporte a coordinar'
                    new_response[-1]=new_line.splitlines()
                elif str(nl[-1]) == 'interior.':
                    new_response[-1]=''
                


            if not footer_has_started:
                Response_text_line = Response_text_line + '\n ' + str(' '.join(new_response[-1]))
    
        
    
    first_line=_getFirstPricedLine(priced_lines,new_response)
    if footer_has_started:
        Response_text_line = Response_text_line + '''
🔥A pedido con entrega de 3 a 5 días hábiles
📦 Equipos 100% NUEVOS en caja sellada.
📝 Garantia de fábrica.
🌟Se retira por nuestra oficina en el San Juan o te lo enviamos a cualquier lugar del país. Transporte a coordinar
💳Formas de Pago:
    💸Pesos en efectivo (TC del día)
    💰Dolares en efectivo
    💎Criptomonedas (USDT +5%)'''
    else:
        Response_text_line= Response_text_line+'''💳Formas de Pago:
      💸Pesos en efectivo (TC del día)
      💰Dolares en efectivo
      💎Criptomonedas (USDT +5%)
    '''
    print(f'Encontrados: Ultimos:{ultimo}, Libres:{libre}, Todo Junto:{todojunto}, USD Arás:{usd_atras}, Separado por Puntos:{con_punto} listado de precios:{priced_lines} inicio: {first_line}')

    # newText= manageFooter(new_response,priced_lines[-1])
    return Response_text_line



def USD(update,context):
    Chat_Id=update.message.chat_id
    Pre_Message_text=update.message.text
    # print(Pre_Message_text)
    Message_text=PrepareMSG(Pre_Message_text)
    currency='USD'
    regMessage(Chat_Id)
    Response_text=_ManageData(Message_text,currency)
    bot.send_message(chat_id=update.message.chat_id,text=Response_text)

def Pesos(update,context):
    Chat_Id=update.message.chat_id
    Pre_Message_text=update.message.text
    # print(Pre_Message_text)
    Message_text=PrepareMSG(Pre_Message_text)
    currency='Pesos'
    regMessage(Chat_Id)
    Response_text=_ManageData(Message_text,currency)
    bot.send_message(chat_id=update.message.chat_id,text=Response_text)


# def Response(update,context):
#     Chat_Id=update.message.chat_id
#     Message_text=update.message.text
#     regMessage(Chat_Id)
#     Response_text=_ManageData(Message_text)
#     bot.send_message(chat_id=update.message.chat_id,text=Response_text)


def mayusculas(bot, update, args):
    texto_en_mayusculas = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=texto_en_mayusculas)


bot = telegram.Bot(token=TOKEN)
updater = Updater(bot.token,use_context=True)

dispatcher = updater.dispatcher

USDHandler= CommandHandler('USD', USD)
PesosHandler= CommandHandler('Pesos', Pesos)
dispatcher.add_handler(USDHandler)
dispatcher.add_handler(PesosHandler)

# Responses= MessageHandler(Filters.text, Response)
# start_handler = CommandHandler('start', start)

# dispatcher.add_handler(start_handler)

# mayusculas_handler = CommandHandler('mayusculas', mayusculas, pass_args=True)

# dispatcher.add_handler(mayusculas_handler)

updater.start_polling()