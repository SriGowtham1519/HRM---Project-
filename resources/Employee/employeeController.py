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
from sqlalchemy import text

router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()

#                                                       ***** C L I E N T   P A G E *****

@router.get("/emplyee")
async def getting(request:Request,db:Session=Depends(get_db)):
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

                            depart_data=db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            d_id=db.query(models.Designation).filter(models.Designation.status=='ACTIVE').all()
                            cid=db.query(models.Client).filter(models.Client.status=='ACTIVE').all()
                            emp=db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            #--------------->>>> 
                            company_data = db.query(models.Company_Settings).filter(models.Company_Settings.status=="ACTIVE").first()
                            def empy_id_gen():
                                try:
                                    emplyee_data = len(db.query(models.Employee).all())
                                    return 'EMP_ID'+str(100+int(emplyee_data))
                                except:
                                    return "EMP_ID"+str(100)
                            return templates.TemplateResponse("Admin/Employees/Employee/employees.html",context={"request":request,'emp_data':emp_data,"depart_data":depart_data,"d_id":d_id,"cid":cid,"emp":emp,'company_data':company_data,'empy_id_gen':empy_id_gen()})
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('Error',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
    
@router.post("/add_employee")
async def add(request:Request,db:Session=Depends(get_db),image:UploadFile=File(...),fname:str=Form(...),lname:str=Form(...),uname:str=Form(...),email:str=Form(...),password:str=Form(...),cpassword:str=Form(...),eid:str=Form(...),jdate:str=Form(...),phone:int=Form(...),company:str=Form(...),department:str=Form(...),designation:str=Form(...),bdate:str=Form(...),gender:str=Form(...),address:str=Form(...),state:str=Form(...),country:str=Form(...),pincode:int=Form(...),report:str=Form(...)):
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
                            file_type = image.content_type
                            extention = file_type.split('/')[-1]
                            if extention != 'routerlication/octet-stream':
                                file_location = f"./templates/assets/uploaded_files/{image.filename}"
                                with open(file_location, 'wb+') as file_object:
                                    shutil.copyfileobj(image.file,file_object)

                            find=db.query(models.Employee).filter(models.Employee.Employee_ID==eid).first()
                            if find is None:    
                                body=models.Employee(
                                    First_Name=fname,
                                    Last_Name=lname,
                                    Username=uname,
                                    Email=email,
                                    Password=password,
                                    Employee_ID=eid,
                                    Joining_Date=jdate,
                                    Phone=phone,
                                    Company_id=company,
                                    Department_id=department,
                                    Designation_id=designation,
                                    Current_status="Active",
                                    Birth_Date=bdate,
                                    Gender=gender,
                                    Address=address,
                                    State=state,
                                    Country=country,
                                    Pin_Code=pincode,
                                    Reports_To=report,
                                    Photo=image.filename,
                                    Lock_screen=password,
                                    status="ACTIVE",
                                    created_by=loginer_id)
                                db.add(body)
                                db.commit()

                                return RedirectResponse("/HrmTool/Employee/emplyee",status_code=302)
                            else:
                                return RedirectResponse("/HrmTool/Employee/emplyee",status_code=302)
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
    
###update_API

@router.put('/put_data/{id}')
def get_form(id: int, request: Request, db: Session = Depends(get_db)):
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
                            print(id)
                            result1 = db.query(models.Employee).filter(models.Employee.id == id and models.Employee.status == "active").first()
                            # print(result1)
                            json_compatible_item_data = jsonable_encoder(result1)
                            return JSONResponse(content=json_compatible_item_data)
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
    
@router.post("/update")
async def updating(request:Request,db:Session=Depends(get_db),edit_id:int=Form(...),eimage:UploadFile=File(...),efname:str=Form(...),elname:str=Form(...),euname:str=Form(...),eemail:str=Form(...),epassword:str=Form(...),ejdate:str=Form(...),ephone:str=Form(...),ecompany:str=Form(...),edepartment:str=Form(...),edesignation:str=Form(...),ebdate:str=Form(...),egender:str=Form(...),eaddress:str=Form(...),estate:str=Form(...),ecountry:str=Form(...),epincode:str=Form(...),ereport:str=Form(...)):
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
                            file_type = eimage.content_type
                            extention = file_type.split('/')[-1]
                            if extention != 'octet-stream':
                                file_location = f"./templates/assets/uploaded_files/{eimage.filename}"
                                with open(file_location, 'wb+') as file_object:
                                    shutil.copyfileobj(eimage.file,file_object)
                                    db.query(models.Employee).filter(models.Employee.id==edit_id).update({'Photo':eimage.filename})
                                    db.commit()

                            db.query(models.Employee).filter(models.Employee.id==edit_id).update({
                                'First_Name':efname,
                                'Last_Name':elname,
                                'Username':euname,
                                'Email':eemail,
                                'Password':epassword,
                                "Joining_Date":ejdate,
                                "Phone":ephone,
                                'Company_id':ecompany,
                                'Department_id':edepartment,
                                'Designation_id':edesignation,
                                'Birth_Date':ebdate,
                                'Gender':egender,
                                'Address':eaddress,
                                'State':estate,
                                'Country':ecountry,
                                'Pin_Code':epincode,
                                'Reports_To':ereport,
                                'Lock_screen':epassword,
                                'created_by':loginer_id
                            })
                            db.commit()
                            return RedirectResponse("/HrmTool/Employee/emplyee",status_code=302)
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
    

####delete_API
@router.get("/delete/{id}")
async def deleting(request:Request,id:int,db:Session=Depends(get_db)):
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
                            body=db.query(models.Employee).filter(models.Employee.id==id).first()
                            body.status="INACTIVE"
                            db.add(body)
                            db.commit()
                            return RedirectResponse('/HrmTool/Employee/emplyee',status_code=302)
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
    
#####search_data
@router.get("/searching_emp_id/{data}")
def delete_project(data:str,request: Request,db: Session = Depends(get_db)):
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
                            search_data = db.query(models.Employee).from_statement(text(f'select * from Employee where Employee_ID like "%{data}%" OR First_Name like "%{data}%" AND status="ACTIVE" ')).all()
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            return search_data,department_data
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
    
@router.get("/searching_designation/{data}")
def delete_project(data:int,request: Request,db: Session = Depends(get_db)):
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                try:
                    if loginer_id:
                        print(data)
                        emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                        if emp_data.Lock_screen == 'OFF':
                            search_data = db.query(models.Employee).filter(models.Employee.Department_id==str(data)).filter(models.Employee.status=='ACTIVE').all()
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            return search_data,department_data 
                        else:
                            return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                    else:
                        return RedirectResponse('/HrmTool/login/login',status_code=302)
                except:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
    