from typing import Dict, List,Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Depends, FastAPI, Request, Form,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.encoders import jsonable_encoder
# from models.schemas import masterSchemas
import base64
import shutil,uuid,os,random
from configs.base_config import BaseConfig
from jose import jwt, JWTError
# from django.contrib import messages
from datetime import datetime 
from models import get_db, models
from sqlalchemy.orm import Session
from sqlalchemy import text
from icecream import ic
router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()

def Days_caluculating(start):
    # 02-02-2024
    # 
    total_days = start - current_datetime
#-----------------------------------------------------------------------------#
#---------------------------------- jobs  ------------------------------------#
#-----------------------------------------------------------------------------#

@router.get('/manage_jobs')
async def home(request:Request,db:Session=Depends(get_db)):
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
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            job_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Administration/Jobs/jobs.html",context={"request":request,'emp_data':emp_data,'department_data':department_data,'job_data':job_data})
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
       
@router.post('/post_manage_jobs')
async def emailSettings(request:Request,db:Session=Depends(get_db),j_name:str=Form(...),j_depart:str=Form(...),j_location:str=Form(...),j_vacans:str=Form(...),j_expery:str=Form(...),j_age:str=Form(...),j_salary_f:str=Form(...),j_salary_to:str=Form(...),j_type:str=Form(...),j_status:str=Form(...),j_start_date:str=Form(...),j_expire_date:str=Form(...),j_d:str=Form(...)):
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
                            job_data = models.Manage_Jobs(Job_Title=j_name,Department=j_depart,Job_Location=j_location,Vacancies=j_vacans,Experience=j_expery,Age=j_age,Salary_From=j_salary_f,Salary_To=j_salary_to,Job_Type=j_type,Current_Status=j_status,Start_Date=j_start_date,Expired_Date=j_expire_date,JD=j_d,Applicants=0,Total_days=0,Viewers=0,status="ACTIVE",created_by=loginer_id)                            
                            db.add(job_data)
                            db.commit()
                            db.refresh(job_data)
                            # ===============>>>> Graph part work 
                            department_data = db.query(models.Department).filter(models.Department.id==j_depart).filter(models.Department.status=='ACTIVE').first()
                            add_graph = models.Job_Graph(Department_id=j_depart,Department_Color=department_data.Colour,Applier_Count='0',Views_Count='0',Jan='0',Feb='0',Mar='0',Apr='0',May='0',Jun='0',Jul='0',Aug='0',Sep='0',Oct='0',Nov='0',Dec='0',status='ACTIVE',created_by=loginer_id)
                            db.add(add_graph)
                            db.commit()
                            db.refresh(add_graph)
                            return RedirectResponse('/HrmTool/Administration/manage_jobs',status_code=302)
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

@router.get('/job_details/{job_id}')
async def home(request:Request,job_id:int,db:Session=Depends(get_db)):
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
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            job_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==job_id).filter(models.Manage_Jobs.status=='ACTIVE').first()
                            return templates.TemplateResponse("Admin/Administration/Jobs/job_details.html",context={"request":request,'emp_data':emp_data,'department_data':department_data,'job_data':job_data})
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
        
@router.post('/edit_post_manage_jobs')
async def emailSettings(request:Request,db:Session=Depends(get_db),page_address:str=Form(...),edit_id:int=Form(...),edit_title:str=Form(...),edit_depart:str=Form(...),edit_location:str=Form(...),edit_vacancy:str=Form(...),edit_experience:str=Form(...),edit_age:str=Form(...),edit_from_salary:str=Form(...),edit_to_salary:str=Form(...),edit_type:str=Form(...),edit_status:str=Form(...),edit_start:str=Form(...),edit_end_date:str=Form(...),edit_jd:str=Form(...)):
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
                            if page_address == '/HrmTool/Administration/job_details/':
                                db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==edit_id).update({'Job_Title':edit_title,'Department':edit_depart,'Job_Location':edit_location,'Vacancies':edit_vacancy,'Experience':edit_experience,'Age':edit_age,'Salary_From':edit_from_salary,'Salary_To':edit_to_salary,'Job_Type':edit_type,'Current_Status':edit_status,'Start_Date':edit_start,'Expired_Date':edit_end_date,'JD':edit_jd})
                                db.commit()
                                return RedirectResponse(f'/HrmTool/Administration/job_details/{edit_id}',status_code=302)
                            else:
                                db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==edit_id).update({'Job_Title':edit_title,'Department':edit_depart,'Job_Location':edit_location,'Vacancies':edit_vacancy,'Experience':edit_experience,'Age':edit_age,'Salary_From':edit_from_salary,'Salary_To':edit_to_salary,'Job_Type':edit_type,'Current_Status':edit_status,'Start_Date':edit_start,'Expired_Date':edit_end_date,'JD':edit_jd})
                                db.commit()
                                return RedirectResponse('/HrmTool/Administration/manage_jobs',status_code=302)
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

@router.get('/job_details_id/{job_id}')
async def home(request:Request,job_id:int,db:Session=Depends(get_db)):
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
                            job_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==job_id).filter(models.Manage_Jobs.status=='ACTIVE').first()
                            department_data = db.query(models.Department).filter(models.Department.id==int(job_data.Department)).filter(models.Department.status=='ACTIVE').first()
                            response_data ={'department_data':jsonable_encoder(department_data),'job_data':jsonable_encoder(job_data)}
                            return JSONResponse(content=response_data,status_code=200)
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
   
@router.get('/del_job_details_id/{job_id}')
async def home(request:Request,job_id:int,db:Session=Depends(get_db)):
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
                            check_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==job_id).filter(models.Manage_Jobs.status=='ACTIVE').first()
                            if check_data:
                                db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==job_id).update({'status':'INACTIVE'})
                                db.commit()
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
  
@router.get('/change_job_type/{ids}/{info}')
async def home(request:Request,ids:int,info:str,db:Session=Depends(get_db)):
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
                            db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==ids).update({'Job_Type':info})
                            db.commit()
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
   
@router.get('/change_job_status/{ids}/{info}')
async def home(request:Request,ids:int,info:str,db:Session=Depends(get_db)):
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
                            db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==ids).update({'Current_Status':info})
                            db.commit()
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
   
#---------------------------------------------------------------------------------------------#
#---------------------------------- jobs  Applier portion ------------------------------------#
#---------------------------------------------------------------------------------------------#

@router.get('/job_lists')
async def home(request:Request,db:Session=Depends(get_db)):
    
    department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
    job_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.Current_Status=="Open",models.Manage_Jobs.status=='ACTIVE').all()

    return templates.TemplateResponse("Job_Applier/job_list.html",context={"request":request,"job_data":job_data})

@router.get('/job_views/{job_id_no}')
async def home(request:Request,job_id_no:int,db:Session=Depends(get_db)):
    
    department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
    job_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==job_id_no).filter(models.Manage_Jobs.Current_Status=="Open",models.Manage_Jobs.status=='ACTIVE').first()
    company_data = db.query(models.Company_Settings).filter(models.Company_Settings.status=='ACTIVE').first()
    return templates.TemplateResponse("Job_Applier/job_view.html",context={"request":request,"job_data":job_data,"department_data":department_data,"company_data":company_data,"job_id_no":job_id_no})

@router.get('/increase_viewers/{job_id_no}')
async def home(request:Request,job_id_no:int,db:Session=Depends(get_db)):
    
    check_viewrs_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==job_id_no).filter(models.Manage_Jobs.Current_Status=="Open",models.Manage_Jobs.status=='ACTIVE').first()
    if check_viewrs_data:
        count_of_views = int(check_viewrs_data.Viewers)+1
        db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==job_id_no).update({'Viewers':count_of_views})
        db.commit()
    
@router.post('/applier_data_store')
async def home(request:Request,db:Session=Depends(get_db),job_id:int=Form(...),applier_name:str=Form(...),applier_email:str=Form(...),applier_mesg:str=Form(...),cv_upload:UploadFile=File(...)):
    
    #here file name in unique type entered ...
    uniqueFileName = str(uuid.uuid4())+'.pdf'

    with open(f'./templates/assets/uploaded_files/Resumes/{uniqueFileName}', 'wb+') as file_object:
        shutil.copyfileobj(cv_upload.file,file_object)

    add_applier = models.Job_Appliers(Job_ID=job_id,Name=applier_name,Email=applier_email,Message=applier_mesg,Resume= uniqueFileName,Shortlist="No",status="ACTIVE",created_by=applier_name)
    db.add(add_applier)
    db.commit()
    db.refresh(add_applier)

    # after appliy increase a applier count 
    all_applier_data = len(db.query(models.Job_Appliers).filter(models.Job_Appliers.Job_ID == str(job_id)).filter(models.Job_Appliers.status=='ACTIVE').all())
    db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==job_id).update({'Applicants':all_applier_data})
    db.commit()
    ic(current_datetime)
    print(current_datetime)

    Job_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.id==int(job_id)).filter(models.Manage_Jobs.status=='ACTIVE').first()


    month = str(current_datetime) #2024-02-09 13:28:24.586655
    split_month = month.split('-')
    mon = split_month[1]
    ic(mon)
    ic(type(mon))

    ic(all_applier_data)

    def find_which_month():
        if mon =='01':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Jan':all_applier_data})
            db.commit()
        elif mon =='02':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Feb':all_applier_data})
            db.commit()
        elif mon =='03':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Mar':all_applier_data})
            db.commit()
        elif mon =='04':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Apr':all_applier_data})
            db.commit()
        elif mon =='05':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'May':all_applier_data})
            db.commit()
        elif mon =='06':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Jun':all_applier_data})
            db.commit()
        elif mon =='07':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Jul':all_applier_data})
            db.commit()
        elif mon =='08':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Aug':all_applier_data})
            db.commit()
        elif mon =='09':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Sep':all_applier_data})
            db.commit()
        elif mon =='10':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Oct':all_applier_data})
            db.commit()
        elif mon =='11':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Nov':all_applier_data})
            db.commit()
        elif mon =='12':
            db.query(models.Job_Graph).filter(models.Job_Graph.Department_id==Job_data.Department).update({'Dec':all_applier_data})
            db.commit()
        
    find_which_month()

    return RedirectResponse(f'/HrmTool/Administration/job_views/{job_id}',status_code=302)
  
#---------------------------------------------------------------------------------------------#
#------------------------------------------ manage resume ------------------------------------#
#---------------------------------------------------------------------------------------------#

@router.get('/manage_resume')
async def home(request:Request,db:Session=Depends(get_db)):
    ic(request)
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
                            
                            appliers_data = db.query(models.Job_Appliers).filter(models.Job_Appliers.status=='ACTIVE').all()
                            manage_job_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.status=='ACTIVE').all()
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()

                            random_photo = []
                            for i in range(len(appliers_data)):
                                all_p = random.randrange(1,8)
                                random_photo.append(all_p)

                            return templates.TemplateResponse("Admin/Administration/Jobs/manage-resumes.html",context={"request":request,'emp_data':emp_data,'appliers_data':appliers_data,"manage_job_data":manage_job_data,"department_data":department_data,"random_photo":random_photo})
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
   
@router.get('/get_applier_data/{applier_id}')
async def home(request:Request,applier_id:int,db:Session=Depends(get_db)):
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
                            print("here")
                            return 0
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
   
@router.get('/shortlist_applier/{applier_id_no}')
async def home(request:Request,applier_id_no:int,db:Session=Depends(get_db)):
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
                           
                           #update here a applier person as shortlist him\his
                           db.query(models.Job_Appliers).filter(models.Job_Appliers.id == applier_id_no).update({'Shortlist':'Yes'})
                           db.commit()
                           response_data = jsonable_encoder({'Done':'Done'})

                           #same time update her\him in schedule Timing table 
                           original_job_id = db.query(models.Job_Appliers).filter(models.Job_Appliers.id==applier_id_no).filter(models.Job_Appliers.status=='ACTIVE').first()

                           new_schedule = models.Schedule_Timing(Job_Appliers_ID=applier_id_no,Job_ID=original_job_id.Job_ID,Schedule_Date_1='',Schedule_Time_1='',Schedule_Date_2='',Schedule_Time_2='',Schedule_Date_3='',Schedule_Time_3='',status='ACTIVE',created_by=loginer_id)
                           db.add(new_schedule)
                           db.commit()
                           db.refresh(new_schedule)

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
   
#----------------------------------------------------------------------------------------------------#
#------------------------------------------ Short List Candiates ------------------------------------#
#----------------------------------------------------------------------------------------------------#
      
@router.get('/shortlisted_candidates')
async def home(request:Request,db:Session=Depends(get_db)):
    ic(request)
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
                            
                            appliers_data = db.query(models.Job_Appliers).filter(models.Job_Appliers.Shortlist=='Yes').filter(models.Job_Appliers.status=='ACTIVE').all()
                            manage_job_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.status=='ACTIVE').all()
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()

                            random_photo = []
                            for i in range(len(appliers_data)):
                                all_p = random.randrange(1,8)
                                random_photo.append(all_p)

                            return templates.TemplateResponse("Admin/Administration/Jobs/shortlist-candidates.html",context={"request":request,'emp_data':emp_data,'appliers_data':appliers_data,"manage_job_data":manage_job_data,"department_data":department_data,"random_photo":random_photo})
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
    
#----------------------------------------------------------------------------------------------#
#------------------------------------------ jobs dashboard ------------------------------------#
#----------------------------------------------------------------------------------------------#
       
@router.get('/jobs_dashboard')
async def home(request:Request,db:Session=Depends(get_db)):
    ic(request)
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
                            
                            appliers_data = db.query(models.Job_Appliers).filter(models.Job_Appliers.status=='ACTIVE').all()
                            manage_job_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.status=='ACTIVE').all()
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            employee_data = db.query(models.Employee).filter(models.Employee.status=='ACTIVE').all()

                            #====================>>>> Latest Jobs Portion

                            def lastest_jobs_all():
                                len_of_jobs = len(db.query(models.Manage_Jobs).filter(models.Manage_Jobs.status=='ACTIVE').all())
                                if len_of_jobs > 5:
                                    last_jobs = db.query(models.Manage_Jobs).from_statement(text(f"select * from manage_jobs order_by id DESC Limit 5 ")).all()
                                    return last_jobs
                                else:
                                    return db.query(models.Manage_Jobs).filter(models.Manage_Jobs.status=='ACTIVE').all()

                            random_photo = []
                            for i in range(len(appliers_data)):
                                all_p = random.randrange(1,8)
                                random_photo.append(all_p)

                            return templates.TemplateResponse("Admin/Administration/Jobs/jobs-dashboard.html",context={"request":request,'emp_data':emp_data,'appliers_data':appliers_data,"manage_job_data":manage_job_data,"department_data":department_data,"random_photo":random_photo,"employee_data":employee_data,"last_jobs":lastest_jobs_all()})
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
    
#---------------------------------------------------------------------------------------------------#
#-------------------------------- Interview questions  category ------------------------------------#
#---------------------------------------------------------------------------------------------------#
       
@router.post('/interview_question_category')
async def home(request:Request,db:Session=Depends(get_db),cat_name:str=Form(...)):
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
                            check_category_data = db.query(models.Question_Category).filter(models.Question_Category.Name == cat_name).filter(models.Question_Category.status=='ACTIVE').all()
                            if not check_category_data:
                                new_category_data = models.Question_Category(Name=cat_name,status='ACTIVE',created_by=loginer_id)                            
                                db.add(new_category_data)
                                db.commit()
                                db.refresh(new_category_data)
                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({'Result':'Error'})
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
         
#---------------------------------------------------------------------------------------------------#
#-------------------------------------------- Experience Level  ------------------------------------#
#---------------------------------------------------------------------------------------------------#
           
@router.get('/experience_level')
async def home(request:Request,db:Session=Depends(get_db)):
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
                            experience_data = db.query(models.Experience_Informations).filter(models.Experience_Informations.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Administration/Jobs/experiance-level.html",context={"request":request,'emp_data':emp_data,"experience_data":experience_data})
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
            
@router.post('/experience_level')
async def home(request:Request,db:Session=Depends(get_db),level:str=Form(...),current:str=Form(...)):
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
                            check_data = db.query(models.Experience_Informations).filter(models.Experience_Informations.Level_Range==level).filter(models.Experience_Informations.status=='ACTIVE').all()
                            if not check_data:
                                new_data = models.Experience_Informations(Level_Range=level,Current_Status=current,status='ACTIVE',created_by=loginer_id)
                                db.add(new_data)
                                db.commit()
                                db.refresh(new_data)
                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({'Result':'Error'})
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
            
@router.get('/experience_ids/{experience_id}')
async def experience_ids(request:Request,experience_id:int,db:Session=Depends(get_db)):
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
                            experience_data = db.query(models.Experience_Informations).filter(models.Experience_Informations.id==experience_id).filter(models.Experience_Informations.status=='ACTIVE').first()
                            response_data = jsonable_encoder({'Result':experience_data})
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
              
@router.post('/update_experience_level')
async def home(request:Request,db:Session=Depends(get_db),edit_id:int=Form(...),edit_level:str=Form(...),edit_current:str=Form(...)):
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
                            check_data = db.query(models.Experience_Informations).filter(models.Experience_Informations.id != edit_id,models.Experience_Informations.Level_Range == edit_level).filter(models.Experience_Informations.status=='ACTIVE').all()
                            if not check_data:
                                db.query(models.Experience_Informations).filter(models.Experience_Informations.id==edit_id).update({'Level_Range':edit_level,'Current_Status':edit_current})
                                db.commit()
                                response_data = jsonable_encoder({'Result':'Done'})
                                return JSONResponse(content=response_data,status_code=200)
                            else:
                                response_data = jsonable_encoder({'Result':'Error'})
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
           
@router.get('/delete_experience_level/{experience_id}')
async def experience_ids(request:Request,experience_id:int,db:Session=Depends(get_db)):
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
                            db.query(models.Experience_Informations).filter(models.Experience_Informations.id==experience_id).update({'status':'INACTIVE'})
                            db.commit()
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
    
#---------------------------------------------------------------------------------------------------#
#-------------------------------------------- schedule timing  -------------------------------------#
#---------------------------------------------------------------------------------------------------#  
             
@router.get('/schedule_timing')
async def schedule_timing(request:Request,db:Session=Depends(get_db)):
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

                            schedule_data = db.query(models.Schedule_Timing).filter(models.Schedule_Timing.status=='ACTIVE').all()
                            job_applier_data = db.query(models.Job_Appliers).filter(models.Job_Appliers.status=='ACTIVE').all()
                            manage_job_data = db.query(models.Manage_Jobs).filter(models.Manage_Jobs.status=='ACTIVE').all()
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()

                            random_photo = []
                            for i in range(len(job_applier_data)):
                                all_p = random.randrange(1,8)
                                random_photo.append(all_p)

                            return templates.TemplateResponse('Admin/Administration/Jobs/schedule-timing.html',context={'request':request,'emp_data':emp_data,"schedule_data":schedule_data,'job_applier_data':job_applier_data,"manage_job_data":manage_job_data,'random_photo':random_photo,"department_data":department_data})
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
               
@router.post('/schedule_timing')
async def home(request:Request,db:Session=Depends(get_db),schedule_id:int=Form(...),date_1:str=Form(...),date_2:str=Form(...),date_3:str=Form(...),time_1:str=Form(...),time_2:str=Form(...),time_3:str=Form(...)):
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
                            db.query(models.Schedule_Timing).filter(models.Schedule_Timing.id==schedule_id).update({'Schedule_Date_1':date_1,'Schedule_Time_1':time_1,'Schedule_Date_2':date_2,'Schedule_Time_2':time_2,'Schedule_Date_3':date_3,'Schedule_Time_3':time_3})
                            db.commit()
                            return RedirectResponse('/HrmTool/Administration/schedule_timing',status_code=302)
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
  