from fastapi import APIRouter
from resources.loginerController import router as loginRouter  
from resources.dashboard.admindashController import router as admindshRouter  
from resources.lockscreenController import router as lockscreenRouter  
from resources.registerController import router as registerRouter  
from resources.job_graphController import router as jobgraphRouter  
#---------------------->>>>>> Employee
from resources.Employee.clientController import router as clientRouter 
from resources.Employee.employeeController import router as employeeRouter 
from resources.Employee.taskboardController import router as taskboardRouter
from resources.Employee.departmentController import router as departmentRouter
from resources.Employee.projectController import router as projectRouter  
from resources.Employee.taskController import router as taskRouter  
from resources.Employee.designationController import router as designationRouter  
from resources.Employee.ticketsController import router as ticketRouter  
from resources.Employee.holidayController import router as holidayRouter  
from resources.Employee.leaveEmployeeController import router as leaveEmployeeRouter  
from resources.Employee.employeeprofileController import router as employeeprofileRouter  
#----------------------->>>>>> HR  
from resources.HR.budgetexpenseController import router as budgetexpenseRouter  
from resources.HR.budgetrevenueController import router as budgetrevenuesRouter  
from resources.HR.budgetController import router as budgetRouter  
from resources.HR.payrollitemsController import router as payrollitemsRouter  
from resources.HR.policisController import router as policiesRouter  
from resources.HR.providentfundController import router as providentFundRouter  
from resources.HR.invoicesController import router as invoicesRouter  
from resources.HR.employesalaryController import router as employeesalaryRouter  
from resources.HR.categoryController import router as categoryRouter  
from resources.HR.taxController import router as taxRouter  
#----------------------->>>>>> Administration  
from resources.administration.assetsController import router as assetsRouter  
from resources.administration.companysettingController import router as companysettingsRouter  
from resources.administration.leavetypeController import router as leavetypeRouter  
from resources.administration.localizationController import router as localizationRouter  
from resources.administration.cronsettingsController import router as cronsettingsRouter  
from resources.administration.toxboxController import router as toxboxsettingsRouter  
from resources.administration.interviewquestionController import router as interviewquestionsRouter  
from resources.administration.emailsettingsController import router as emailsettingsRouter  
from resources.administration.invoicesettingsController import router as invoicessettingsRouter  
from resources.administration.salarysettingController import router as salarysettingsRouter  
from resources.administration.jobsController import router as jobsRouter  
#----------------------->>>>>> Performance  
from resources.performance.trainersController import router as trainersRouter  
from resources.performance.resignationController import router as resignationRouter  
from resources.performance.goaltypeController import router as goaltypeRouter  
from resources.performance.promotionController import router as promotionRouter  
from resources.performance.terminationController import router as terminationRouter  
from resources.performance.performanceController import router as performanceRouter  

from fastapi.templating import Jinja2Templates

router = APIRouter()

router.include_router(loginRouter, prefix='/login', tags=['Login'])
router.include_router(admindshRouter, prefix='/Admin', tags=['Dashboard'])
router.include_router(lockscreenRouter, prefix='/Lock', tags=['Lock Screen'])
router.include_router(registerRouter, prefix='/Register', tags=['Register'])
router.include_router(jobgraphRouter, prefix='/Job', tags=['Job Dashboard'])
#---------------------->>>>>> Employee
router.include_router(clientRouter, prefix='/Client', tags=['Client'])
router.include_router(employeeRouter, prefix='/Employee', tags=['Employee'])
router.include_router(taskboardRouter, prefix='/Employee', tags=['Task Board'])
router.include_router(departmentRouter, prefix='/Employee', tags=['Department'])
router.include_router(projectRouter, prefix='/Employee', tags=['Project'])
router.include_router(taskRouter, prefix='/Employee', tags=['Task'])
router.include_router(designationRouter, prefix='/Employee', tags=['Designation'])
router.include_router(ticketRouter, prefix='/Employee', tags=['Tickets'])
router.include_router(holidayRouter, prefix='/Employee', tags=['Holidays'])
router.include_router(leaveEmployeeRouter, prefix='/Employee', tags=['Leave Employee'])
router.include_router(employeeprofileRouter, prefix='/Employee', tags=['Employee Profile'])
#------------------------------>>>> HR 
router.include_router(payrollitemsRouter, prefix='/PayrollItems', tags=['PayrollItems'])
router.include_router(policiesRouter, prefix='/HR', tags=['Policies'])
router.include_router(providentFundRouter, prefix='/HR', tags=['Provident Fund'])
router.include_router(invoicesRouter, prefix='/HR', tags=['Invocies'])
router.include_router(employeesalaryRouter, prefix='/HR', tags=['Employee Salary'])
router.include_router(categoryRouter, prefix='/HR', tags=['Category'])
router.include_router(budgetexpenseRouter, prefix='/HR', tags=['Budget Expense'])
router.include_router(budgetrevenuesRouter, prefix='/HR', tags=['Budget Revenue'])
router.include_router(budgetRouter, prefix='/HR', tags=['Budget'])
router.include_router(taxRouter, prefix='/HR', tags=['Tax'])

#------------------------------>>>> Administration 
router.include_router(assetsRouter, prefix='/Administration', tags=['Administration'])
router.include_router(companysettingsRouter, prefix='/Administration', tags=['Company Settings'])
router.include_router(leavetypeRouter, prefix='/Administration', tags=['Leave Type'])
router.include_router(localizationRouter, prefix='/Administration', tags=['Localization'])
router.include_router(cronsettingsRouter, prefix='/Administration', tags=['Cron Settings'])
router.include_router(toxboxsettingsRouter, prefix='/Administration', tags=['Tox Box'])
router.include_router(interviewquestionsRouter, prefix='/Administration', tags=['Interview Questions'])
router.include_router(emailsettingsRouter, prefix='/Administration', tags=['E mail'])
router.include_router(invoicessettingsRouter, prefix='/Administration', tags=['Invoices Settings'])
router.include_router(salarysettingsRouter, prefix='/Administration', tags=['Salary Settings'])
router.include_router(jobsRouter, prefix='/Administration', tags=['Jobs'])
#----------------------->>>>>> Performance  
router.include_router(trainersRouter, prefix='/Performance', tags=['Trainers'])
router.include_router(resignationRouter, prefix='/Performance', tags=['Resignation'])
router.include_router(goaltypeRouter, prefix='/Performance', tags=['Goaltype'])
router.include_router(promotionRouter, prefix='/Performance', tags=['Promotion'])
router.include_router(terminationRouter, prefix='/termination', tags=['Termination'])
router.include_router(performanceRouter, prefix='/Performance', tags=['Performance Indicator'])


templates = Jinja2Templates(directory="templates")
