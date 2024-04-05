from typing import Dict, List,Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Depends, FastAPI, Request, Form,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.encoders import jsonable_encoder
# from models.schemas import masterSchemas
import base64,json
import shutil,uuid
from configs.base_config import BaseConfig
from jose import jwt, JWTError
# from django.contrib import messages
from datetime import datetime 
from models import get_db, models
from sqlalchemy.orm import Session
from sqlalchemy import text,func,update

router = APIRouter()

templates = Jinja2Templates(directory="templates")

current_datetime = datetime.today()

#                                 *********** A S S E S T S ***********

@router.get("/salary_settings")
async def getting(request:Request,db:Session = Depends(get_db)):
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
                            da=db.query(models.Salary_Settings).filter(models.Salary_Settings.status=="ACTIVE").first()
                            anual=db.query(models.TDS_Data).filter(models.TDS_Data.status=="ACTIVE").all()
                            return templates.TemplateResponse("Admin/Administration/Settings/salary-settings.html",context={"request":request,'emp_data':emp_data,"da":da,"anual":anual})
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
    
@router.post("/salary_settings")
async def posting(request:Request,db:Session = Depends(get_db),da:int=Form(...),hra:int=Form(...),peshare:int=Form(...),poshare:int=Form(...),eeshare:int=Form(...),eoshare:int=Form(...),sfrom:List[int]=Form(...),sto:List[int]=Form(...),tdsp:List[int]=Form(...),edit_ids:Optional[str]=Form(None),
                  dh_button:str=Form(...),fund_button:str=Form(...),esi_button:str=Form(...),tds_button:str=Form(...)):
    
    try:
        if 'loginer_details' in request.session:
            token = request.session['loginer_details']
            try:
                payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
                loginer_id : int= payload.get("empid") 
                # try:
                print(sfrom)
                print(edit_ids)
                if loginer_id:
                    emp_data = db.query(models.Employee).filter(models.Employee.id==loginer_id).filter(models.Employee.status=='ACTIVE').first()
                    if emp_data.Lock_screen == 'OFF':
                        find=db.query(models.Salary_Settings).filter(models.Salary_Settings.status=="Active").all()
                        if find == []:
                            print(sfrom)
                            body1=models.Salary_Settings(DA=da,HRA=hra,DA_HRA_Switch=dh_button,Employee_Share=peshare,Organization_Share=poshare,Fund_Settings_switch=fund_button,Employee_ESI=eeshare,Organization_ESI=eoshare,ESI_Switch=esi_button,status="ACTIVE",created_by=loginer_id)    
                            db.add(body1)
                            db.commit()

                            for i,j,k in zip (sfrom,sto,tdsp):
                                tds_data=models.TDS_Data(Salary_Settings_id=body1.id,TDS_Switch=tds_button,Salary_From=i,Salary_To=j,Percentage=k,status="ACTIVE",created_by=loginer_id)    
                                db.add(tds_data)
                                db.commit()
                            
                            return RedirectResponse("/HrmTool/Administration/salary_settings",status_code=302)
                        else:
                            body1=db.query(models.Salary_Settings).update({"DA":da,"HRA":hra,"DA_HRA_Switch":dh_button,"Employee_Share":peshare,"Organization_Share":poshare,"Fund_Settings_switch":fund_button,"Employee_ESI":eeshare,"Organization_ESI":eoshare,"ESI_Switch":esi_button,"created_by":loginer_id})
                            db.commit()
                            #------------->>>> loop the tds data 
                            tds_data = db.query(models.TDS_Data).filter(models.TDS_Data.status=='ACTIVE').all()
                            len_db_tds = len(tds_data)
                            len_tds = len(sfrom)
                            if len_db_tds < len_tds:
                                for sf,st,per in zip(sfrom[len_db_tds::],sto[len_db_tds::],tdsp[len_db_tds::]):
                                    extra_tds_data = models.TDS_Data(Salary_Settings_id=1,TDS_Switch=tds_button,Salary_From=sf,Salary_To=st,Percentage=per,status="ACTIVE",created_by=loginer_id)
                                    db.add(extra_tds_data)
                                    db.commit()
                                    db.refresh(extra_tds_data)
                                for i,esf,est,eper in zip(edit_ids,sfrom[:len_db_tds:],sto[:len_db_tds:],tdsp[:len_db_tds:]):
                                    db.query(models.TDS_Data).filter(models.TDS_Data.id==i).update({'Salary_From':esf,'Salary_To':est,'Percentage':eper,'created_by':loginer_id})
                                    db.commit()
                            else:
                                for i,esf,est,eper in zip(edit_ids,sfrom,sto,tdsp):
                                    db.query(models.TDS_Data).filter(models.TDS_Data.id==int(i)).update({'Salary_From':esf,'Salary_To':est,'Percentage':eper,'created_by':loginer_id})
                                    db.commit()
                                
                            return RedirectResponse("/HrmTool/Administration/salary_settings",status_code=303)
                    else:
                        return RedirectResponse('/HrmTool/Lock/lockscreen',status_code=302)
                else:
                    return RedirectResponse('/HrmTool/login/login',status_code=302)
                # except:
                #     return RedirectResponse('/HrmTool/login/login',status_code=302)
            except JWTError:
                return RedirectResponse('/HrmTool/login/login',status_code=302)
        else:
            return RedirectResponse('/HrmTool/login/login',status_code=303)
    except JWTError:
            return RedirectResponse('/HrmTool/login/login',status_code=302)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"}) 
    
