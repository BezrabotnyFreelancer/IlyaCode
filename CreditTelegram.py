#Import libraries 
import datetime
import telebot
from telebot import types
import sqlite3

#Our token
token = '5586466061:AAF9ElE5pbYeQnPCSQ6D4EnBbtuubuE26Rw'
bot = telebot.TeleBot(token)

#Actions when user write start command
@bot.message_handler(commands=['start'])
def start(message):
    
    #Connect to our database
    conn = sqlite3.connect('Balance.db')
    cursor = conn.cursor()
    
    #Create table
    cursor.execute('CREATE TABLE IF NOT EXISTS MEMBER(ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID VARCHAR(50), FIRST_NAME VARCHAR(50), LAST_NAME VARCHAR(50))')
    conn.commit()
    
    #Select our user id for find hin in our table
    cursor.execute(f'SELECT USER_ID FROM MEMBER WHERE USER_ID = {message.chat.id}')
    
    if cursor.fetchone() is None:
        
        #Add user in table 
        cursor.execute('INSERT INTO MEMBER (USER_ID, FIRST_NAME, LAST_NAME) VALUES (?,?,?)', (message.chat.id, message.from_user.first_name, message.from_user.last_name))
        conn.commit()
        
        #Send welcome message
        bot.send_message(message.chat.id, text=f'Hello, {message.from_user.first_name} {message.from_user.last_name}')
    
    else:
        #Send welcome message, if user exists
        bot.send_message(message.chat.id, text=f'Hello, {message.from_user.first_name} {message.from_user.last_name}')
    
    #Close connection with database    
    conn.close()
    
#Manual for our user
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, text='/income and data - Add info about incomes in database, ex: /income 1000\n/expense and data - Add info about expenses in database, ex: /expense 1000\n/showincomes - Show options with incomes\n/showexpenses - Show options with expenses\n/incomessum - Show options for sum of incomes\n/averageincomes - Show options for average sum of incomes\n/countincomes - SHow options for count of incomes\n/expensessum - Show options for sum of expenses\n/averageexpenses - Show options for average sum of expenses\n/countexpenses - Show options for count of expenses')
                         
#Function for add information about user's income
@bot.message_handler(commands=['income'])
def income(message):
    
    #Connect to database
    conn = sqlite3.connect('Balance.db')
    cursor = conn.cursor()
    
    #Make variables consists from date and info about user's income
    income_data = message.text[8::]
    date = datetime.date.today()
    
    #Create table of incomes if not exists
    cursor.execute('CREATE TABLE IF NOT EXISTS INCOME(ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID VARCHAR(50), TOTAL VARCHAR(30), "DATE" DATE)')
    conn.commit()
    
    #Add main information in table
    cursor.execute('INSERT INTO INCOME(USER_ID, TOTAL, "DATE") VALUES (?,?,?)', (message.chat.id, income_data, date))
    conn.commit()
    
    #Close connection with database
    conn.close()
    
#Functio for add information about user's expenses
@bot.message_handler(commands=['expense'])
def expense(message):
    
    #Connect to database
    conn = sqlite3.connect('Balance.db')
    cursor = conn.cursor()
    
    #Create table of expenses if not exists
    cursor.execute('CREATE TABLE IF NOT EXISTS EXPENSE(ID INTEGER PRIMARY KEY AUTOINCREMENT, USER_ID VARCHAR(50), TOTAL VARCHAR(30), "DATE" DATE)')
    conn.commit()
    
    #Make variables consists from date and info about user's expense
    expense_data = message.text[9::]
    date = datetime.date.today()
    
    #Add main information in database
    cursor.execute('INSERT INTO EXPENSE(USER_ID, TOTAL, "DATE") VALUES (?,?,?)', (message.chat.id, expense_data, date))
    conn.commit()
    
    #Close connection with database
    conn.close()

#Make buttons for navigate in incomes table  
@bot.message_handler(commands=['showincomes'])
def show_incomes(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Total incomes', callback_data='Total incomes'))
    markup.add(types.InlineKeyboardButton(text='Incomes for 12 months', callback_data='Incomes for 12 months'))
    markup.add(types.InlineKeyboardButton(text='Incomes for 6 months', callback_data='Incomes for 6 months'))
    markup.add(types.InlineKeyboardButton(text='Incomes for 3 months', callback_data='Incomes for 3 months'))
    markup.add(types.InlineKeyboardButton(text='Incomes for 1 month', callback_data='Incomes for 1 month'))
    
    #Reply our markup in chat
    bot.send_message(
        message.chat.id,
        text='Period options',
        reply_markup=markup
    )
    
#Make buttons for navigate in expenses table
@bot.message_handler(commands=['showexpenses'])
def show_expenses(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Total expenses', callback_data='Total expenses'))
    markup.add(types.InlineKeyboardButton(text='Expenses for 12 months', callback_data='Expenses for 12 months'))
    markup.add(types.InlineKeyboardButton(text='Expenses for 6 months', callback_data='Expenses for 6 months'))
    markup.add(types.InlineKeyboardButton(text='Expenses for 3 months', callback_data='Expenses for 3 month'))
    markup.add(types.InlineKeyboardButton(text='Expenses for 1 month', callback_data='Expenses for 1 month'))
    
    #Reply our markup in chat
    bot.send_message(
        message.chat.id,
        text='Period otions',
        reply_markup=markup
    )
    
#Make buttons for send info about total sum of income in different period
@bot.message_handler(commands=['incomessum'])
def incomes_sum(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Sum of incomes', callback_data='Sum of total incomes'))
    markup.add(types.InlineKeyboardButton(text='Sum of incomes for 12 months', callback_data='Sum of total incomes for 12 months'))
    markup.add(types.InlineKeyboardButton(text='Sum of incomes for 6 months', callback_data='Sum of total incomes for 6 months'))
    markup.add(types.InlineKeyboardButton(text='Sum of incomes for 3 months', callback_data='Sum of total incomes for 3 months'))
    markup.add(types.InlineKeyboardButton(text='Sum of incomes for 1 month', callback_data='Sum of total incomes for 1 month'))
    
    #Reply markup in chat
    bot.send_message(
        message.chat.id,
        text='Options for sum',
        reply_markup=markup
    )    

#Make buttons for send info about average sum of incomes in defferent period
@bot.message_handler(commands=['averageincomes'])
def incomes_average(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Average sum of incomes', callback_data='Average sum of total incomes'))
    markup.add(types.InlineKeyboardButton(text='Average sum of incomes for 12 months', callback_data='Average sum of total incomes for 12 months'))
    markup.add(types.InlineKeyboardButton(text='Average sum of incomes for 6 months', callback_data='Average sum of total incomes for 6 months'))
    markup.add(types.InlineKeyboardButton(text='Average sum of incomes for 3 months', callback_data='Average sum of total incomes for 3 months'))
    markup.add(types.InlineKeyboardButton(text='Average sum of incomes for 1 month', callback_data='Average sum of total incomes for 1 month'))
    
    #Reply markup in chat
    bot.send_message(
        message.chat.id,
        text='Average options',
        reply_markup=markup
    )
    
#Make buttons for send info about count of incomes in defferent period
@bot.message_handler(commands=['countincomes'])
def count_of_incomes(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Count of incomes', callback_data='Count of total incomes'))
    markup.add(types.InlineKeyboardButton(text='Count of incomes for 12 months', callback_data='Count of total incomes for 12 months'))
    markup.add(types.InlineKeyboardButton(text='Count of incomes for 6 months', callback_data='Count of total incomes for 6 months'))
    markup.add(types.InlineKeyboardButton(text='Coumt of incomes for 3 months', callback_data='Count of total incomes for 3 months'))
    markup.add(types.InlineKeyboardButton(text='Count of incomes for 1 month', callback_data='Count of total incomes for 1 month'))
    
    #Reply markup in chat
    bot.send_message(
        message.chat.id,
        text='Count options',
        reply_markup=markup
    )    

#Make buttons for send info about sum of expenses in defferent period
@bot.message_handler(commands=['expensessum'])
def incomes_sum(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Sum of expenses', callback_data='Sum of total expenses'))
    markup.add(types.InlineKeyboardButton(text='Sum of expenses for 12 months', callback_data='Sum of total expenses for 12 months'))
    markup.add(types.InlineKeyboardButton(text='Sum of expenses for 6 months', callback_data='Sum of total expenses for 6 months'))
    markup.add(types.InlineKeyboardButton(text='Sum of expenses for 3 months', callback_data='Sum of total expenses for 3 months'))
    markup.add(types.InlineKeyboardButton(text='Sum of expenses for 1 month', callback_data='Sum of total expenses for 1 month'))
    
    #Reply markup in database
    bot.send_message(
        message.chat.id,
        text='Options for sum',
        reply_markup=markup
    )    

#Make buttons for send info about average sum of expenses in different period
@bot.message_handler(commands=['averageexpenses'])
def incomes_average(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Average sum of expenses', callback_data='Average sum of total expenses'))
    markup.add(types.InlineKeyboardButton(text='Average sum of expenses for 12 months', callback_data='Average sum of total expenses for 12 months'))
    markup.add(types.InlineKeyboardButton(text='Average sum of expenses for 6 months', callback_data='Average sum of total expenses for 6 months'))
    markup.add(types.InlineKeyboardButton(text='Average sum of expenses for 3 months', callback_data='Average sum of total expenses for 3 months'))
    markup.add(types.InlineKeyboardButton(text='Average sum of expenses for 1 month', callback_data='Average sum of total expenses for 1 month'))
    
    #Reply markup in chat
    bot.send_message(
        message.chat.id,
        text='Average options',
        reply_markup=markup
    )
    
#Make buttons for send info about count of expenses in different period
@bot.message_handler(commands=['countexpenses'])
def count_of_incomes(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Count of expenses', callback_data='Count of total expenses'))
    markup.add(types.InlineKeyboardButton(text='Count of expenses for 12 months', callback_data='Count of total expenses for 12 months'))
    markup.add(types.InlineKeyboardButton(text='Count of expenses for 6 months', callback_data='Count of total expenses for 6 months'))
    markup.add(types.InlineKeyboardButton(text='Coumt of expenses for 3 months', callback_data='Count of total expenses for 3 months'))
    markup.add(types.InlineKeyboardButton(text='Count of expenses for 1 month', callback_data='Count of total expenses for 1 month'))
    bot.send_message(
        message.chat.id,
        text='Count options',
        reply_markup=markup
    )

#Make actions when user tap on button        
@bot.callback_query_handler(func=lambda call: True)
def callback_options(call):
    #Connect to database
    conn = sqlite3.connect('Balance.db')
    cursor = conn.cursor()
    
    #Make a variable of user's id
    user = call.message.chat.id
    
    if call.data == 'Total incomes':
        
        #Select full info from our table
        cursor.execute(f'SELECT * FROM INCOME WHERE USER_ID = {user}')
        data = cursor.fetchall()
        
        #Send messages consist's from info about incomes (id, total sum, date of add in database)
        for income in data:
            bot.send_message(
                call.message.chat.id,
                text=f'ID: {income[0]} - Total: {income[2]}, date: {income[3]}'
            )    

    elif call.data == 'Incomes for 12 months':
        
        #Select info about incomes in period 12 months
        cursor.execute(f'SELECT * FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-12 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
        data = cursor.fetchall()
        
        for income in data:
            bot.send_message(
                call.message.chat.id,
                text=f'ID: {income[0]} - Total: {income[2]}, date: {income[3]}'
            )    

    elif call.data == 'Incomes for 6 months':
        
        #Select info about incomes in period 6 months
        cursor.execute(f'SELECT * FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-6 month") AND DATETIME ("now", "localtime") ORDER BY "DATE"')
        data = cursor.fetchall()
        
        for income in data:
            bot.send_message(
                call.message.chat.id,
                text=f'ID: {income[0]} - Total: {income[2]}, date: {income[3]}'
            )
            
    elif call.data == 'Incomes for 3 months':
        
        #Select info about incomes in period 3 months
        cursor.execute(f'SELECT * FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-3 month") AND DATETIME ("now", "localtime") ORDER BY "DATE"')
        data = cursor.fetchall()
        
        for income in data:
            bot.send_message(
                call.message.chat.id,
                text=f'ID: {income[0]} - Total: {income[2]}, date: {income[3]}'
            )
            
    elif call.data == 'Incomes for 1 month':
        
        #Select info about incomes in period 1 month
        cursor.execute(f'SELECT * FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-1 month") AND DATETIME ("now", "localtime") ORDER BY "DATE"')
        data = cursor.fetchall()
        
        for income in data:
            bot.send_message(
                call.message.chat.id,
                text=f'ID: {income[0]} - Total: {income[2]}, date: {income[3]}'
            )
            
    elif call.data == 'Total expenses':
        
        #Select full info about expenses
        cursor.execute(f'SELECT * FROM EXPENSE WHERE USER_ID = {user}')
        data = cursor.fetchall()
        
        for expense in data:
            bot.send_message(
                call.message.chat.id,
                text=f'ID: {expense[0]} - Total: {expense[2]}, date: {expense[3]}'
            )
            
    elif call.data == 'Expenses for 12 months':
        
        #Select info about exepenses in period 12 months
        cursor.execute(f'SELECT * FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-12 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
        data = cursor.fetchall()
        
        for expense in data:
            bot.send_message(
                call.message.chat.id,
                text=f'ID: {expense[0]} - Total: {expense[2]}, date: {expense[3]}'
            )
            
    elif call.data == 'Expenses for 6 months':
        
        #Select info about expenses in period 6 months
        cursor.execute(f'SELECT * FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-6 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
        data = cursor.fetchall()
        
        for expense in data:
            bot.send_message(
                call.message.chat.id,
                text=f'ID: {expense[0]} - Total: {expense[2]}, date: {expense[3]}'
            )
            
    elif call.data == 'Expenses for 3 months':
        
        #Select info about expenses in period 3 months
        cursor.execute(f'SELECT * FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-3 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
        data = cursor.fetchall()
        
        for expense in data:
            bot.send_message(
                call.message.chat.id,
                text=f'ID: {expense[0]} - Total: {expense[2]}, date: {expense[3]}'
            )
    
    elif call.data == 'Expenses for 1 month':
        
        #Select info about expenses in period 1 month
        cursor.execute(f'SELECT * FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-1 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
        data = cursor.fetchall()
        
        for expense in data:
            bot.send_message(
                call.message.chat.id,
                text=f'ID: {expense[0]} - Total: {expense[2]}, date: {expense[3]}'
            )    

    elif call.data == 'Sum of total incomes':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Calculate total sum of incomes for full period
        cursor.execute(f'SELECT SUM(TOTAL) FROM INCOME WHERE USER_ID = {user}')
        
        #Make a variable for send message
        data = cursor.fetchone()[0]
        
        #Send message with data about total sum of incomes
        bot.send_message(
            call.message.chat.id,
            text=f'Sum of incomes: {data}'
            )

        conn.close()
        
    elif call.data == 'Sum of total incomes for 12 months':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select total sum of incomes in period of 12 months
        cursor.execute(f'SELECT SUM(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-12 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Total sum of incomes for 12 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Sum of total incomes for 6 months':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select total sum of incomes in period of 6 months
        cursor.execute(f'SELECT SUM(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-6 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Total sum of incomes for 6 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Sum of total incomes for 3 months':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select total sum of incomes in period of 3 months
        cursor.execute(f'SELECT SUM(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-3 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Total sum of incomes for 3 months: {data}'
        )  

        conn.close()
    
    elif call.data == 'Sum of total incomes for 1 month':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select sum of total incomes in period of 1 month
        cursor.execute(f'SELECT SUM(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-1 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Total sum of incomes for 1 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Average sum of total incomes':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select info about average sum of total incomes in full period
        cursor.execute(f'SELECT AVG(TOTAL) FROM INCOME WHERE USER_ID = {user}')
        
        data = round(cursor.fetchone()[0], 2)
        
        bot.send_message(
            call.message.chat.id,
            text=f'Average sum of incomes: {data}'
            )

        conn.close()
        
    elif call.data == 'Average sum of total incomes for 12 months':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Seletc info about average sum of total incomes in period of 12 months
        cursor.execute(f'SELECT AVG(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-12 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
        
        data = round(cursor.fetchone()[0], 2)
        
        bot.send_message(
            call.message.chat.id,
            text=f'Average sum of incomes for 12 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Average sum of total incomes for 6 months':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select info about average sum of total incomes in period of 6 months
        cursor.execute(f'SELECT AVG(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-6 month") AND DATETIME("now", "localtime")')
        
        data = round(cursor.fetchone()[0], 2)
        
        bot.send_message(
            call.message.chat.id,
            text=f'Average sum of incomes for 6 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Average sum of total incomes for 3 months':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select info about average sum of incomes in period of 3 months
        cursor.execute(f'SELECT AVG(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-3 month") AND DATETIME("now", "localtime")')
        
        data = round(cursor.fetchone()[0], 2)
        
        bot.send_message(
            call.message.chat.id,
            text=f'Average sum of incomes for 3 months: {data}'
        )
        
        conn.close()  
    
    elif call.data == 'Average sum of total incomes for 1 month':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select info about average sum of total incomes in period of 1 month
        cursor.execute(f'SELECT AVG(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-1 month") AND DATETIME("now", "localtime")')
        
        data = round(cursor.fetchone()[0], 2)
        
        bot.send_message(
            call.message.chat.id,
            text=f'Average sum of incomes for 1 months: {data}'
        )
        
        conn.close()
    
    elif call.data == 'Count of total incomes':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select info about count of incomes in full period
        cursor.execute(f'SELECT COUNT(TOTAL) FROM INCOME WHERE USER_ID = {user}')

        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Count of incomes: {data}'
        )
        
        conn.close()
        

    elif call.data == 'Count of total incomes for 12 months':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select info about count of incomes in period of 12 months    
        cursor.execute(f'SELECT COUNT(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-12 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
            
        data = cursor.fetchone()[0]
            
        bot.send_message(
            call.message.chat.id,
            text=f'Count of incomes for 12 months: {data}'
            )
            
        conn.close()
        
    elif call.data == 'Count of total incomes for 6 months':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select info about count of incomes in period of 6 months
        cursor.execute(f'SELECT COUNT(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-6 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Count of incomes for 6 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Count of total incomes for 3 months':
        
        #Connect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select info about count of incomes in period of 3 months
        cursor.execute(f'SELECT COUNT(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-3 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Count of incomes for 3 months: {data}'
        )
        
        conn.close()  
    
    elif call.data == 'Count of total incomes for 1 month':
        
        #Connnect to database
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        #Select info about count of incomes in period of 1 month
        cursor.execute(f'SELECT COUNT(TOTAL) FROM INCOME WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-1 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Count of incomes for 1 months: {data}'
        )
        
        conn.close()
    
    #All operations is the same, but with expenses
    elif call.data == 'Sum of total expenses':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT SUM(TOTAL) FROM EXPENSE WHERE USER_ID = {user}')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Sum of expenses: {data}'
            )

        conn.close()
        
    elif call.data == 'Sum of total expenses for 12 months':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT SUM(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-12 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Total sum of expenses for 12 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Sum of total expenses for 6 months':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT SUM(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-6 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Total sum of expenses for 6 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Sum of total expenses for 3 months':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT SUM(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-3 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Total sum of expenses for 3 months: {data}'
        )  

        conn.close()
        
    elif call.data == 'Sum of total expenses for 1 month':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT SUM(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-1 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Total sum of expenses for 1 months: {data}'
        )
        
        conn.close()
                
    elif call.data == 'Average sum of total expenses':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT AVG(TOTAL) FROM EXPENSE WHERE USER_ID = {user}')
        
        data = round(cursor.fetchone()[0], 2)
        
        bot.send_message(
            call.message.chat.id,
            text=f'Average sum of expenses: {data}'
            )

        conn.close()
        
    elif call.data == 'Average sum of total expenses for 12 months':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT AVG(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-12 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
        
        data = round(cursor.fetchone()[0], 2)
        
        bot.send_message(
            call.message.chat.id,
            text=f'Average sum of expenses for 12 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Average sum of total expenses for 6 months':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT AVG(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-6 month") AND DATETIME("now", "localtime")')
        
        data = round(cursor.fetchone()[0], 2)
        
        bot.send_message(
            call.message.chat.id,
            text=f'Average sum of expenses for 6 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Average sum of total expenses for 3 months':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT AVG(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-3 month") AND DATETIME("now", "localtime")')
        
        data = round(cursor.fetchone()[0], 2)
        
        bot.send_message(
            call.message.chat.id,
            text=f'Average sum of expenses for 3 months: {data}'
        )
        
        conn.close()  
    
    elif call.data == 'Average sum of total expenses for 1 month':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT AVG(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-1 month") AND DATETIME("now", "localtime")')
        
        data = round(cursor.fetchone()[0], 2)
        
        bot.send_message(
            call.message.chat.id,
            text=f'Average sum of expenses for 1 months: {data}'
        )
        
        conn.close()
    
    elif call.data == 'Count of total expenses':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT COUNT(TOTAL) FROM EXPENSE WHERE USER_ID = {user}')

        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Count of expenses: {data}'
        )
        
        conn.close()
        

    elif call.data == 'Count of total expenses for 12 months':
            conn = sqlite3.connect('Balance.db')
            cursor = conn.cursor()
            
            cursor.execute(f'SELECT COUNT(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-12 month") AND DATETIME("now", "localtime") ORDER BY "DATE"')
            
            data = cursor.fetchone()[0]
            
            bot.send_message(
                call.message.chat.id,
                text=f'Count of expenses for 12 months: {data}'
            )
            
            conn.close()
        
    elif call.data == 'Count of total expenses for 6 months':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT COUNT(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-6 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Count of expenses for 6 months: {data}'
        )
        
        conn.close()
        
    elif call.data == 'Count of total expenses for 3 months':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT COUNT(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-3 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Count of expenses for 3 months: {data}'
        )
        
        conn.close()  
    
    elif call.data == 'Count of total expenses for 1 month':
        conn = sqlite3.connect('Balance.db')
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT COUNT(TOTAL) FROM EXPENSE WHERE USER_ID = {user} AND "DATE" BETWEEN DATETIME("now", "-1 month") AND DATETIME("now", "localtime")')
        
        data = cursor.fetchone()[0]
        
        bot.send_message(
            call.message.chat.id,
            text=f'Count of expenses for 1 months: {data}'
        )
        
        conn.close()
        
        
if __name__ == '__main__':
    bot.infinity_polling()