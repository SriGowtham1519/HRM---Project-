from typing import Dict, List,Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Depends, FastAPI, Request, Form,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse,RedirectResponse,HTMLResponse
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

# #grid view
# @router.get('/projects')
# def get_form(request:Request,db:Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         display = db.query(models.Project).filter(models.Project.status=='ACTIVE').all()
#                         employee_ids = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
#                         client = db.query(models.Client).filter(models.Client.status=='ACTIVE').all()
#                         emp = db.query(models.Employee).filter(models.Project.status=='ACTIVE').all()
#                         team = db.query(models.Project, models.Employee).join(models.Employee, models.Project.Teams == models.Employee.id).filter(models.Project.status=='ACTIVE').all()
#                         return templates.TemplateResponse("projects.html",context={"request":request,"display":display,"employee_ids":employee_ids,"emp":emp, "team":team, "client":client})
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)
    
# #list view
# @router.get('/project_list')
# def get_form(request:Request,db:Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         display = db.query(models.Project).filter(models.Project.status=='ACTIVE').all()
#                         employee_ids = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()
#                         emp = db.query(models.Employee).filter(models.Project.status=='ACTIVE').all()
#                         client = db.query(models.Client).filter(models.Client.status=='ACTIVE').all()
#                         team = db.query(models.Project, models.Employee).join(models.Employee, models.Project.Teams == models.Employee.id).filter(models.Project.status=='ACTIVE').all()
#                         return templates.TemplateResponse("project-list.html",context={"request":request,"display": display,"employee_ids":employee_ids,"emp":emp,"team":team, "client":client})
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)
    
# # create data
# @router.post("/create_project")
# async def create_data(request: Request, db: Session = Depends(get_db),pagetype:str=Form(...), Project_Name: str = Form(...),Client_id:str=Form(...),Start_Date: str = Form(...),End_Date: str = Form(...),Rate: str = Form(...),Priority: str = Form(...),Project_Leader_id: str = Form(...),Teams: str = Form(...),Description: Optional[str] = Form(None),File: UploadFile  = Form(...)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         # Fetch the phone number from the Employee table based on Project_Leader_id
#                         project_leader = db.query(models.Employee).filter(models.Employee.id == Project_Leader_id).first()
#                         phone_number = project_leader.Phone if project_leader else None

#                         find = db.query(models.Project).filter(models.Project.Project_Name == Project_Name,models.Project.Client_id == Client_id,models.Project.Start_Date == Start_Date, models.Project.End_Date == End_Date,models.Project.Rate == Rate,models.Project.Priority == Priority,models.Project.Project_Leader_id == Project_Leader_id,models.Project.Teams == Teams,models.Project.Description == Description,models.Project.File == File.filename,models.Project.Current_status == "Active",models.Project.status == "ACTIVE").first()
#                         file_content = await File.read()
#                         with open(File.filename, "wb") as pdf_file:
#                             pdf_file.write(file_content)

#                         if find is None:
#                             if pagetype=="grid":
#                                 body = models.Project(Project_Name=Project_Name,Client_id=Client_id,Start_Date=Start_Date,End_Date=End_Date,Rate=Rate,Priority=Priority,Phone=phone_number,Project_Leader_id=Project_Leader_id,Teams=Teams,Description=Description,File=File.filename,Current_status="Active",status="ACTIVE",created_by="")  # Set the phone attribute with the fetched value
#                                 db.add(body)
#                                 db.commit()
#                                 return RedirectResponse("/projects", status_code=303)
#                             else:
#                                 body = models.Project(Project_Name=Project_Name,Client_id=Client_id,Start_Date=Start_Date,End_Date=End_Date,Rate=Rate,Priority=Priority,Phone=phone_number,Project_Leader_id=Project_Leader_id,Teams=Teams,Description=Description,File=File.filename,Current_status="Active",status="ACTIVE",created_by="")  # Set the phone attribute with the fetched value
#                                 db.add(body)
#                                 db.commit()
#                                 return RedirectResponse("/project_list", status_code=303)
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)
    
# #edit data
# @router.get("/edit_projects/{ids}")       
# def edit_projects(ids:int,request: Request,db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         data = db.query(models.Project).filter(models.Project.id==ids).filter(models.Project.status=='ACTIVE').first()
#                         return data
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)
    
# @router.get("/edit_projectgrid/{ids}")       
# def edit_projects(ids:int,request: Request,db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         data = db.query(models.Project).filter(models.Project.id==ids).filter(models.Project.status=='ACTIVE').first()
#                         return data
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/Error',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)

# @router.post("/update_project")
# def create_data(request: Request, db: Session = Depends(get_db),pagetype:str=Form(...),edit_id:int=Form(...), edit_projectname:str=Form(...),edit_clientid:str=Form(...),edit_startdate:str=Form(...), edit_enddate:str=Form(...), edit_rate:str=Form(...),edit_priority:str=Form(...),edit_projectleaderid:str=Form(...),edit_teams:str=Form(...),edit_description:str=Form(...), edit_file:UploadFile=File(...)):
    
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         if pagetype == "grid":
#                             db.query(models.Project).filter(models.Project.id==edit_id).update({"Project_Name":edit_projectname,"Client_id":edit_clientid,"Start_Date":edit_startdate,"End_Date":edit_enddate,"Rate":edit_rate,"Priority":edit_priority,"Project_Leader_id":edit_projectleaderid,"Teams":edit_teams,"Description":edit_description, "File":edit_file})
#                             db.commit()
#                             return RedirectResponse("/projects",status_code=303)
#                         else:
#                             db.query(models.Project).filter(models.Project.id==edit_id).update({"Project_Name":edit_projectname,"Client_id":edit_clientid,"Start_Date":edit_startdate,"End_Date":edit_enddate,"Rate":edit_rate,"Priority":edit_priority,"Project_Leader_id":edit_projectleaderid,"Teams":edit_teams,"Description":edit_description, "File":edit_file})
#                             db.commit()
#                             return RedirectResponse("/project_list",status_code=303)
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)

# #delete data
# @router.get("/delete_project/{ids}")
# def delete_project(request: Request,ids:int,db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         delete_ids = db.query(models.Project).filter(models.Project.status=='ACTIVE').all()
#                         db.query(models.Project).filter(models.Project.id == ids).update({"status":"INACTIVE"})
#                         db.commit()
#                         return templates.TemplateResponse("project-list.html",context={"request":request})
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)

# #delete data
# @router.get("/delete_projectgrid/{ids}")
# def delete_project(request: Request,ids:int,db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         delete_ids = db.query(models.Project).filter(models.Project.status=='ACTIVE').all()
#                         db.query(models.Project).filter(models.Project.id == ids).update({"status":"INACTIVE"})
#                         db.commit()
#                         return templates.TemplateResponse("projects.html",context={"request":request,'delete_ids':delete_ids})
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)

# #search filter
# @router.get("/search_name/{data}")
# def delete_project(request: Request,data:str,db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         search_data = db.query(models.Project).from_statement(text(f'select * from project where Project_Name like "%{data}%" and status="ACTIVE" ')).all()
#                         return search_data
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)
    
# @router.get("/search_employee/{data}")
# def delete_project(request: Request,data:str,db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         search_data = db.query(models.Project).from_statement(text(f'select * from project where id like "%{data}%" and status="ACTIVE" ')).all()
#                         return search_data
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)
    
# @router.get("/search_role/{data}")
# def delete_project(request: Request,data:str,db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         search_data = db.query(models.Project).from_statement(text(f'select * from project where Project_Name like "%{data}%" and status="ACTIVE" ')).all()
#                         return search_data
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)
    
# @router.post('/update_status')
# async def update_status(request: Request,item_id: str=Form(...), new_status: str=Form(...), db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         # Check if the item exists in the database
#                         db.query(models.Project).filter(models.Project.id==item_id).update({"Current_status":new_status})
#                         db.commit()
#                         return {"status": "Update successful"}
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)
    
# @router.post('/update_priority')
# async def update_status(request: Request,item_id: str=Form(...), new_priority: str=Form(...), db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         # Check if the item exists in the database
#                         db.query(models.Project).filter(models.Project.id==item_id).update({"Priority":new_priority})
#                         db.commit()
#                         return {"status": "Update successful"}
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)
    

# #project report
# @router.get("/project_report")
# def project_reports(request: Request, db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         display = db.query(models.Project).filter(models.Project.status=='ACTIVE').all()
#                         emp = db.query(models.Employee).filter(models.Project.status=='ACTIVE').all()
#                         team = db.query(models.Project, models.Employee).join(models.Employee, models.Project.Teams == models.Employee.id).filter(models.Project.status=='ACTIVE').all()
#                         return templates.TemplateResponse("project-reports.html",context={"request":request, "display":display, "emp":emp, "team":team,})
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)

# @router.get("/search_project/{data}")
# def delete_project(data:str,request: Request,db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         print(data)
#                         search_data = db.query(models.Project).from_statement(text(f'select * from project where Project_Name like "%{data}%" AND status="ACTIVE"')).all()
#                         print(search_data)
#                         return search_data
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/HrmTool/login/login',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)
    
# @router.get("/search_status/{data}")
# def delete_project(data:str,request: Request,db: Session = Depends(get_db)):
#     if 'loginer_details' in request.session:
#         token = request.session['loginer_details']
#         try:
#             payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
#             loginer_id : int= payload.get("empid") 
#             try:
#                 if loginer_id:
#                     emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
#                     if emp_data.Lock_screen == 'OFF':
#                         print(data)
#                         search_data = db.query(models.Project).from_statement(text(f'select * from project where Current_status like "%{data}%" AND status="ACTIVE"')).all()
#                         print(search_data)
#                         return search_data
#                     else:
#                         return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
#                 else:
#                     return RedirectResponse('/HrmTool/login/login',status_code=302)
#             except:
#                 return RedirectResponse('/Error',status_code=302)
#         except JWTError:
#             return RedirectResponse('/HrmTool/login/login',status_code=302)
#     else:
#         return RedirectResponse('/HrmTool/login/login',status_code=303)

#holidays
@router.get('/holidays')
def holiday(request:Request,db:Session = Depends(get_db)):
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
                            display = db.query(models.Holiday_List).filter(models.Holiday_List.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Employees/Employee/holidays.html",context={"request":request, "display":display, "get_day_of_week": get_day_of_week, "is_past_date": is_past_date, "format_display_date":format_display_date,'emp_data':emp_data})
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
    
# create data
@router.post("/create_holiday")
def create_data(request: Request, db: Session = Depends(get_db), Name: str = Form(...), Date:str=Form(...)):
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
                            existing_date = db.query(models.Holiday_List).filter(models.Holiday_List.Date == Date, models.Holiday_List.status == "ACTIVE").first()
                            if not existing_date:
                                body = models.Holiday_List(Name=Name,Date=Date,Current_status="Active",status="ACTIVE",created_by=loginer_id)  
                                db.add(body)
                                db.commit()
                                return RedirectResponse("/HrmTool/Employee/holidays", status_code=303)
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
    
# edit
@router.get("/edit_holidays/{ids}")       
def edit_holidays(ids:int,request: Request,db: Session = Depends(get_db)):
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
                            data = db.query(models.Holiday_List).filter(models.Holiday_List.id==ids).filter(models.Holiday_List.status=='ACTIVE').first()
                            return data
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
    
@router.post("/update_holiday")
def create_data(request: Request, db: Session = Depends(get_db),edit_id:int=Form(...), edit_name:str=Form(...),edit_date:str=Form(...)):
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
                            existing_date = db.query(models.Holiday_List).filter(models.Holiday_List.Date == edit_date, models.Holiday_List.status == "ACTIVE").first()
                            if existing_date:
                                return HTMLResponse(
                                    """<script>
                                        alert("Holiday name already exists.");
                                        window.location.href = "/holidays";
                                    </script>""")
                            db.query(models.Holiday_List).filter(models.Holiday_List.id==edit_id).update({"Name":edit_name,"Date":edit_date})
                            db.commit()
                            return RedirectResponse("/holidays",status_code=303)
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
    
# delete
@router.get("/delete_holiday/{ids}")
def delete_data(request: Request,ids:int,db: Session = Depends(get_db)):
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
                            db.query(models.Holiday_List).filter(models.Holiday_List.id == ids).update({"status":"INACTIVE"})
                            db.commit()
                            return templates.TemplateResponse("holidays.html",context={"request":request})
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

#=========================>>> Function Used For Spare ...


def get_day_of_week(date_str):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    # Get the day of the week (e.g., Monday, Tuesday, etc.)
    day_of_week = date_obj.strftime('%A')
    return day_of_week

def is_past_date(date_str):
    today = datetime.now().date()
    date = datetime.strptime(date_str, '%d-%m-%Y').date()
    return date < today

def format_display_date(date_str):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    # Format the date as "day Month Year" (e.g., 12 May 2023)
    formatted_date = date_obj.strftime('%d %b %Y')
    return formatted_date
