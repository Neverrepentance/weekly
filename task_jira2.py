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
        members="zhangzhen, nijiahe, honglidong, caopo, caoxu, qianwei,zhangchuangang, yangmingke, caichengjie, lileping, sunzhihong, liuhao"
        members_protocol = "yangmingke,caichengjie,lileping,xunzhihong"
        members_parse = "caopo,qianwei,caoxu,sunchuangang"
        createData="-1w"
        
        proVersions=[
            {
            "name":"P04",
            "key":"DSA_V3.2.2_CH3C000_R800*",
            },
            {
            "name":"多租户",
            "key":"V3.2.5_R001*",
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
        
        current_path=os.path.split(os.path.realpath(__file__))[0]
        with open(os.path.join(current_path, f"output/weekly.csv"), "w+") as f:
            f.write(f"项目, 事项, 说明\n")
            for versions in proVersions:
                proKey = versions["key"]
                proName = versions["name"]
                print(f"\n版本 {proName} 统计：")
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

                # current_path=os.path.split(os.path.realpath(__file__))[0]
                # with open(os.path.join(current_path, f"output/{proName}.csv"), "w+") as f:
                #     f.write(f"{proName}, 历史遗留, 本周新增, 合计\n")
                #     f.write(f"未完成, {befor_count}, {new_count}, {befor_count + new_count}\n")
                #     f.write(f"本周完成, {befor_done_count}, {new_done_count}, {befor_done_count + new_done_count}\n")
                #     f.write(f"合计, {befor_count + befor_done_count}, {new_count + new_done_count}\n")


                print(f"    历史遗留：{befor_count + befor_done_count}, 本周完成：{befor_done_count}, 未完成:{befor_count}")
                print(f"    本周新增:{new_count + new_done_count}, 本周完成{new_done_count}, 未完成{new_count}")
                print(f"    本周完成总数{new_done_count + befor_done_count}, 未完成总数{befor_count + new_count}")
                f.write(f"{proName},bugfix,\"")
                f.write(f"历史遗留：{befor_count + befor_done_count}, 本周完成：{befor_done_count}, 未完成:{befor_count}\n")
                f.write(f"本周新增:{new_count + new_done_count}, 本周完成{new_done_count}, 未完成{new_count}\n")
                f.write(f"本周完成总数{new_done_count + befor_done_count}, 未完成总数{befor_count + new_count}")
                f.write(f"\"\n")

                product_count = 0
                product_count_new = 0
                product_str = ""
                protocol_count = 0
                protocol_count_new = 0
                protocol_str = ""
                grammar_count = 0
                grammar_count_new = 0
                grammar_str = ""

                next_version = 'project = "{0}" AND issuetype = {1} AND status in (转后续版本处理) AND 发现版本-TY ~ "{2}" AND assignee in ({3})' \
                    .format(project, issuetype, proKey, members)
                issues = self.jira.search_issues(next_version)
                next_count = len(issues)
                for iss in issues:
                    if '语法解析' in iss.fields.labels:
                        grammar_count = grammar_count + 1
                        grammar_str = grammar_str + iss.key + ','
                    elif '协议解析' in iss.fields.labels:
                        protocol_count = protocol_count + 1
                        protocol_str = protocol_str + iss.key + ','
                    else:
                        product_count = product_count + 1
                        product_str = product_str + iss.key + ','
                
                next_version_new = 'project = "{0}" AND issuetype = {1} AND status in (转后续版本处理) AND 发现版本-TY ~ "{2}" AND assignee in ({3}) AND updated >= -1w' \
                    .format(project, issuetype, proKey, members)
                issues_new = self.jira.search_issues(next_version_new)
                for iss in issues_new:
                    if '语法解析' in iss.fields.labels:
                        grammar_count_new = grammar_count_new + 1
                    elif '协议解析' in iss.fields.labels:
                        protocol_count_new = protocol_count_new + 1
                    else:
                        product_count_new = product_count_new + 1
                
                befor1w_undo= 'project = "{0}" AND issuetype = {1} AND status in (创建, 分析, 提交) AND 发现版本-TY ~ "{2}" AND assignee in ({3}) AND created < {4}' \
                    .format(project, issuetype, proKey, members, createData)
                issues = self.jira.search_issues(befor1w_undo)
                befor1w_undo_count = len(issues)
                for iss in issues:
                    if '语法解析' in iss.fields.labels:
                        grammar_count = grammar_count + 1
                        grammar_str = grammar_str + iss.key + ','
                    elif '协议解析' in iss.fields.labels:
                        protocol_count = protocol_count + 1
                        protocol_str = protocol_str + iss.key + ','
                    else:
                        product_count = product_count + 1
                        product_str = product_str + iss.key + ','
                
                befor1w_undo_new= 'project = "{0}" AND issuetype = {1} AND status in (创建, 分析, 提交) AND 发现版本-TY ~ "{2}" AND assignee in ({3}) AND created >=-2w AND created < {4}' \
                    .format(project, issuetype, proKey, members, createData)
                issues_new = self.jira.search_issues(befor1w_undo_new)
                for iss in issues_new:
                    if '语法解析' in iss.fields.labels:
                        grammar_count_new = grammar_count_new + 1
                    elif '协议解析' in iss.fields.labels:
                        protocol_count_new = protocol_count_new + 1
                    else:
                        product_count_new = product_count_new + 1

                print("风险：")                
                f.write(f"{proName},风险,\"")
                new_line =False
                if next_count > 0 :
                    print(f"    {next_count} 个问题单遗留到下个版本")
                    f.write(f"{next_count} 个问题单遗留到下个版本")
                    new_line = True
                if befor1w_undo_count > 0 :
                    print(f"    {befor1w_undo_count}个问题单超过1周未处理")
                    if new_line :
                        f.write(f"\n")
                    f.write(f"{befor1w_undo_count}个问题单超过1周未处理")
                f.write(f"\"")
                if product_count > 0 or protocol_count > 0 or grammar_count > 0:
                    f.write(f",\"")
                    new_line = False
                    if product_count > 0:
                        f.write(f"c++ {product_count}个，新增{product_count_new}个")  
                        print(f"产品端：{product_str}") 
                        new_line = True
                    if protocol_count > 0:
                        if new_line:
                            f.write('\n')
                        f.write(f"协议解析{protocol_count}个，新增{protocol_count_new}个")  
                        print(f"协议解析：{protocol_str}") 
                        new_line = True  
                    if grammar_count > 0:
                        if new_line:
                            f.write('\n')
                        f.write(f"语法解析{grammar_count}个，新增{grammar_count_new}个") 
                        print(f"语法解析：{grammar_str}")
                    f.write(f"\"")
                f.write(f"\n")
                

            print(f"\n线上问题 统计：")
            issuetype = "任务,故事"
            status_hang = "主管审核, 问题分析, 问题修改"
            status_done = "回归完成"
            task_befor1w_undo= 'project = "{0}" AND issuetype in ({1}) AND status in ({2}) AND Sprint = 432  AND created < {3}' \
                .format(project, issuetype, status_hang, createData)
            
            task_new1w = 'project = "{0}" AND issuetype in ({1}) AND status in ({2}) AND Sprint = 432  AND created >= {3}' \
                .format(project, issuetype, status_hang, createData)

            issues = self.jira.search_issues(task_befor1w_undo)
            task_befor_count = len(issues)

            issues = self.jira.search_issues(task_new1w)
            task_new_count = len(issues)

            task_befor1w_done = 'project = "{0}" AND issuetype in ({1}) AND status in ({2}) AND Sprint = 432  AND created < {3}' \
                .format(project, issuetype, status_done, createData)
            issues = self.jira.search_issues(task_befor1w_done)
            task_befor_done_count = len(issues)
            
            task_new1w_done= 'project = "{0}" AND issuetype in ({1}) AND status in ({2}) AND Sprint = 432  AND created >= {3}' \
                .format(project, issuetype, status_done, createData)
            issues = self.jira.search_issues(task_new1w_done)
            task_new_done_count = len(issues)

            print(f"    历史遗留：{task_befor_count + task_befor_done_count}, 本周完成：{task_befor_done_count}, 未完成:{task_befor_count}")
            print(f"    本周新增:{task_new_count + task_new_done_count}, 本周完成{task_new_done_count}, 未完成{task_new_count}")
            print(f"    本周完成总数{task_new_done_count + task_befor_done_count}, 未完成总数{task_befor_count + task_new_count}")
            f.write(f"线上问题,bugfix,\"")
            f.write(f"历史遗留：{task_befor_count + task_befor_done_count}, 本周完成：{task_befor_done_count}, 未完成:{task_befor_count}\n")
            f.write(f"本周新增:{task_new_count + task_new_done_count}, 本周完成{task_new_done_count}, 未完成{task_new_count}\n")
            f.write(f"本周完成总数{task_new_done_count + task_befor_done_count}, 未完成总数{task_befor_count + task_new_count}")
            f.write(f"\"\n")
            print("风险：")                
            f.write(f"线上问题,风险,\"")
            task_timeout= 'project = "{0}" AND issuetype = {1} AND Sprint = 432 AND status in ({2}) AND due < now()' \
                .format(project, issuetype, status_hang)
            issues = self.jira.search_issues(task_timeout)
            task_timeout_count = len(issues)
            timeout_list = ""
            new_line = False
            if task_timeout_count > 0:
                print(f"{task_timeout_count}个问题逾期未解决")
                f.write(f"{task_timeout_count}个问题逾期未解决")
                new_line = True
                for iss in issues:
                    timeout_list =  '\n' + timeout_list + iss.fields.summary

            task_timeout1w= 'project = "{0}" AND issuetype = {1} AND Sprint = 432 AND status in ({2}) AND due > now() AND due < {3}' \
                .format(project, issuetype, status_hang, "1w")
            issues = self.jira.search_issues(task_timeout1w)
            task_timeout1w_count = len(issues)
            timeout1w_list = ""
            if task_timeout1w_count > 0:
                print(f"{task_timeout1w_count}个问题下周到期")
                if new_line:
                    f.write("\n")
                f.write(f"{task_timeout1w_count}个问题下周到期")
                for iss in issues:
                    timeout1w_list = '\n' + timeout1w_list + iss.fields.summary 
            f.write(f"\",\"")
            if task_timeout_count > 0:
                f.write(f"逾期：")
                f.write(f"{timeout_list}")
            if task_timeout1w_count > 0:
                f.write(f"下周到期:")
                f.write(f"{timeout1w_list}")
            f.write(f"\"")

    def FormatPrint(self):
        print("格式化输出")
