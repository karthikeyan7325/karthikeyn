from tkinter import*
from tkinter import ttk #tableviw,notebook
import random
import tkinter.messagebox
import datetime
import time
import tkinter.ttk as tkrtk
import tkinter as tt
import pymysql
class Payroll:

    def __init__(self,root):
        self.root=root
        #TITTLE FOR OUR TAB
        self.root.title("Payroll Management System")
        self.root.geometry("1350x800+0+0")
        #USING NOTE_BOOK WIDGET
        notebook=ttk.Notebook(self.root) #for tabs.
        self.control1=ttk.Frame(notebook)
        self.control2=ttk.Frame(notebook)
        self.control3=ttk.Frame(notebook)
        notebook.add(self.control1,text='PAYROLL SYSTEM')
        notebook.add(self.control2,text='VIEW PAYMENTS')
        notebook.add(self.control3,text='COMMENT BOOK')
        notebook.grid()

        EmployeeName=StringVar()
        Address=StringVar()
        Reference=StringVar()
        EmployerName=StringVar()
        CityWeighting=IntVar()
        BasicSalary=IntVar()
        OverTime=StringVar()
        OtherPaymentDue=StringVar()
        GrossPay=StringVar()
        Tax=StringVar()
        Pension=StringVar()
        StudentLoan=StringVar()
        NIPayments=StringVar()
        Deductions=StringVar()
        PostCode=StringVar()
        Gender=StringVar()
        Payday=StringVar()
        TaxPeriod=StringVar()
        TaxCode=StringVar()
        NINumber=StringVar()
        TaxablePay=StringVar()
        PensionablePay=StringVar()
        Netpay=StringVar()

        text_in=StringVar()
        global operator
        operator=""
        CityWeighting.set("")
        BasicSalary.set("")

        #==================================================calculator========================================
        def btnClick(numbers):
            global operator
            operator=operator+str(numbers)
            text_in.set(operator)

        def btnClear():
            global operator
            operator=""
            text_in.set("")

        def btnEquals():
            global operator
            s=str(eval(operator))
            text_in.set(s)
            operator=""
        #==================================================EXIT========================================
        def Exit():
            Exit=tkinter.messagebox.askyesno("Payroll System","Confirm if you want to exit")
            if Exit>0:
                root.destroy()
                return
        def Reset():
            EmployeeName.set("")
            Address.set("")
            Reference.set("")
            EmployerName.set("")
            CityWeighting.set("")
            BasicSalary.set("")
            OverTime.set("")
            OtherPaymentDue.set("")
            GrossPay.set("")
            Tax.set("")
            Pension.set("")
            StudentLoan.set("")
            NIPayments.set("")
            Deductions.set("")
            PostCode.set("")
            Gender.set("")
            Payday.set("")
            TaxPeriod.set("")
            TaxCode.set("")
            NINumber.set("")
            TaxablePay.set("")
            PensionablePay.set("")
            Netpay.set("")
            
        #==================================================WAGES========================================
        def Payref():
           Nipay=random.randint(32000,567890)
           nipaid=("NI"+str(Nipay))
           NINumber.set(nipaid)
           idate=datetime.datetime.now()
           TaxPeriod.set(idate.month)
           axcode=random.randint(1435,35768)
           acode=("TCODE"+str(axcode))
           TaxCode.set(acode)
        
        def payment():
            Payref()
            bs=float(BasicSalary.get())
            cw=float(CityWeighting.get())
            ot=float(OverTime.get())
            mtax=((bs+cw+ot)*0.3)
            ttax=str('$%.2f'%(mtax))
            Tax.set(ttax)

            mpen=((bs+cw+ot)*0.02)
            mpension=str('$%.2f'%(mpen))
            Pension.set(mpension)

            mstudentloan=((bs+cw+ot)*0.012)
            mstudent=str('$%.2f'%(mstudentloan))
            StudentLoan.set(mstudent)

            mni=((bs+cw+ot)*0.011)
            mnipay=str('$%.2f'%(mni))
            NIPayments.set(mnipay)


            deduct=(mtax+mpen+mstudentloan+mni)
            dday=str('$%.2f'%(deduct))
            Deductions.set(dday)

            gpay=str('$%.2f'%(bs+cw+ot))
            GrossPay.set(gpay)

            npay=(bs+cw+ot)-deduct
            nafter=str('$%.2f'%(npay))
            Netpay.set(nafter)

            
            TaxablePay.set(ttax)
            PensionablePay.set(mpension)
            OtherPaymentDue.set("0.00")
            
        #==================================================data========================================
        def addData():
             Payday.set(time.strftime("%d/%m/%Y"))
             refpay=random.randint(15000,99000)
             refpaid=("RP"+str(refpay))
             Reference.set(refpaid)
             if EmployeeName.get()=="" or  Address.get()=="" or Reference.get()=="":
                 tkinter.messagebox.showerror("ENTER CORRECT MEMBER DETAILS","NO VALUES")
             else:
                 sqlcon=pymysql.connect(host="localhost",user="root",password="@slAmalef12",database="payroll")
                 cur=sqlcon.cursor()
                 cur.execute("insert into ni_pay values(%s,%s)",(NINumber.get(),NIPayments.get()))
                 cur.execute("insert into tax values(%s,%s,%s,%s)",(TaxCode.get(),TaxPeriod.get(),Tax.get(),NINumber.get()))
                 cur.execute("insert into payroll_management values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                             (Reference.get(),
                             EmployeeName.get(),
                             Address.get(),
                             CityWeighting.get(),
                             BasicSalary.get(),
                             OverTime.get(),
                             GrossPay.get(),
                             Pension.get(),
                             PostCode.get(),
                             Gender.get(),
                             Payday.get(),
                             Netpay.get(),
                             TaxCode.get(),
                             NINumber.get()))
                 
            
                 sqlcon.commit()
                 displaydata()
                 sqlcon.close()
                 tkinter.messagebox.showinfo("Data Entered Successfully❕❕","SUCCESSFULLY INSERTED")
                 Reset()
        
        #==================================================data========================================
        def displaydata():
             
             sqlcon=pymysql.connect(host="localhost",user="root",password="@slAmalef12",database="payroll")
             cur=sqlcon.cursor()
             cur.execute("select p.reference,p.name,p.address,p.cityweighting,p.basic_salary,p.over_time,p.gross_pay,p.pension,p.post_code,p.gender,p.pay_day,p.nett_pay,\
                          n.ni_number,n.ni_payments,t.tax_code,t.tax_period,t.tax \
                          from payroll_management p \
                          inner join ni_pay n on p.ni_number=n.ni_number\
                          inner join tax t on n.ni_number=t.ni_number")
             result=cur.fetchall()
             if len(result)!=0:
                 self.payroll_rec.delete(*self.payroll_rec.get_children())
                 for row in result:
                     self.payroll_rec.insert('',END,values=row)
                 sqlcon.commit()
        def clear_all():
             for item in self.payroll_rec.get_children():
                 self.payroll_rec.delete(item)
                 break
           
         
         
        def Wagesinfo(ev):
             view=self.payroll_rec.focus()
             learn=self.payroll_rec.item(view)
             row=learn['values']
             Reference.set(row[0])
             EmployerName.set(row[1])
             Address.set(row[2])
             CityWeighting.set(row[3])
             BasicSalary.set(row[4])
             OverTime.set(row[5])
             GrossPay.set(row[6])
             Pension.set(row[7])
             PostCode.set(row[8])
             Gender.set(row[9])
             Payday.set(row[10])
             Netpay.set(row[11])
             NINumber.set(row[12])
             NIPayments.set(row[13])
             TaxCode.set(row[14])
             TaxPeriod.set(row[15])
             Tax.set(row[16])
        def update():
             sqlcon=pymysql.connect(host="localhost",user="root",password="@slAmalef12",database="payroll")
             cur=sqlcon.cursor()
             cur.execute("update ni_pay set ni_payments=%s where ni_number=%s",(NIPayments.get(),NINumber.get()))
             cur.execute("update tax set Tax_period=%s,Tax=%s where tax_code=%s",(TaxPeriod.get(),Tax.get(),TaxCode.get()))
             cur.execute("update payroll_management set name=%s,address=%s,cityweighting=%s,basic_salary=%s,\
                          over_time=%s,gross_pay=%s,pension=%s,post_code=%s,gender=%s,\
                           pay_day=%s,nett_pay=%s where reference=%s",(
                               
                             EmployeeName.get(),
                             Address.get(),
                             CityWeighting.get(),
                             BasicSalary.get(),
                             OverTime.get(),
                             GrossPay.get(),
                             Pension.get(),
                             PostCode.get(),
                             Gender.get(),
                             Payday.get(),
                             Netpay.get(),
                             Reference.get())) 
                             
             sqlcon.commit()
             sqlcon.close()
             displaydata()
             tkinter.messagebox.showinfo("Data Entered Successfully❕❕","SUCCESSFULLY UPDATED✨")                
                             
                             
        def deleteDB():
             sqlcon=pymysql.connect(host="localhost",user="root",password="@slAmalef12",database="payroll")
             cur=sqlcon.cursor()
             cur.execute("delete from payroll_management where reference=%s",Reference.get())
             cur.execute("delete from tax where Tax_code=%s",TaxCode.get())
             cur.execute("delete from ni_pay where NI_Number=%s",NINumber.get())
             sqlcon.commit()
             sqlcon.close()
             displaydata()
             Reset()
             clear_all()
             tkinter.messagebox.showinfo("Data Deleted Successfully❕❕","SUCCESSFULLY DELETED✨") 
             
                             
                              
                              
                             
                             

           
           


            
        
        

       #--------------------------------FRAMES--------------------------------------------
        Tab1 = Frame(self.control1, bd=10, width=1350, height=700,relief=RIDGE)
        Tab1.grid()
        Tab2 = Frame(self.control2, bd=10, width=1350, height=700,relief=RIDGE)
        Tab2.grid()
        Tab3 = Frame(self.control3, bd=10, width=1350, height=700,relief=RIDGE)
        Tab3.grid()


        topframe1=Frame(Tab1, bd=10, width=1340, height=100, relief=RIDGE)
        topframe1.grid()
        topframe2=Frame(Tab1, bd=10, width=1340, height=100, relief=RIDGE)
        topframe2.grid()
        topframe3=Frame(Tab1, bd=10, width=1340, height=500, relief=RIDGE)
        topframe3.grid()

        leftframe=Frame(topframe3, bd=5, width=1340, height=400, padx=2,bg="VioletRed2",relief=RIDGE)
        leftframe.pack(side=RIGHT)
        leftframe1=Frame(leftframe, bd=5, width=600, height=180, padx=2,relief=RIDGE)
        leftframe1.pack(side=TOP)

        leftframe2=Frame(leftframe, bd=5, width=600, height=180, padx=2, bg="VioletRed2" ,relief=RIDGE)
        leftframe2.pack(side=TOP)
        leftframe2left=Frame(leftframe2, bd=5, width=300, height=170, padx=2 ,relief=RIDGE)
        leftframe2left.pack(side=LEFT)
        leftframe2right=Frame(leftframe2, bd=5, width=300, height=170, padx=2 ,relief=RIDGE)
        leftframe2right.pack(side=RIGHT)


        leftframe3left=Frame(leftframe, bd=5, width=320, height=50, padx=2, bg="VioletRed2", relief=RIDGE)
        leftframe3left.pack(side=LEFT)
        leftframe3right=Frame(leftframe, bd=5, width=320, height=50, padx=2, bg="VioletRed2", relief=RIDGE)
        leftframe3right.pack(side=RIGHT)

        rightframe1=Frame(topframe3, bd=5, width=320, height=400, padx=2, bg="VioletRed2", relief=RIDGE)
        rightframe1.pack(side=RIGHT)
        rightframe1a=Frame(rightframe1, bd=5, width=310, height=300, padx=2, relief=RIDGE)
        rightframe1a.pack(side=TOP)
        rightframe1b=Frame(rightframe1, bd=5, width=310, height=100, padx=2, relief=RIDGE)
        rightframe1b.pack(side=TOP)

        rightframe2=Frame(topframe3, bd=5, width=300, height=400, padx=2, bg="VioletRed2", relief=RIDGE)
        rightframe2.pack(side=LEFT)
        rightframe2a=Frame(rightframe2, bd=5, width=280, height=50, padx=2, relief=RIDGE)
        rightframe2a.pack(side=TOP)
        rightframe2b=Frame(rightframe2, bd=5, width=280, height=180, padx=2, relief=RIDGE)
        rightframe2b.pack(side=TOP)
        rightframe2c=Frame(rightframe2, bd=5, width=280, height=180, padx=2, relief=RIDGE)
        rightframe2c.pack(side=TOP)
        rightframe2d=Frame(rightframe2, bd=5, width=280, height=50, padx=2, bg="VioletRed2", relief=RIDGE)
        rightframe2d.pack(side=TOP)
        #------------------------------------TITTLE MAIN TITTLE-----------------------------------------------------
        self.toptittle=Label(topframe1, font=('stylus',40,'bold'),text="\tPAYROLL MANAGEMENT SYSTEM\t",justify=CENTER)
        self.toptittle.grid(padx=76)
        #----------------------------------------EMPLOYEE-------------------------------------------------
        self.employeename=Label(topframe2, font=('stylus',12,'bold'),text="EMPLOYEE NAME",bd=10)
        self.employeename.grid(row=0,column=0,sticky=W)
        self.txtemployeename=Entry(topframe2, font=('stylus',12,'bold'),bd=5,width=59,justify='left',textvariable= EmployeeName)
        self.txtemployeename.grid(row=0,column=1) 
        #-----------------------------------------ADDRESS---------------------------------------------------------
        self.lbladdress=Label(topframe2, font=('stylus',12,'bold'),text="ADDRESS",bd=10)
        self.lbladdress.grid(row=1,column=0,sticky=W)
        self.txtaddress=Entry(topframe2, font=('stylus',12,'bold'),bd=5,width=60,justify='left',textvariable=Address)
        self.txtaddress.grid(row=1,column=1)
        #-----------------------------------------POST CODE-------------------------------------------------------
        self.lblpostcode=Label(topframe2, font=('stylus',12,'bold'),text="POST CODE",bd=10)
        self.lblpostcode.grid(row=0,column=2,sticky=W)
        self.txtpostcode=Entry(topframe2, font=('stylus',12,'bold'),bd=5,width=50,justify='left',textvariable= PostCode)
        self.txtpostcode.grid(row=0,column=3)
        #------------------------------------------GENDER-------------------------------------------------------------
        self.lblgen=Label(topframe2, font=('stylus',12,'bold'),text="GENDER",bd=10)
        self.lblgen.grid(row=1,column=2,sticky=W)
        self.gen=ttk.Combobox(topframe2,textvariable= Gender,state='readonly',font=('stylus',12,'bold'),width=46)
        self.gen['value']=('NOT MENTION','Female','Male')
        self.gen.current(0)
        self.gen.grid(row=1,column=3)
        #-----------------------------------------PAY DAY----------------------------------------------------------------
        self.lbpayday=Label(rightframe2a,font=('stylus',12,'bold'),text="PAY DAY",bd=10)
        self.lbpayday.grid(row=0,column=0,sticky=W)
        self.txtpayday=Entry(rightframe2a, font=('stylus',12,'bold'),bd=5,width=20,justify='left',textvariable=Payday,state=DISABLED)
        self.txtpayday.grid(row=0,column=1)
        #---------------------------------------------TAX PERIOD-------------------------------------------------------------------------
        
        self.lbtaxperiod=Label(rightframe2b,font=('stylus',12,'bold'),text="TAX PERIOD",bd=10)
        self.lbtaxperiod.grid(row=0,column=0,sticky=W)
        self.txttaxperiod=Entry(rightframe2b, font=('stylus',12,'bold'),bd=5,width=17,justify='left',textvariable=TaxPeriod,state=DISABLED)
        self.txttaxperiod.grid(row=0,column=1)

        #-----------------------------------------------TAX CODE---------------------------------------------------------------------------------------------------------
        self.lbtaxcode=Label(rightframe2b,font=('stylus',12,'bold'),text="TAX CODE",bd=10)
        self.lbtaxcode.grid(row=1,column=0,sticky=W)
        self.txttaxcode=Entry(rightframe2b, font=('stylus',12,'bold'),bd=5,width=17,justify='left',textvariable=TaxCode,state=DISABLED)
        self.txttaxcode.grid(row=1,column=1)
        #-----------------------------------------------NATIONAL INSURANCE NUMBER------------------------------------------------------------------------------------------
        self.lbninum=Label(rightframe2b,font=('stylus',12,'bold'),text="NI NUMBER",bd=10)
        self.lbninum.grid(row=2,column=0,sticky=W)
        self.txtninum=Entry(rightframe2b, font=('stylus',12,'bold'),bd=5,width=17,justify='left',textvariable=NINumber,state=DISABLED)
        self.txtninum.grid(row=2,column=1)
        #-----------------------------------------------TAXABLE PAY-------------------------------------------------------------------------------------------------------------------
        self.lbtaxpay=Label(rightframe2c,font=('stylus',12,'bold'),text="TAXABLE PAY",bd=10)
        self.lbtaxpay.grid(row=0,column=0,sticky=W)
        self.txttaxpay=Entry(rightframe2c, font=('stylus',12,'bold'),bd=5,width=11,justify='left',textvariable=TaxablePay,state=DISABLED)
        self.txttaxpay.grid(row=0,column=1)

        #----------------------------------------------PENSIONABLE PAY-----------------------------------------------------------------------
        
        self.lbppay=Label(rightframe2c,font=('stylus',12,'bold'),text="PENSIONABLE PAY",bd=10)
        self.lbppay.grid(row=1,column=0,sticky=W)
        self.txtppay=Entry(rightframe2c, font=('stylus',12,'bold'),bd=5,width=11,justify='left',textvariable=PensionablePay,state=DISABLED)
        self.txtppay.grid(row=1,column=1)

        #---------------------------------------------------NETT PAY--------------------------------------------------------------------
        self.lbnetpay=Label(rightframe2d,font=('stylus',12,'bold'),text="NETT PAY",bd=10)
        self.lbnetpay.grid(row=0,column=0,sticky=W)
        self.txtnetpay=Entry(rightframe2d, font=('stylus',12,'bold'),bd=5,width=19,justify='left',textvariable=Netpay,state=DISABLED)
        self.txtnetpay.grid(row=0,column=1)
        #--------------------------------------------------------REFERENCE--------------------------------------------------------
        self.lbref=Label(leftframe1,font=('stylus',12,'bold'),text="REFERENCE",bd=10)
        self.lbref.grid(row=0,column=0,sticky=W)
        self.txtref=Entry(leftframe1, font=('stylus',12,'bold'),bd=5,width=57,justify='left',textvariable=Reference,state=DISABLED)
        self.txtref.grid(row=0,column=1)
        #----------------------------------------------------------EMPLOYER NAME--------------------------------------------------
        self.lbempname=Label(leftframe1,font=('stylus',12,'bold'),text="EMPLOYER NAME",bd=10)
        self.lbempname.grid(row=1,column=0,sticky=W)
        self.txtempname=Entry(leftframe1, font=('stylus',12,'bold'),bd=5,width=57,justify='left',textvariable=EmployerName)
        self.txtempname.grid(row=1,column=1)
        #------------------------------------------------------------EMPLOYEE NAME----------------------------------------------------
        self.lbempname=Label(leftframe1,font=('stylus',12,'bold'),text="EMPLOYEE NAME",bd=10)
        self.lbempname.grid(row=2,column=0,sticky=W)
        self.txtempname=Entry(leftframe1, font=('stylus',12,'bold'),bd=5,width=57,justify='left',textvariable=EmployeeName,state=DISABLED)
        self.txtempname.grid(row=2,column=1)
        #-------------------------------------------------------------CITY WEIGHTING-----------------------------------------------------
        self.lbctywe=Label(leftframe2left,font=('stylus',12,'bold'),text="CITY WEIGHTING",bd=10,anchor='e')
        self.lbctywe.grid(row=0,column=0,sticky=W)
        self.txtctywe=Entry(leftframe2left, font=('stylus',12,'bold'),bd=5,width=20,justify='left',textvariable=CityWeighting)
        self.txtctywe.grid(row=0,column=1)
        #------------------------------------------------------------BASIC SALARY-------------------------------------------------------------
        self.lbbsal=Label(leftframe2left,font=('stylus',12,'bold'),text="BASIC SALARY",bd=10)
        self.lbbsal.grid(row=1,column=0,sticky=W)
        self.txtbsal=Entry(leftframe2left, font=('stylus',12,'bold'),bd=5,width=20,justify='left',textvariable=BasicSalary)
        self.txtbsal.grid(row=1,column=1)
        #------------------------------------------------------------OVER TIME--------------------------------------------------------------
        self.lbotpay=Label(leftframe2left,font=('stylus',12,'bold'),text="OVER TIME",bd=10)
        self.lbotpay.grid(row=2,column=0,sticky=W)
        self.txtotpay=Entry(leftframe2left, font=('stylus',12,'bold'),bd=5,width=20,justify='left',textvariable=OverTime)
        self.txtotpay.grid(row=2,column=1)
        #-----------------------------------------------------------OTHER PAY------------------------------------------------------

        self.lbopay=Label(leftframe2left,font=('stylus',12,'bold'),text="OTHER PAY",bd=10)
        self.lbopay.grid(row=3,column=0,sticky=W)
        self.txtopay=Entry(leftframe2left, font=('stylus',12,'bold'),bd=5,width=20,justify='left',textvariable=OtherPaymentDue)
        self.txtopay.grid(row=3,column=1)

        #----------------------------------------------------------------TAX-------------------------------------------------------
        self.lbtax=Label(leftframe2right,font=('stylus',12,'bold'),text="TAX",bd=10,anchor='e')
        self.lbtax.grid(row=0,column=0,sticky=W)
        self.txttax=Entry(leftframe2right, font=('stylus',12,'bold'),bd=5,width=20,justify='left',textvariable=Tax,state=DISABLED)
        self.txttax.grid(row=0,column=1)

        #------------------------------------------------------------------PENSION-----------------------------------------------
        

        self.lbpension=Label(leftframe2right,font=('stylus',12,'bold'),text="PENSION",bd=10)
        self.lbpension.grid(row=1,column=0,sticky=W)
        self.txtpension=Entry(leftframe2right, font=('stylus',12,'bold'),bd=5,width=20,justify='left',textvariable=Pension,state=DISABLED)
        self.txtpension.grid(row=1,column=1)
        #-----------------------------------------------------------------STUDENT LOAN---------------------------------------------

        self.lbstloan=Label(leftframe2right,font=('stylus',12,'bold'),text="STUDENT LOAN",bd=10)
        self.lbstloan.grid(row=2,column=0,sticky=W)
        self.txtstloan=Entry(leftframe2right, font=('stylus',12,'bold'),bd=5,width=20,justify='left',textvariable=StudentLoan,state=DISABLED)
        self.txtstloan.grid(row=2,column=1)


        #-----------------------------------------------------------------NI PAYMENT---------------------------------------------
        self.lbnipay=Label(leftframe2right,font=('stylus',12,'bold'),text="NI PAYMENT",bd=10)
        self.lbnipay.grid(row=3,column=0,sticky=W)
        self.txtnipay=Entry(leftframe2right, font=('stylus',12,'bold'),bd=5,width=20,justify='left',textvariable=NIPayments,state=DISABLED)
        self.txtnipay.grid(row=3,column=1)


        #---------------------------------------------------GROSS PAY-----------------------------------------------------------
        self.lbgpay=Label(leftframe3left,font=('stylus',12,'bold'),text="GROSS PAY",bd=10)
        self.lbgpay.grid(row=3,column=0,sticky=W)
        self.txtgpay=Entry(leftframe3left, font=('stylus',12,'bold'),bd=5,width=25,justify='left',textvariable=GrossPay,state=DISABLED)
        self.txtgpay.grid(row=3,column=1)
        #----------------------------------------------------DEDUCTIONS-----------------------------------------------------------
        self.lbdpay=Label(leftframe3right,font=('stylus',12,'bold'),text="DEDUCTIONS",bd=10)
        self.lbdpay.grid(row=3,column=0,sticky=W)
        self.txtdpay=Entry(leftframe3right, font=('stylus',12,'bold'),bd=5,width=23,justify='left',textvariable=Deductions,state=DISABLED)
        self.txtdpay.grid(row=3,column=1)
        #------------------------------------------------------CALCULATOR------------------------------------------------------------

        self.txtdisplay=Entry(rightframe1a, font=('stylus',19,'bold'),bd=5,insertwidth=4,justify='right',textvariable=text_in)
        self.txtdisplay.grid(row=0,column=0,columnspan=4)

        #--------------------------------------------------------------------------------------------------
        self.btnwages=Button(rightframe1b,padx=16,pady=0,bd=5,font=('stylus',16,'bold'),width=4,text="WAGES",command=lambda:payment()).grid(row=0,column=0)
        self.btndisplay=Button(rightframe1b,padx=16,pady=0,bd=5,font=('stylus',16,'bold'),width=4,text="ADD",command=lambda:addData()).grid(row=0,column=1)
        self.btnupdate=Button(rightframe1b,padx=16,pady=0,bd=5,font=('stylus',16,'bold'),width=4,text="UPDATE",command=lambda:update()).grid(row=0,column=2)
        self.btndel=Button(rightframe1b,padx=16,pady=0,bd=5,font=('stylus',16,'bold'),width=4,text="DELETE",command=lambda:deleteDB()).grid(row=1,column=0)
        self.btnreset=Button(rightframe1b,padx=16,pady=0,bd=5,font=('stylus',16,'bold'),width=4,text="RESET",command=lambda:Reset()).grid(row=1,column=1)
        self.btnexit=Button(rightframe1b,padx=16,pady=0,bd=5,font=('stylus',16,'bold'),width=4,text="EXIT",command=lambda:Exit()).grid(row=1,column=2)
    


        self.btn1=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="1",command=lambda:btnClick(1)).grid(row=3,column=0)
        self.btn2=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="2",command=lambda:btnClick(2)).grid(row=3,column=1)
        self.btn3=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="3",command=lambda:btnClick(3)).grid(row=3,column=2)
        self.btnmul=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="x",command=lambda:btnClick("*")).grid(row=3,column=3)
        #---------------------------------------------------------------------------------------------------------------
        
        self.btn4=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="4",command=lambda:btnClick(4)).grid(row=2,column=0)
        self.btn5=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="5",command=lambda:btnClick(5)).grid(row=2,column=1)
        self.btn6=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="6",command=lambda:btnClick(6)).grid(row=2,column=2)
        self.btnsub=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="-",command=lambda:btnClick("-")).grid(row=2,column=3)
        #------------------------------------------------------------------------------------------------------------------
        self.btn7=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="7",command=lambda:btnClick(7)).grid(row=1,column=0)
        self.btn8=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="8",command=lambda:btnClick(8)).grid(row=1,column=1)
        self.btn9=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="9",command=lambda:btnClick(9)).grid(row=1,column=2)
        self.btnadd=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="+",command=lambda:btnClick("+")).grid(row=1,column=3)

        #---------------------------------------------------------BUTTON----------------------------------------------------------------

        self.btn0=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="0",command=lambda:btnClick(0)).grid(row=4,column=0)
        self.btnclear=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="C",command=lambda:btnClear()).grid(row=4,column=1)
        self.btnEqual=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="=",command=lambda:btnEquals()).grid(row=4,column=2)
        self.btndiv=Button(rightframe1a,padx=6,pady=6,bd=2,font=('stylus',16,'bold'),width=4,text="/",command=lambda:btnClick("/")).grid(row=4,column=3)

        #---------------------------------------------------------TAB-2----------------------------------------------------------------
        topframe11=Frame(Tab2,bd=10,width=1340,height=100,relief=RIDGE)
        topframe11.grid(row=0,column=0)
        topframe12=Frame(Tab2,bd=10,width=1340,height=100,relief=RIDGE)
        topframe12.grid(row=1,column=0)
        self.toptittle11=Label(topframe11, font=('stylus',40,'bold'),text="\tPAYROLL MANAGEMENT SYSTEM\t",bd=10,justify=CENTER)
        self.toptittle11.grid(padx=72)


        scroll_x=Scrollbar(topframe12,orient=HORIZONTAL)
        scroll_y=Scrollbar(topframe12,orient=VERTICAL)
        self.payroll_rec=ttk.Treeview(topframe12,height=22,columns=("ref","Fullname","Address","Cityweighting","Basicsalary","Overtime","Grosspay"
                                                                     ,"Pension","Postcode","Gender","Payday","Netpay","Ninumber","Nipayment","Taxcode","Taxperiod",
                                                                     "Tax"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        self.payroll_rec.heading("ref",text="Ref")
         
        self.payroll_rec.heading("Fullname",text="Fullname")
         
         
        self.payroll_rec.heading("Address",text="Address")
        self.payroll_rec.heading("Cityweighting",text="Cityweighting")
        self.payroll_rec.heading("Basicsalary",text="Basicsalary")
        self.payroll_rec.heading("Overtime",text="Overtime")
        self.payroll_rec.heading("Grosspay",text="Grosspay")
        self.payroll_rec.heading("Pension",text="Pension")
        self.payroll_rec.heading("Postcode",text="Postcode")
        self.payroll_rec.heading("Gender",text="Gender")
        self.payroll_rec.heading("Payday",text="Payday")
        self.payroll_rec.heading("Netpay",text="Netpay")
        self.payroll_rec.heading("Ninumber",text="Ninumber")
        self.payroll_rec.heading("Nipayment",text="Nipayment")
        self.payroll_rec.heading("Taxcode",text="Taxcode")
        self.payroll_rec.heading("Taxperiod",text="Taxperiod")
        self.payroll_rec.heading("Tax",text="Tax")
       

       
        self.payroll_rec['show']='headings'
        #==========================================================
        self.payroll_rec.column("ref",width=70)
        self.payroll_rec.column("Fullname",width=70)
        self.payroll_rec.column("Address",width=70)
        self.payroll_rec.column("Cityweighting",width=70)
        self.payroll_rec.column("Basicsalary",width=70)
        self.payroll_rec.column("Overtime",width=70)
        self.payroll_rec.column("Grosspay",width=70)
        self.payroll_rec.column("Pension",width=70)
        self.payroll_rec.column("Postcode",width=70)
        self.payroll_rec.column("Gender",width=70)
        self.payroll_rec.column("Payday",width=70)
        self.payroll_rec.column("Netpay",width=70)
        self.payroll_rec.column("Ninumber",width=70)
        self.payroll_rec.column("Nipayment",width=70)
        self.payroll_rec.column("Taxcode",width=70)
        self.payroll_rec.column("Taxperiod",width=70)
        self.payroll_rec.column("Tax",width=70)
        self.payroll_rec.pack(fill=BOTH,expand=1)
        self.payroll_rec.bind("<ButtonRelease-1>",Wagesinfo)
        displaydata()
       
        #=============================================================================
        topframe13=Frame(Tab3,bd=10,width=1340,height=100,relief=RIDGE)
        topframe13.grid(row=0,column=0)
        self.toptittle13=Label(topframe13, font=('stylus',40,'bold'),text="\tPAYROLL COMMENTBOOK\t",bd=10,justify=CENTER)
        self.toptittle13.grid(row=0,column=0)
        #==============================================================================
        self.txtcmt=Text(topframe13,width=100,height=22,font=('stylus',14,'bold'))
        self.txtcmt.grid(row=1,column=0)
        
      

      









#CREATING MAIN FUNCTION
if __name__=='__main__':
    root=Tk()
    application = Payroll(root)
