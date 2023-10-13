import requests,json,os

class JiraTask:
    userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67"
    header={
        "Refer":"http://www.jr.com/login.jsp",
        "User-Agent":userAgent,
    }
    def __init__(self) -> None:
        pass

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
        print(postData)
        res=requests.post(loginUrl,data=postData,headers=self.header)
        print(f"status = {res.status_code}")