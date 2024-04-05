from typing import Dict, List,Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Depends, FastAPI, Request, Form,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.encoders import jsonable_encoder
# from models.schemas import masterSchemas
import base64
import shutil,uuid
from configs.base_config import BaseConfig
from jose import jwt, JWTError
# from django.contrib import messages
from datetime import datetime 
from models import get_db, models
from sqlalchemy.orm import Session
from sqlalchemy import text,desc
from icecream import ic

router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()


@router.get("/ticket")
async def getting(request:Request,db: Session = Depends(get_db)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            employee_data=db.query(models.Employee).filter(models.Employee.status=="ACTIVE").all()
                            client_data=db.query(models.Client).filter(models.Client.status=="ACTIVE").all()
                            emp=db.query(models.Tickets).filter(models.Tickets.status=='ACTIVE').all()
                            def gen_id():
                                try:
                                    db_len = len(db.query(models.Tickets).all())
                                    return "TKT_"+str(100+int(db_len))
                                except:
                                    return "TKT_100"
                            return templates.TemplateResponse("Admin/Employees/Tickets/tickets.html",context={"request":request,'emp_data':emp_data,"emp":emp,"employee_data":employee_data,"client_data":client_data,'gen_id':gen_id()})
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
@router.get('/getSelectId/{main_id}')
def  getSelectId(main_id:int,request:Request,db:Session=Depends(get_db)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            employeeData=db.query(models.Employee).filter(models.Employee.id==main_id).filter(models.Employee.status=='ACTIVE').first();
                            return {"employeeData":employeeData}
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
@router.post("/add_ticket")
async def add(request:Request,db: Session = Depends(get_db),aticketsubject:str=Form(...),aticketid:str=Form(...),aclient:str=Form(...), apriority:str=Form(...), acc:str=Form(...), aassign:str=Form(...), adescription:str=Form(...), aaddfollowers:str=Form(...), auploadfiles:UploadFile=File(...)): 
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                # try:
                if loginer_id:
                    emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                    if emp_data.Lock_screen == 'OFF':

                        file_type = auploadfiles.content_type;extention = file_type.split('/')[-1]
    
                        if extention != 'application/octet-stream':
                            token_image = str(uuid.uuid4()) + '.' + str(extention)
                            file_location = f"./templates/assets/uploaded_files/{token_image}"
                            with open(file_location, 'wb+') as file_object:
                                shutil.copyfileobj(auploadfiles.file,file_object)

                        tickets_data = db.query(models.Tickets).filter(models.Tickets.status=='ACTIVE').all()

                        # =====>> First Time Data Entered  
                        if not tickets_data:
                            check_exit_data = db.query(models.Tickets).filter(models.Tickets.Ticket_Subject==aticketsubject,models.Tickets.Client_id==aclient).filter(models.Tickets.status=='ACTIVE').all()
                            if not check_exit_data:
                                new_tickets = models.Tickets(Ticket_Subject=aticketsubject,Ticket_Id=aticketid,Loginer=loginer_id,Client_id=aclient,Priority=apriority,CC=acc,Assign_id=aassign,Description=adescription,Files=token_image,Today_Tickets=1,Today_Tickets_percent=100,Solved_Tickets=0,Solved_Tickets_percent=0,Open_Tickets=0,Open_Tickets_percent=0,Pending_Tickets=1,Pending_Tickets_percent=100,Current_status='New',status='ACTIVE',created_by=loginer_id)
                                db.add(new_tickets)
                                db.commit()
                                db.refresh(new_tickets)

                                #=====>Followers
                                ic(aaddfollowers)
                                splited_data = aaddfollowers.split(',')
                                ic(splited_data)
                                for i in splited_data:
                                    ic(i)
                                    new_followers = models.Tickets_Followers(Ticket_id=new_tickets.id,Employee_id=str(i),status='ACTIVE',created_by=loginer_id)
                                    db.add(new_followers)
                                    db.commit()
                                    db.refresh(new_followers)

                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({'Result':'Error'})
                                return JSONResponse(content=response_data,status_code=200)
                        else:
                            yesterday_ticket_data = db.query(models.Tickets).filter(models.Tickets.status=='ACTIVE').order_by(desc(models.Tickets.id)).first()

                            new_tickets_count = db.query(models.Tickets).filter(models.Tickets.Current_status=='New').filter(models.Tickets.status=='ACTIVE').all()
                            solved_ticket_count = db.query(models.Tickets).filter(models.Tickets.Current_status=='Closed').filter(models.Tickets.status=='ACTIVE').all()
                            open_ticket_count = db.query(models.Tickets).filter(models.Tickets.Current_status=='Open').filter(models.Tickets.status=='ACTIVE').all()
                            pending_ticket_count = db.query(models.Tickets).filter(models.Tickets.Current_status!='New',models.Tickets.Current_status!='Closed',models.Tickets.Current_status!='Open').filter(models.Tickets.status=='ACTIVE').all()

                            def count_data(datas):
                                try:
                                    return len(datas)
                                except:
                                    return 0
                                
                            # def percent_data(info):
                            #     try:
                            #         total_data = len(info)


                            # tickets_data = models.Tickets(Ticket_Subject=aticketsubject,Ticket_Id=aticketid,Loginer=loginer_id,Client_id=aclient,Priority=apriority,CC=acc,Assign_id=aassign,Description=adescription,Files=token_image,Today_Tickets=count_data(new_tickets_count),Today_Tickets_percent=,Solved_Tickets,Solved_Tickets_percent,Open_Tickets,Open_Tickets_percent,Current_status='New',status='ACTIVE',created_by=loginer_id)

                            

                        return RedirectResponse("/HrmTool/Employee/ticket",status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                else:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/Error',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
####delete_API
@router.get("/delete/{id}")
async def deleting(request:Request,db: Session = Depends(get_db)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            statuss="Inactive"
                            body=db.query(models.Tickets).filter(models.Tickets.id==id).first()
                            body.Current_status=statuss
                            db.add(body)
                            db.commit()
                            return templates.TemplateResponse("tickets.html",context={"request":request})
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
@router.get("/del_tickets/{ids}")
def taking_dlt_id_addition(request: Request,ids:int,db: Session = Depends(get_db)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            db.query(models.Tickets).filter(models.Tickets.id == ids).update({"status":"INACTIVE"})
                            db.commit()
                            return RedirectResponse('/HrmTool/Employee/ticket',status_code=302)
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
@router.post("/edit_tickets")
def edit_tickets(request: Request, db: Session = Depends(get_db),edit_id:str= Form(...),eticketsubject:str=Form(...), eticketid:str=Form(...), eassignstaff:str=Form(...), eclient:str=Form(...), epriority:str=Form(...), ecc:str=Form(...), eassign:str=Form(...), eaddfollowers:str=Form(...), edescription:str=Form(...), euploadfiles:UploadFile=Form(...) ):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            a = db.query(models.Tickets).filter(models.Tickets.status=='isactive').all()
                            print(eticketsubject)
                            db.query(models.Tickets).filter(models.Tickets.id==edit_id).update({"Ticket_Subject": eticketsubject, "Ticket_Id": eticketid, "Employee_id": eassignstaff, "Client_id": eclient, "Priority": epriority, "CC": ecc ,"Assign_id": eassign ,"Description": edescription ,"Files": euploadfiles, "Current_status": '' })
                            # print(eticketsubject)
                            db.commit()
                            return RedirectResponse("/open",status_code=303)
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
@router.get("/ticket_edit_id/{ids}")       
def taking_edit_id_addition(ids:int,request:Request,db: Session = Depends(get_db)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            print("hello")
                            single_data = db.query(models.Tickets).filter(models.Tickets.id==ids).filter(models.Tickets.status=='ACTIVE').first()
                            employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            return single_data,employee_data
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
@router.get("/assigni_id/{ids}")
def taking_dlt_id_addition(request: Request,ids:int,db: Session = Depends(get_db)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            assigni_id = db.query(models.Employee).filter(models.Employee.id==ids).filter(models.Employee.status=='ACTIVE').first()
                            return assigni_id
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
   
@router.post("/ticket_followers_data")
def taking_dlt_id_addition(request: Request,db: Session = Depends(get_db),Followers:str=Form(...)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            splited_list = Followers.split(',')
                            followers_data = []
                            for i in splited_list:
                                employee_data = db.query(models.Employee).filter(models.Employee.id==int(i)).filter(models.Employee.status=='ACTIVE').first()
                                if employee_data:
                                    followers_data.append(employee_data)

                            response_data = jsonable_encoder({'Result':followers_data})
                            return JSONResponse(content=response_data,status_code=200)
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
@router.get("/ticket_emp_search/{data}")
def taking_dlt_id_addition(request: Request,data:str,db: Session = Depends(get_db)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            employee_data = db.query(models.Employee).from_statement(text(f"select * from employee where First_Name like '%{data}%' or Last_Name like '%{data}%' and status='ACTIVE'")).all()
                            store_data = []
                            def seperate_id():
                                if employee_data != []:
                                    for i in employee_data:
                                        ticket_data = db.query(models.Tickets).filter(models.Tickets.Assign_id == i.id ).filter(models.Tickets.status=='ACTIVE').first()
                                        if ticket_data !=None:
                                            store_data.append(ticket_data)
                            seperate_id()
                            return store_data,employee_data
                            
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
