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


def format_display_date(date_str):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    # Format the date as "day Month Year" (e.g., 12 May 2023)
    formatted_date = date_obj.strftime('%d %b %Y')
    return formatted_date


#grid view
@router.get('/projects')
def get_form(request:Request,db:Session = Depends(get_db)):
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
                            display = db.query(models.Project).filter(models.Project.status=='ACTIVE').all()
                            employee_ids = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            client_data = db.query(models.Client).filter(models.Client.status=='ACTIVE').all()
                            desig_data = db.query(models.Designation).filter(models.Designation.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Employees/Projects/projects.html",context={"request":request,'emp_data':emp_data,"display":display,"employee_ids":employee_ids,'client_data':client_data,'format_display_date':format_display_date,'desig_data':desig_data})
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
    
#list view
@router.get('/project_list')
def get_form(request:Request,db:Session = Depends(get_db)):
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
                            display = db.query(models.Project).filter(models.Project.status=='ACTIVE').all()
                            employee_ids = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            return templates.TemplateResponse("project-list.html",context={"request":request,'emp_data':emp_data,"display": display,"employee_ids":employee_ids})
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
    
# create data
@router.post("/create_project")
def create_data(request: Request, db: Session = Depends(get_db), Project_Name: str = Form(...),Client_id:str=Form(...),Start_Date: str = Form(...),End_Date: str = Form(...),Rate: str = Form(...),Priority: str = Form(...),Project_Leader_id: str = Form(...),Teams: str = Form(...),Description: str = Form(...),File: UploadFile  = File(...)):
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
                            client_data = db.query(models.Client).filter(models.Client.id==int(Client_id)).filter(models.Client.status=='ACTIVE').first()
                            #FILE CONVERTING 
                            file_type = File.content_type
                            extention = file_type.split('/')[-1]
                            if extention != 'applcation/octet-stream':
                                token_pdf = str(uuid.uuid4()) + '.' + str(extention)
                                file_location = f"./templates/assets/uploaded_files/{token_pdf}"
                                with open(file_location, 'wb+') as file_object:
                                    shutil.copyfileobj(File.file,file_object)

                            add_project = models.Project(Project_Name,Client_id,Start_Date,End_Date,Rate,Priority,Phone=client_data.Phone,Project_Leader_id=Project_Leader_id,Teams=Teams,Description=Description,File=token_pdf,Current_status='Active',status='ACTIVE',created_by=loginer_id)
                            db.add(add_project)
                            db.commit()
                            db.refresh(add_project)

                            return RedirectResponse('/HrmTool/Employee/projects',status_code=302)
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
    
#edit data
        
@router.get("/edit_projects/{ids}")       
def edit_projects(ids:int,request:Request,db: Session = Depends(get_db)):
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
                            data = db.query(models.Project).filter(models.Project.id==ids).filter(models.Project.status=='ACTIVE').first()
                            empl_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
                            return data,empl_data
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
    
@router.get("/edit_projectgrid/{ids}")       
def edit_projects(ids:int,request:Request,db: Session = Depends(get_db)):
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
                            data = db.query(models.Project).filter(models.Project.id==ids).filter(models.Project.status=='ACTIVE').first()
                            return data
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
    
@router.post("/update_project")
def create_data(request: Request, db: Session = Depends(get_db),pagetype:str=Form(...),edit_id:int=Form(...), edit_projectname:str=Form(...),edit_clientid:str=Form(...),edit_startdate:str=Form(...), edit_enddate:str=Form(...), edit_rate:str=Form(...),edit_priority:str=Form(...),edit_projectleaderid:str=Form(...),edit_teams:str=Form(...),edit_description:str=Form(...), edit_file:UploadFile=File(...)):
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
                            if pagetype == "grid":
                                db.query(models.Project).filter(models.Project.id==edit_id).update({"Project_Name":edit_projectname,"Client_id":edit_clientid,"Start_Date":edit_startdate,"End_Date":edit_enddate,"Rate":edit_rate,"Priority":edit_priority,"Project_Leader_id":edit_projectleaderid,"Teams":edit_teams,"Description":edit_description, "File":edit_file})
                                db.commit()
                                return RedirectResponse("/projects",status_code=303)
                            else:
                                db.query(models.Project).filter(models.Project.id==edit_id).update({"Project_Name":edit_projectname,"Client_id":edit_clientid,"Start_Date":edit_startdate,"End_Date":edit_enddate,"Rate":edit_rate,"Priority":edit_priority,"Project_Leader_id":edit_projectleaderid,"Teams":edit_teams,"Description":edit_description, "File":edit_file})
                                db.commit()
                                return RedirectResponse("/project_list",status_code=303)
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
    
#delete data
@router.get("/delete_project/{ids}")
def delete_project(request: Request,ids:int,db: Session = Depends(get_db)):
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
                            delete_ids = db.query(models.Project).filter(models.Project.status=='ACTIVE').all()
                            db.query(models.Project).filter(models.Project.id == ids).update({"status":"INACTIVE"})
                            db.commit()
                            return templates.TemplateResponse("project-list.html",context={"request":request,'emp_data':emp_data})
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
    
#delete data

@router.get("/delete_projectgrid/{ids}")
def delete_project(request: Request,ids:int,db: Session = Depends(get_db)):
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
                            delete_ids = db.query(models.Project).filter(models.Project.status=='ACTIVE').all()
                            db.query(models.Project).filter(models.Project.id == ids).update({"status":"INACTIVE"})
                            db.commit()
                            return templates.TemplateResponse("projects.html",context={"request":request,'emp_data':emp_data,'delete_ids':delete_ids})
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
    
@router.get("/search_name/{data}")
def delete_project(request: Request,data:str,db: Session = Depends(get_db)):
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
                            search_data = db.query(models.Project).from_statement(text(f'select * from project where Project_Name like "%{data}%" and status="ACTIVE" ')).all()
                            return JSONResponse(content={'search_data':search_data})
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
    
@router.get("/search_employee/{data}")
def delete_project(request: Request,data:str,db: Session = Depends(get_db)):
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
                            search_data = db.query(models.Project).from_statement(text(f'select * from project where id like "%{data}%" and status="ACTIVE" ')).all()
                            return JSONResponse(content={'search_data':search_data})
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
    
@router.get("/search_role/{data}")
def delete_project(request: Request,data:str,db: Session = Depends(get_db)):
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
                            search_data = db.query(models.Project).from_statement(text(f'select * from project where Project_Name like "%{data}%" and status="ACTIVE" ')).all()
                            return JSONResponse(content={'search_data':search_data}) 
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
    

