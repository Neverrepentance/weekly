# coding=utf-8

from task_jira2 import JiraTask
from sendmail import Sender


def main():
        # task=JiraTask()
        # task.Login()
        # task.GetBugInfo()

        send = Sender()
        send.SendMail()

if __name__ == "__main__":
    main()