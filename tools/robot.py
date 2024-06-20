import requests
import json
from tools.tool_http import http


class FeiShu():

    def __init__(self, webhook="https://open.feishu.cn/open-apis/bot/v2/hook/ff901dcc-4772-4fc6-b98a-f74fcb7cad3b"):
        self.webhook = webhook

    def header(self, title="提醒", color="blue"):
        return {
            "template": color,
            "title": {
                "content": title,
                "tag": "plain_text"
            }
        }

    def element(self, tag="div", fileds=None):
        """
        div---标签
        hr---分隔符
        action---活动
        note---备注
        """
        return {"tag": "hr"} if tag == "hr" else {"tag": tag, "fields": fileds}

    def fileds(self, content, is_short=True):
        # div使用
        return {"is_short": is_short, "text": {"content": content, "tag": "lark_md"}}

    def action(self, url, content, tag="button", type="primary"):
        # action使用
        return {"tag": tag, "text": {"content": content, "tag": "plain_text"}, "url": url, "type": type}

    def note(self, content):
        # note使用
        return {"content": content, "tag": "lark_md"}

    def send(self, header, elements):
        obj = {"msg_type": "interactive", "card": {
            "header": header, "elements": elements}}
        return requests.post(url=self.webhook, data=json.dumps(obj), headers={"Content-Type": "application/json"}).text


# if __name__ == '__main__':
#     feishu = FeiShu("https://open.feishu.cn/open-apis/bot/v2/hook/47bec932-07a6-4609-ac41-57ecca09bbcb")
#     fileds=[]
#     elements=[]
#     fileds.append(feishu.fileds("ok"))
#     fileds.append(feishu.fileds("ok1"))
#     print(feishu.element(fileds))
#     elements.append(feishu.element(fileds))
#     print(elements)
#     feishu.send(feishu.header("ok"),elements)
