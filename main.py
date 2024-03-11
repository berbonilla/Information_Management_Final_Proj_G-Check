import mysql.connector
from datetime import datetime
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField,MDTextFieldHintText,MDTextFieldTrailingIcon
from kivymd.uix.list import MDListItem
from kivymd.uix.list import MDListItemHeadlineText
from kivymd.uix.list import MDListItemSupportingText
from kivymd.uix.list import MDListItemTertiaryText
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.snackbar import MDSnackbarText,MDSnackbarSupportingText,MDSnackbarButtonContainer,MDSnackbarActionButton,MDSnackbarActionButtonText
from kivymd.uix.snackbar import MDSnackbarCloseButton
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.widget import Widget
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screenmanager import MDScreenManager

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database = "g-check"
)

def remove_chars(input_data):
    input_string = str(input_data)
    chars_to_remove = ['(','"', ',)', "'"]
    for char in chars_to_remove:
        input_string = input_string.replace(char, '')
    return input_string

# Transaction Variable Arrays
transactionIDs = []
transactionTypes = []
amount = []
referenceNums =[]
timestamps = []
balance = []

# Admin Variable Arrays
cashierID = []
adminID = []
adminAuthCode = []
adminPass = []

# Cashier Variable Arrays
cashierPIN = []

#audit variables
auditlogIDS = []
auditTimestamps = []
auditOriginfo = []
auditStatus = []
auditAmount = []
auditTransactionTypes = []

# Cash In Variables
total_cash_in = []
total_cash_out = []

def query_data():
    if len(balance) < 2:
        dbCursor = mydb.cursor()
        dbCursor.execute("select balance from admin")
        
        for i in dbCursor:
            balance.append(remove_chars(i))
    
    if len(adminID) == 0 and len(adminID) < 1:
        dbCursor = mydb.cursor()
        dbCursor.execute("select admin_id from admin")

        for i in dbCursor:
            adminID.append(remove_chars(i))
            
        dbCursor = mydb.cursor()
        dbCursor.execute("select authenticator_code from admin")

        for i in dbCursor:
            adminAuthCode.append(remove_chars(i))
    

    dbCursor = mydb.cursor()
    dbCursor.execute("select cashierID from cashiers")

    for i in dbCursor:
        if (remove_chars(i) in cashierID):
            pass
        else:
            cashierID.append(remove_chars(i))    
        
    dbCursor = mydb.cursor()
    dbCursor.execute("select pin from cashiers")
    
    for i in dbCursor:
        if (remove_chars(i) in cashierPIN):
            pass
        else:
            cashierPIN.append(remove_chars(i))
        
    dbCursor = mydb.cursor()
    dbCursor.execute("select transactionID from transactions")

    for i in dbCursor:
        transactionIDs.append(remove_chars(i))

    dbCursor = mydb.cursor()
    dbCursor.execute("select transaction_type from transactions")

    for i in dbCursor:
        transactionTypes.append(remove_chars(i))

    dbCursor = mydb.cursor()
    dbCursor.execute("select amount from transactions")

    for i in dbCursor:
        amount.append(remove_chars(i))

    dbCursor = mydb.cursor()
    dbCursor.execute("select gcash_reference_number from transactions")

    for i in dbCursor:
        referenceNums.append(remove_chars(i))

    dbCursor = mydb.cursor()
    dbCursor.execute("select timestamp from transactions")

    for i in dbCursor:
        input_tuple = i
        formatted_date = input_tuple[0].strftime("%B, %d, %Y, %I:%M %p")
        timestamps.append(formatted_date)    
        
    dbCursor = mydb.cursor()
    dbCursor.execute("select auditlogID from audit_log")

    for i in dbCursor:
        auditlogIDS.append(remove_chars(i))   
        
    dbCursor = mydb.cursor()
    dbCursor.execute("select timestamp from audit_log")

    for i in dbCursor:
        input_tuple = i
        formatted_date = input_tuple[0].strftime("%B, %d, %Y, %I:%M %p")
        auditTimestamps.append(remove_chars(formatted_date))  

    dbCursor = mydb.cursor()
    dbCursor.execute("select amount from audit_log")

    for i in dbCursor:
        auditAmount.append(remove_chars(i))   
    
    dbCursor = mydb.cursor()
    dbCursor.execute("select transaction_type from audit_log")

    for i in dbCursor:
        auditTransactionTypes.append(remove_chars(i)) 
    
    
    dbCursor = mydb.cursor()
    dbCursor.execute("select status from audit_log")

    for i in dbCursor:
        auditStatus.append(remove_chars(i))     
        



class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()
class BaseScreen(MDScreen):
    ...

def void_display(self,):
    App.void(self)

def show(self):
    App.show_snackbar(self)
    
def success():
        snackbar = MDSnackbar(
                MDSnackbarText(
                    pos_hint = {'center_x':.5},
                    halign="center",
                    theme_text_color = "Custom",
                    text_color="white",
                    text="Success!",
                    ),
                    show_transition = "out_elastic",
                    show_duration = ".8",
                    size_hint_x=".5",
                    pos_hint = {'center_x':.5,'center_y':.5},
                    background_color= "gray"
                )
        snackbar.open()
        
        App.reset_text_fields

SCREEN = []
AUTHCODE = []
SELF = []
UPDATE = []

class App(MDApp):
    
    def exit_app(self):
        Window.close() 
    
    def on_start(self):
        query_data()
        
        if len(adminID) == 1: 
            self.root.current = "setupScreen"
            
        SCREEN.append(self.root)
        SELF.append(self)
            
    def checker(self, snackbar_instance):

        admin_pin = self.ids.checker.text  
        snackbar_instance.dismiss() 

    def password_too_common_fail(self):
        snackbar = MDSnackbar(
            MDSnackbarText(
                pos_hint = {'center_x':.5},
                halign="center",
                theme_text_color = "Custom",
                text_color="white",
                text="Password Too Common",
                bold = "True"
                ),
                show_transition = "out_elastic",
                show_duration = ".3",
                size_hint_x=".5",
                pos_hint = {'center_x':.5,'center_y':.5},
                background_color= "gray",
                duration = ".01"
            )
        snackbar.open()

    def invalid_input_fail(self):
        snackbar = MDSnackbar(
            MDSnackbarText(
                pos_hint = {'center_x':.5},
                halign="center",
                theme_text_color = "Custom",
                text_color="white",
                text="Invalid Input",
                bold = "True"
                ),
                show_transition = "out_elastic",
                show_duration = ".3",
                size_hint_x=".5",
                pos_hint = {'center_x':.5,'center_y':.5},
                background_color= "gray",
                duration = ".01"
            )
        snackbar.open()

    def already_voided_fail(self):
        snackbar = MDSnackbar(
            MDSnackbarText(
                pos_hint = {'center_x':.5},
                halign="center",
                theme_text_color = "Custom",
                text_color="white",
                text="Transaction Alread Voided",
                bold = "True"
                ),
                show_transition = "out_elastic",
                show_duration = ".3",
                size_hint_x=".5",
                pos_hint = {'center_x':.5,'center_y':.5},
                background_color= "gray",
                duration = ".01"
            )
        snackbar.open()


    def cannot_be_empty_fail(self):
        snackbar = MDSnackbar(
            MDSnackbarText(
                pos_hint = {'center_x':.5},
                halign="center",
                theme_text_color = "Custom",
                text_color="white",
                text="Input Cannot Be Empty",
                bold = "True"
                ),
                show_transition = "out_elastic",
                show_duration = ".3",
                size_hint_x=".5",
                pos_hint = {'center_x':.5,'center_y':.5},
                background_color= "gray",
                duration = ".01"
            )
        snackbar.open() 

    def wrong_credentials_fail(self):
        snackbar = MDSnackbar(
            MDSnackbarText(
                pos_hint = {'center_x':.5},
                theme_text_color = "Custom",
                text_color="white",
                text="Account Not Found",
                bold = "True"
                ),
                show_transition = "out_elastic",
                show_duration = ".3",
                size_hint_x=".5",
                pos_hint = {'center_x':.5,'center_y':.5},
                background_color= "gray",
                duration = ".01"
            )
        snackbar.open()
            
    def reset_text_fields(self):
        self.root.ids.cash_in_amount.text = ""
        self.root.ids.cash_in_ref_number.text = ""
        self.root.ids.PinField.text = ""
        self.root.ids.cash_out_amount.text = ""
        self.root.ids.cash_out_ref_number.text = ""        
        
    def cash_out(self):
        if (self.root.ids.cash_out_amount.text != "" and  self.root.ids.cash_out_ref_number.text != ""):
            if (float(self.root.ids.cash_out_amount.text)) < (float(balance[0])):
                if (self.root.ids.cash_out_ref_number not in referenceNums):
                    
                    now_cashier = self.root.ids.cashieridField.text
                    now_cashier = int(now_cashier)   
                    
                    dbCursor = mydb.cursor()
                    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_query = 'INSERT INTO transactions (amount, transaction_type,gcash_reference_number,cashierID,timestamp) VALUES (%s,%s,%s,%s,%s)'
                    dbCursor.execute(insert_query, (self.root.ids.cash_out_amount.text,"CASH OUT",self.root.ids.cash_out_ref_number.text,int(now_cashier),(current_date_time)))
                    
                    dbCursor.execute("SELECT LAST_INSERT_ID() AS transactionID")
                    transactionID = dbCursor.fetchone()[0]
                    
                    insert_query = 'INSERT INTO audit_log (transactionID, amount, transaction_type,gcash_reference_number,timestamp,status) VALUES (%s,%s,%s,%s,%s,%s)'
                    dbCursor.execute(insert_query, (transactionID,self.root.ids.cash_out_amount.text,"CASH OUT",self.root.ids.cash_out_ref_number.text,(current_date_time),"VALID"))

                    new_balance = (float(balance[0])-float(self.root.ids.cash_out_amount.text))
                    dbCursor.execute(f"UPDATE admin SET balance = {str(new_balance)} WHERE admin_id = {adminID[0]}")
                    
                    mydb.commit()
                    success
                    
                    query_data()
                    return True
        
        else:
            self.invalid_input_fail
            return False  
                 
    def cash_in(self):
        
        if (self.root.ids.cash_in_amount.text != "" and  self.root.ids.cash_in_ref_number.text != ""):
            if (self.root.ids.cash_in_ref_number not in referenceNums):
                
                now_cashier = self.root.ids.cashieridField.text
                now_cashier = int(now_cashier)       

    
                                    
                dbCursor = mydb.cursor()
                current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                insert_query = 'INSERT INTO transactions (amount, transaction_type,gcash_reference_number,cashierID,timestamp) VALUES (%s,%s,%s,%s,%s)'
                dbCursor.execute(insert_query, (self.root.ids.cash_in_amount.text,"CASH IN",self.root.ids.cash_in_ref_number.text,int(now_cashier),(current_date_time)))
                dbCursor.execute("SELECT LAST_INSERT_ID() AS transactionID")
                transactionID = dbCursor.fetchone()[0]
                
                insert_query = 'INSERT INTO audit_log (transactionID, amount, transaction_type,gcash_reference_number,timestamp,status) VALUES (%s,%s,%s,%s,%s,%s)'
                dbCursor.execute(insert_query, (transactionID,self.root.ids.cash_in_amount.text,"CASH IN",self.root.ids.cash_in_ref_number.text,(current_date_time),"VALID"))
                
                new_balance = (float(self.root.ids.cash_in_amount.text) + float(balance[0]))
                dbCursor.execute(f"UPDATE admin SET balance = {str(new_balance)} WHERE admin_id = {adminID[0]}")
                mydb.commit()
                
                success
                
                return True
        
        query_data()
        
    def admin_login(self):
        query_data()
        
        admin = self.root.ids.adminidField.text 
        pin  = self.root.ids.authField.text

        if (admin in adminID):
            if (admin == adminID[0] and pin == adminAuthCode[0]):
                success
                
                return True
        
    def cashier_login(self):
        query_data()
        
        cashier_id = self.root.ids.cashieridField.text 
        pin = self.root.ids.PinField.text
        
        if (cashier_id in cashierID and pin in cashierPIN and cashier_id != "" and pin != ""):
            if (cashierID.index(cashier_id)== cashierPIN.index(pin)):
                success
                self.dashboard
                return True
      
    def cashier_name(self):
        query_data()
        if (cashierID == 0):
           return str(1)
        else:
            return str((len(cashierID))+1)
            
    def cashier_register(self):
        query_data()
        cashier_pin_reg  = str(self.root.ids.cashierRegistrationPinField.text)
        if (cashier_pin_reg not in cashierPIN):
            if (cashier_pin_reg != 0 and len(cashier_pin_reg) == 4):
                
                dbCursor = mydb.cursor()
                insert_query = 'INSERT INTO cashiers (cashierID ,pin) VALUES (%s,%s)'
                dbCursor.execute(insert_query, (str(len(cashierID)+1),cashier_pin_reg))
                    
                mydb.commit()
                success
                return True
        
    def register(self):
        admin_reg = str(self.root.ids.registeradminidField.text)
        admin_pin_reg  = str(self.root.ids.registeradminPinField.text)
        bal_in = str(self.root.ids.balanceField.text)
        
        if (len(adminID) == 0 and admin_reg != "" and admin_pin_reg != "" and bal_in != ""):
            dbCursor = mydb.cursor()
            insert_query = 'INSERT INTO admin (admin_id, authenticator_code,balance) VALUES (%s,%s,%s)'
            dbCursor.execute(insert_query, (admin_reg,admin_pin_reg,bal_in))
                
            mydb.commit()
            success

            return True
        
        query_data()
        
    def update(self):
        if (len(UPDATE ) == 0):
            UPDATE.append(self)
        
        if (len(transactionIDs) != 0): 
            i = 0
            for i in range(len(transactionIDs)):      
                transactionIDs.remove(transactionIDs[i-(i+1)])
                transactionTypes.remove(transactionTypes[i-(i+1)])
                amount.remove(amount[i-(i+1)])
                referenceNums.remove(referenceNums[i-(i+1)])
                timestamps.remove(timestamps[i-(i+1)])
                      
            self.root.ids.recent_transactions_container.clear_widgets()      

    def void(self):
        id = str(self.id)
        id = int(id)
        try:             
            item_index = id        
            if auditStatus[(len(auditStatus)-1)-id] == "VALID":
                snackbar_2 = MDSnackbar(
                    orientation = "vertical",
                    show_transition = "out_elastic",
                    show_duration = ".5",
                    size_hint_y=".85",
                    pos_hint = {'center_x':.5,'center_y':.5},
                    duration="60",
                    background_color= (143,142,142,.3),
                    radius = [15,15,15,15],
                    spacing = 25
                )
                
                summary = MDLabel(                
                    text= "Audit Summary",
                    font_style = "Title",
                    role= "medium",   
                    bold = True,
                    halign = "center",
                    pos_hint= {"center_x": .5},
                    size_hint_y= .5,
                    theme_text_color= "Custom",
                    text_color="#034189",
                    theme_bg_color= "Custom",
                    md_bg_color = "#FFFFFF",
                    radius = [15,15,15,15]                    
                )
                
                label_1 = MDLabel(                
                    text= f"Amount        :{amount[item_index]}",
                    font_style = "Title",
                    role= "medium",   
                    text_color= "black",
                    bold = True,
                    halign = "left",
                    pos_hint= {"center_x": .5},
                    size_hint_y= .5,
                    size_hint_x= .8,
                    theme_bg_color= "Custom",
                    md_bg_color = "#8f8e8e4d",                 
                )
                
                label_2 = MDLabel(                
                    text= f"Type            :{transactionTypes[id]}",
                    font_style = "Title",
                    role= "medium",   
                    text_color= "black",
                    bold = True,
                    halign = "left",
                    pos_hint= {"center_x": .5},
                    size_hint_y= .5,
                    size_hint_x= .8,
                    theme_bg_color= "Custom",
                    md_bg_color = "#8f8e8e4d",
                )
                
                label_3 = MDLabel(                
                    text= f"Processed on :{timestamps[id]}",
                    font_style = "Title",
                    role= "medium",   
                    text_color= "black",
                    bold = True,
                    halign = "left",
                    pos_hint= {"center_x": .5},
                    size_hint_y= .5,
                    size_hint_x= .8,
                    theme_bg_color= "Custom",
                    md_bg_color = "#8f8e8e4d",
                )
                
                label_4 = MDLabel(                
                    text= f"Cashier Num  :{cashierID[id]}",
                    font_style = "Title",
                    role= "medium",   
                    text_color= "black",
                    bold = True,
                    halign = "left",
                    pos_hint= {"center_x": .5},
                    size_hint_y= .5,
                    size_hint_x= .8,
                    theme_bg_color= "Custom",
                    md_bg_color = "#8f8e8e4d",
                )
                
                label_5 = MDLabel(                
                    text= f"Status       :{auditStatus[(len(auditStatus)-1)-id]}",
                    font_style = "Title",
                    role= "medium",   
                    text_color= "black",
                    bold = True,
                    halign = "left",
                    pos_hint= {"center_x": .5},
                    size_hint_y= .5,
                    size_hint_x= .8,
                    theme_bg_color= "Custom",
                    md_bg_color = "#8f8e8e4d",
                )
                
                proceed_button = MDButton(
                        MDButtonText(
                            bold= True,
                            font_style= "Title",
                            role="medium",
                            text= "Void",
                            pos_hint= {"center_x": .5,"center_y":.5},
                            theme_text_color= "Custom",
                            text_color= "#000000",
                            radius= [100,100,100,100],
                        ),       
                        style= "elevated",
                        theme_width = "Custom",
                        size_hint_x= .45,
                        height= "56dp",            
                        pos_hint={"center_x": .5,"center_y":.4},
                        theme_bg_color= "Custom",
                        on_release = lambda instance: App.process_void_data(self,item_index,textNewAmount.text,textNewRefNum.text) 
                    )
                
                exit_button = MDButton(
                        MDButtonText(
                            bold= True,
                            font_style= "Title",
                            role="medium",
                            text= "Close",
                            pos_hint= {"center_x": .5,"center_y":.5},
                            theme_text_color= "Custom",
                            text_color= "#000000",
                            radius= [100,100,100,100],
                        ),       
                        style= "elevated",
                        theme_width = "Custom",
                        size_hint_x= .45,
                        height= "56dp",            
                        pos_hint={"center_x": .5,"center_y":.4},
                        theme_bg_color= "Custom",
                        on_release = lambda instance: snackbar_2.dismiss()
                    )                                
                
                textNewAmount = MDTextField(                
                        MDTextFieldHintText(
                            text= "New Amount",
                            font_style = "Label",
                            role= "small",
                            theme_text_color= "Custom",
                            text_color= "#000000"                                     
                        ), 
                        mode = "outlined",
                        theme_text_color= "Custom",
                        text_color_focus= (0,0,0,1),         
                        pos_hint= {"center_x": .5,"center_y":.6},
                        size_hint_x= .625,
                        theme_line_color= "Custom",
                        line_color_focus= (0,0,0,1),
                        md_bg_color="#0d82f6"
                    )
                
                textNewRefNum = MDTextField(                
                        MDTextFieldHintText(
                            text= "New Reference #",
                            font_style = "Label",
                            role= "small",
                            theme_text_color= "Custom",
                            text_color= "#000000"                                     
                        ), 
                        mode = "outlined",
                        theme_text_color= "Custom",
                        text_color_focus= (0,0,0,1),         
                        pos_hint= {"center_x": .5,"center_y":.5},
                        size_hint_x= .625,
                        theme_line_color= "Custom",
                        line_color_focus= (0,0,0,1),
                        md_bg_color="#0d82f6"
                    )
       
            snackbar_2.add_widget(summary)
            snackbar_2.add_widget(label_1)
            snackbar_2.add_widget(label_2)
            snackbar_2.add_widget(label_3)
            snackbar_2.add_widget(label_4)
            snackbar_2.add_widget(label_5)
            snackbar_2.add_widget(proceed_button)
            snackbar_2.add_widget(exit_button)
            snackbar_2.open()
       
            
            
        except:
            
            SELF[0].already_voided_fail()
        
            
    def process_void_data(self,*args):
        
        index = remove_chars(args[0])
        index = int(index)
        
        dbCursor = mydb.cursor()
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        insert_query = 'INSERT INTO transactions (amount, transaction_type,gcash_reference_number,cashierID,timestamp) VALUES (%s,%s,%s,%s,%s)'
        
        if (args[0] == "" or args[1] == ""):
            dbCursor.execute(f"DELETE FROM transactions WHERE amount = {amount[index]} and gcash_reference_number = {referenceNums[index]}")
            dbCursor.execute(f"UPDATE audit_log SET status = 'VOIDED' WHERE transactionID = {transactionIDs[index]}")
            newAmount = 0
            newReference= 0

            if (transactionTypes[index] == "CASH OUT"):
                oldbalance = (float(balance[0])+float(amount[index]))
                dbCursor.execute(f"UPDATE admin SET balance = {str(oldbalance)} WHERE admin_id = {adminID[0]}")
                
            elif (transactionTypes[index] == "CASH IN"):
                oldbalance = (float(balance[0])-float(amount[index]))
                dbCursor.execute(f"UPDATE admin SET balance = {str(oldbalance)} WHERE admin_id = {adminID[0]}")
        
        else:
            newAmount = args[0]
            newReference= args[1]
            
            if (transactionTypes[index] == "CASH OUT"):
                dbCursor.execute(insert_query, (newAmount,"CASH OUT",newReference,1,(current_date_time)))
                oldbalance = (float(balance[0])+float(amount[index]))
                dbCursor.execute(f"UPDATE admin SET balance = {str(oldbalance)} WHERE admin_id = {adminID[0]}")  
                
                new_balance = (float(balance[0])-float(newAmount))
                dbCursor.execute(f"UPDATE admin SET balance = {str(new_balance)} WHERE admin_id = {adminID[0]}") 
                                
            elif (transactionTypes[index] == "CASH IN"):
                dbCursor.execute(insert_query, (newAmount,"CASH IN",newReference,1,(current_date_time)))
                oldbalance = (float(balance[0])-float(amount[index]))
                dbCursor.execute(f"UPDATE admin SET balance = {str(oldbalance)} WHERE admin_id = {adminID[0]}")
                
                new_balance = (float(balance[0])+float(newAmount))
                dbCursor.execute(f"UPDATE admin SET balance = {str(new_balance)} WHERE admin_id = {adminID[0]}")   
                            
        mydb.commit()
        
        UPDATE[0].update()
        query_data()
        
        if(len(balance) > 1):
            balance.pop(0)
        
        if (type(balance[0]) == "int"):
            balanceDisplay = int(balance[0])
        else:
            balanceDisplay = float(balance[0])
            
        balanceDisplay = str(balanceDisplay)

        UPDATE[0].root.ids.BalanceLabelDashboard.text = (f"₱ {balanceDisplay}")
        UPDATE[0].root.ids.BalanceLabelCashout.text = (f"₱ {balanceDisplay}")
        UPDATE[0].root.ids.BalanceLabelCashIn.text = (f"₱ {balanceDisplay}")
        
        
    def get_text(self,*args):
        if (adminAuthCode[0] == self):
            AUTHCODE.append(self)
            SCREEN[0].current = "auditLogScreen"
            query_data()
            
            if (len(transactionIDs) != 0): 
                i = 0
                for i in range(len(transactionIDs)):      
                    transactionIDs.remove(transactionIDs[i-(i+1)])
                    transactionTypes.remove(transactionTypes[i-(i+1)])
                    amount.remove(amount[i-(i+1)])
                    referenceNums.remove(referenceNums[i-(i+1)])
                    timestamps.remove(timestamps[i-(i+1)])
            
            if (len(auditlogIDS) != 0): 
                for i in range(len(auditlogIDS)):                          
                    auditlogIDS.remove(auditlogIDS[i-(i+1)])
                    auditAmount.remove(auditAmount[i-(i+1)])
                    auditTransactionTypes.remove(auditTransactionTypes[i-(i+1)])
                    auditTimestamps.remove(auditTimestamps[i-(i+1)])
                    
                SCREEN[0].ids.audits_container.clear_widgets()
                
            UPDATE[0].update()    
            query_data() 

            for i in range(len(auditlogIDS)):

                if(auditStatus[(len(auditStatus)-1)-i] == "VOIDED"):
                    mode = True
                elif(auditStatus[(len(auditStatus)-1)-i] == "VALID"):
                    mode = False
                SCREEN[0].ids.audits_container.add_widget( 
                    MDListItem(
                        MDListItemHeadlineText(
                            text = f"₱ {auditAmount[(len(auditlogIDS)-1)-i]}",   
                            font_style = "Label",
                            role= "medium",
                            theme_text_color= "Custom",
                            text_color="#000000",
                            pos_hint= {"center_x": .5, "center_y": .8},
                            bold = True               
                        ),                    
                        MDListItemSupportingText(
                            text = f"{auditTransactionTypes[(len(auditlogIDS)-1)-i]}",
                            font_style = "Label",
                            role= "medium",
                            theme_text_color= "Custom",
                            pos_hint= {"center_x": .5, "center_y": .725},
                            text_color="#000000"                   
                        ),                  
                        MDListItemSupportingText(
                            text = f"{auditTimestamps[(len(auditlogIDS)-1)-i]}",
                            font_style = "Label",
                            role= "small",
                            theme_text_color= "Custom",
                            pos_hint= {"center_x": 1, "center_y": .675},
                            text_color="#000000"
                        ),
                        disabled = mode,                          
                        id = str(i),   
                        on_press= void_display,
                        theme_bg_color= "Custom",
                        md_bg_color= "#D3D3D3",
                        md_bg_color_disabled = "#6b6b6b",
                        radius = (3,3,3,3),
                        divider = True,
                        divider_color= (0, 0, 0, .5)                            
                    )
                )
            
            success
            UPDATE[0].update()
            query_data()
        
            
    def show_snackbar(self):   
        id = str(self.id)
        id = int(id)
        
        item_index = id    

        self.textfield = MDTextField(                
                MDTextFieldHintText(
                    text= "Admin Pin",
                    font_style = "Label",
                    role= "small",
                    theme_text_color= "Custom",
                    text_color= "#000000"                                     
                ), 
                password= True,
                password_mask = "•",
                halign = "center",
                mode = "outlined",
                theme_text_color= "Custom",
                text_color_focus= (0,0,0,1),         
                pos_hint= {"center_x": .5},
                size_hint_x= .625,
                theme_line_color= "Custom",
                line_color_focus= (0,0,0,1),
                md_bg_color="#0d82f6"
            )
        
        self.button = MDSnackbarActionButton(
            MDSnackbarActionButtonText(
                text="Proceed",
                theme_text_color = "Custom",
                text_color = "white",
            ),
            pos_hint={"center_y": 0.2,"center_x": 0.5},
            on_release = lambda instance: self.snackbar.dismiss(),
            theme_bg_color = "Custom",
            md_bg_color= "#0d82f6"                     
        )
        
        self.snackbar = MDSnackbar(
            pos_hint={"center_y": 0.5,"center_x": 0.5},
            size_hint_x=0.625,
            show_transition = "out_elastic",
            padding = [1,1,1,1],
            show_duration = ".8",
            background_color= "#0d82f6",
            duration = "3"
        )
        
        self.snackbar.add_widget(self.textfield)
        self.snackbar.add_widget(self.button)
        self.snackbar.open()
        self.snackbar.bind(on_dismiss = lambda instance: App.get_text(self.textfield.text,item_index))       
    
    def dashboard(self):
        self.update()
        query_data() 
        
        if(len(balance) > 1):
            balance.pop(0)
        
        if (type(balance[0]) == "int"):
            balanceDisplay = int(balance[0])
        else:
            balanceDisplay = float(balance[0])
            
        balanceDisplay = str(balanceDisplay)
        

        self.root.ids.CashierID.text = (f"Cashier : {self.root.ids.cashieridField.text}")
        self.root.ids.BalanceLabelDashboard.text = (f"₱ {balanceDisplay}")
        self.root.ids.BalanceLabelCashout.text = (f"₱ {balanceDisplay}")
        self.root.ids.BalanceLabelCashIn.text = (f"₱ {balanceDisplay}")
        
        for i in range(len(transactionIDs)):
            self.root.ids.recent_transactions_container.add_widget( 
                MDListItem(
                    MDListItemHeadlineText(
                        text = f"₱ {amount[(len(transactionIDs)-1)-i]}",   
                        font_style = "Label",
                        role= "medium",
                        theme_text_color= "Custom",
                        text_color="#000000",
                        pos_hint= {"center_x": .5, "center_y": .5},
                        bold = True               
                    ),                    
                    MDListItemSupportingText(
                        text = f"{transactionTypes[(len(transactionIDs)-1)-i]}",
                        font_style = "Label",
                        role= "medium",
                        theme_text_color= "Custom",
                        pos_hint= {"center_x": .5, "center_y": .3},
                        text_color="#000000"                   
                    ),                  
                    MDListItemSupportingText(
                        text = f"{timestamps[(len(transactionIDs)-1)-i]}",
                        font_style = "Label",
                        role= "small",
                        theme_text_color= "Custom",
                        pos_hint= {"center_x": 1, "center_y": .3},
                        text_color="#000000"
                    ),  
                    id = str(i),   
                    on_press= show,
                    theme_bg_color= "Custom",
                    md_bg_color= "#D3D3D3",
                    radius = (3,3,3,3),
                    divider = True,
                    divider_color= (0, 0, 0, .5)                            
                )
            )
                
    def build(self):
        Window.size = (360,640)
        self.title = "GCheck"
        self.icon = 'Images/logo.ico'
        return Builder.load_file("kv\g_check_(refactored).kv")
        
App().run()