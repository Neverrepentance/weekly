import json,os
from requests_html import HTMLSession

class JiraTask:
    userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67"
    header={
        "Refer":"http://www.jr.com/issues/?filter=18000",
        "User-Agent":userAgent,
    }

    bugList=[]
    
    def __init__(self) -> None:
        self.session = HTMLSession()

    def Login(self):
        print("登录Jira")
        loginUrl="http://www.jr.com/login.jsp"

        
        current_path=os.path.split(os.path.realpath(__file__))[0]
        with open(os.path.join(current_path, 'config/jira_account.json')) as f:
            myconfig=json.load(f)

            postData={
                "os_username":myconfig["username"],
                "os_password":myconfig["password"],
                "os_cookie":"true",
                "login":"登录"
            }
        res = self.session.post(loginUrl,data=postData,headers=self.header)
        ret = res.html.xpath('//*[@id="header-details-user-fullname"]')
        if ret is None :
            print("登录失败")
        else:
            displayName = ret[0].attrs["data-displayname"]
            print(f"{displayName} 登录成功!")


    def GetBugInfo(self):
        print("查询Bug单")

        queryUrl="http://www.jr.com/secure/QueryComponent!Jql.jspa"
        tableUrl = "http://www.jr.com/rest/issueNav/1/issueTable"

        project="AUDIT"
        issuetype="故障"
        status="创建, 分析, 提交, 修改评审, 转后续版本处理"
        proVersion="DSA_V3.2.2_CH3C000_R800*"
        members="zhangzhen, nijiahe, honglidong, languoquan, caopo, caichengjie, qianwei, lileping, currentUser()"

        jqlStr= 'project = "{0}" AND issuetype = {1} AND status in ({2}) AND 发现版本-TY ~ "{3}" AND assignee in ({4})'.format(project, issuetype, status, proVersion, members)

        queryData={
            "jql":r'project+=+"AUDIT"+AND+issuetype+=+故障+AND+status+in+(创建,+分析,+提交,+修改评审,+转后续版本处理)+AND+发现版本-TY+~+"DSA_V3.2.2_CH3C000_R800*"+AND+assignee+in+(zhangzhen,+nijiahe,+honglidong,+languoquan,+caopo,+yangmingke,+caichengjie,+lileping,+qianwei,+currentUser())+ORDER+BY+updated+DESC',
            "decorator":"none"
        }

        tableData={
            "startIndex":0,
            "filterId":18000,
            "jql":jqlStr,
            "layoutKey":"list-view"
        }

        res = self.session.post(queryUrl, data=queryData,headers=self.header)
        print(f"status:{res.status_code}")

        res = self.session.post(tableUrl, data=tableData,headers=self.header)
        print(f"status:{res.status_code}")

        ret = json.load(res.html.text)
        print("issues count:%d"% int(ret["issueTable"]["total"]))

    def FormatPrint(self):
        print("格式化输出")
