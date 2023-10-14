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

        project = "AUDIT"
        issuetype = "故障"
        status_hang = "创建, 分析, 提交, 修改评审, 转后续版本处理"
        status_done = "通过, 回归"
        members="zhangzhen, nijiahe, honglidong, languoquan, yangmingke, caopo, caichengjie, qianwei, lileping, currentUser()"
        createData="-1w"
        
        proVersions=[
            {
            "name":"P04",
            "key":"DSA_V3.2.2_CH3C000_R800*",
            },
            {
            "name":"P03",
            "key":"DSA_V3.2.2_CH3C000_R700*",
            },
            {
            "name":"主线",
            "key":"V3.2.3_R500*",
            },
            {
            "name":"JD",
            "key":"V3.2.3_R300*",
            },
        ]

        for versions in proVersions:
            proKey = versions["key"]
            proName = versions["name"]
            print(f"版本 {proName} 统计：")
            befor1w= 'project = "{0}" AND issuetype = {1} AND status in ({2}) AND 发现版本-TY ~ "{3}" AND assignee in ({4}) AND created < {5}' \
                .format(project, issuetype, status_hang,  proKey, members, createData)
            
            new1w = 'project = "{0}" AND issuetype = {1} AND status in ({2}) AND 发现版本-TY ~ "{3}" AND assignee in ({4}) AND created >= {5}' \
                .format(project, issuetype, status_hang,  proKey, members, createData)

            issues = self.jira.search_issues(befor1w)
            befor_count = len(issues)

            issues = self.jira.search_issues(new1w)
            new_count = len(issues)

            befor1w_done = 'project = "{0}" AND issuetype = {1} AND status in ({2}) AND 发现版本-TY ~ "{3}" AND 修改人员 in ({4}) AND created < {5} AND updated >-1w' \
                .format(project, issuetype, status_done,  proKey, members, createData)
            issues = self.jira.search_issues(befor1w_done)
            befor_done_count = len(issues)
            
            new1w_done= 'project = "{0}" AND issuetype = {1} AND status in ({2}) AND 发现版本-TY ~ "{3}" AND 修改人员 in ({4}) AND created >= {5} AND updated >-1w' \
                .format(project, issuetype, status_done,  proKey, members, createData)
            issues = self.jira.search_issues(new1w_done)
            new_done_count = len(issues)

            current_path=os.path.split(os.path.realpath(__file__))[0]
            with open(os.path.join(current_path, f"output/{proName}.csv"), "w+") as f:
                f.write(f"{proName}, 历史遗留, 本周新增, 合计\n")
                f.write(f"未完成, {befor_count}, {new_count}, {befor_count + new_count}\n")
                f.write(f"本周完成, {befor_done_count}, {new_done_count}, {befor_done_count + new_done_count}\n")
                f.write(f"合计, {befor_count + befor_done_count}, {new_count + new_done_count}\n")


            print(f"历史遗留：{befor_count + befor_done_count}, 本周完成：{befor_done_count}, 未完成:{befor_count}")
            print(f"本周新增:{new_count + new_done_count}, 本周完成{new_done_count}, 未完成{new_count}")
            print(f"本周完成总数{new_done_count + befor_done_count}, 未完成总数{befor_count + new_count}")

    def FormatPrint(self):
        print("格式化输出")
