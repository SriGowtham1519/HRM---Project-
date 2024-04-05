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


#                                 *********** A S S E S T S ***********

@router.get('/interview') 
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
                            add_ques = db.query(models.Interview_Questions).filter(models.Interview_Questions.status=='ACTIVE').all()
                            category_data = db.query(models.Question_Category).filter(models.Question_Category.status=='ACTIVE').all()
                            department_data = db.query(models.Department).filter(models.Department.status=='ACTIVE').all()
                            return templates.TemplateResponse("Admin/Administration/Jobs/interview-questions.html",context={"request":request,'emp_data':emp_data,"add_ques":add_ques,"category_data":category_data,"department_data":department_data})
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
    
@router.post("/ques_add")
def ques_add(request: Request, db: Session = Depends(get_db),
                 add_category: str = Form(...),
                 department: str = Form(...),
                 add_question: str = Form(...),
                 option_a: str = Form(...),
                 option_b: str = Form(...),
                 option_c: str = Form(...),
                 option_d: str = Form(...),
                 cor_ans: str = Form(...),
                 code_snippets: str = Form(...),
                 ans_exp: str = Form(...),
                 vdo_link: str = Form(...),
                 add_image: UploadFile = File(...)):
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

                            image_name = str(uuid.uuid4())+'.png'
                            with open (f'./templates/assets/uploaded_files/{image_name}' ,"wb+") as file_object:
                                shutil.copyfileobj(add_image.file , file_object)

                            body = models.Interview_Questions(Category_ID = add_category,Department_ID = department,Question = add_question,OPtion_A = option_a,OPtion_B = option_b,OPtion_C = option_c,OPtion_D = option_d,Correct_Answer = cor_ans,Code_Snippets = code_snippets,Answer_Explanation = ans_exp,Video_Link = vdo_link,Image = image_name,status='ACTIVE',created_by=loginer_id)
                            db.add(body)
                            db.commit()
                            return RedirectResponse("/HrmTool/Administration/interview", status_code=303)  
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
    
@router.get('/ques_add') 
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
                            return templates.TemplateResponse("interview.html",context={"request":request}) 
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
    
@router.get("/taking_edit_modal/{ids}")       
def taking_edit_modal(ids:int,request:Request,db: Session = Depends(get_db)):
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
                            single_data = db.query(models.Interview_Questions).filter(models.Interview_Questions.id==ids).first()
                            return single_data
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
    
@router.post('/question_edit')
def create_data(request: Request, db: Session = Depends(get_db),  edit_id: str= Form(...),edit_category: str =Form(...), edit_department: str = Form(...),edit_question: str = Form(...) , edit_a: str = Form(...), edit_b: str = Form(...), edit_c: str = Form(...),edit_d: str=Form(...),edit_ans: str=Form(...),edit_snippets: str=Form(...),edit_exp: str=Form(...),edit_link: str=Form(...),edit_image: str=Form(...)):
    # Correct_Answer  = Column(String(255), nullable=False, index=True)
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
                            db.query(models.Interview_Questions).filter(models.Interview_Questions.id==edit_id).update({"Category_ID": edit_category, "Department_ID": edit_department, "Question": edit_question, "OPtion_A": edit_a, "OPtion_B": edit_b, "OPtion_C": edit_c,"OPtion_D":edit_d,"Correct_Answer":edit_ans ,"Code_Snippets":edit_snippets ,"Answer_Explanation":edit_exp ,"Video_Link":edit_link,"Image":edit_image })
                            db.commit()
                            return RedirectResponse("/interview", status_code=303)   
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
    
@router.get("/delete_question/{ids}")
def taking_dlt_id(request: Request,ids:int,db: Session = Depends(get_db)):
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
                            db.query(models.Interview_Questions).filter(models.Interview_Questions.id== ids).delete()
                            db.commit()
                            return templates.TemplateResponse("interview.html",context={"request":request})
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
    
@router.get('/add_categry') 
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
                            add_name = db.query(models.Question_Category).all()
                            return templates.TemplateResponse("interview.html",context={"request":request,"add_name":add_name})
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