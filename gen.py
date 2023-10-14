# coding=utf-8

from task_jira2 import JiraTask


def main():
        task=JiraTask()
        task.Login()
        task.GetBugInfo()

if __name__ == "__main__":
    main()