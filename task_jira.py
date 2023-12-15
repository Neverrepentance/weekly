from jira import JIRA
import json,os

class JiraTask:

    bugList=[]
    jira = None
    
    def __init__(self) -> None:
        pass

    def Login(self):
        print("登录Jira")

        current_path=os.path.split(os.path.realpath(__file__))[0]
        with open(os.path.join(current_path, 'config/jira_account.json')) as f:
            myconfig=json.load(f)

        self.jira = JIRA(basic_auth=(myconfig["username"],myconfig["password"]), options={"server":"http://www.jr.com"})
        if self.jira is None :
            print("登录失败")
        else:
            print("登录成功")


    def GetBugInfo(self):
        print("查询Bug单")

        iss = self.jira.issue(id="AUDIT-8544")
        print(iss.fields.labels)
        if '语法解析' in iss.fields.labels:
            print("语法解析")
        elif '协议解析' in iss.fields.labels:
            print("协议解析")
        else:
            print("c++")

    def FormatPrint(self):
        print("格式化输出")
