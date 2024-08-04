# aifox操作类

import time
import json
import uuid
import inspect
import requests
from urllib.parse import quote


class Apifox:
    def __init__(self, project,team="", token="", phone="", password=""):
        """apifox初始化函数,用户ID与用户token为一对,phone与password为一对,两者二选一,推荐使用第一种方式,使用手机号登录后会返回用户ID和token,建议保存下来下次登录使用

        Args:
            project (str): 项目,可以填项目ID或项目名称,为名称时,项目不存在会自动创建.
            team (str): 项目,可以填项目ID或项目名称,为名称时,项目不存在会自动创建.
            user_id (str, optional): 用户ID. Defaults to "".
            token (str, optional): 用户token. Defaults to "".
            phone (str, optional): 手机号. Defaults to "".
            password (str, optional): 密码. Defaults to "".
        """

        self.project_id = ""
        if token:
            self.headers = {"Host": "api.apifox.com","x-client-version":"2.6.8-alpha.1"}
            self.headers["Authorization"] = token
            success, data = self.set_project_id(project,team)
            if not success:
                raise Exception(f"设置项目失败,{data}")
            self.create_var()
            return
        if phone and password:
            if not self.login(phone, password):
                raise Exception("登录失败")
            success, data = self.set_project_id(project,team)
            if not success:
                raise Exception(f"设置项目失败,{data}")
            self.create_var()
            return
        raise Exception("请输入用户ID或手机号")

    def __request(self, url, json=None, data=None, method=None):
        if not method:
            method = "GET" if not json and not data else "POST"
        if data:
            self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        elif json:
            self.headers["Content-Type"] = "application/json"
        else:
            try:
                del self.headers["Content-Type"]
            except Exception:
                pass
        response = requests.request(
            url=url, method=method, headers=self.headers, json=json, data=data
        )
        if response.status_code != 200:
            print("请求失败", response.json()["errorMessage"])
            return False, response.json()["errorMessage"]
        return True, response.json()["data"]

    def login(self, phone, password):
        """登录apifox

        Args:
            phone (_type_): 手机号
            password (_type_): 密码

        Returns:
            _type_: 成功返回true,并获取userId和assessToken,失败返回false并打印错误
        """
        url = "https://api.apifox.com/api/v1/login?locale=zh-CN"
        json = {
            "mobile": f"+86 {phone}",
            "password": password,
            "account": f"+86 {phone}",
            "loginType": "MobilePassword",
        }
        success, data = self.__request(url, json)
        if not success:
            return False

        self.user_id = data["data"]["userId"]
        self.token = data["data"]["accessToken"]
        self.headers["Authorization"] = self.token
        return True

    def set_project_id(self, project="",team=""):
        """设置项目

        Args:
            project (_type_): 项目ID或项目名称

        Returns:
            _type_: 成功返回true,失败返回false并打印错误
        """
        successs, data = self.get_projects()
        if not successs:
            return successs, data

        try:
            int(project)
            self.project_id = project
            for item in data:
                if item["id"] == project:
                    self.headers["X-Project-Id"] = str(project)
                    return True, "设置项目成功"
            self.project_id = ""
            return False, f"没有找到ID为{project}的项目"
        except Exception:
            for item in data:
                if item["name"] == project:
                    self.headers["X-Project-Id"] = str(item["id"])
                    self.project_id = item["id"]
                    return True, "设置项目成功"

            success, data = self.create_project(project,team)
            if not success:
                return success, data

            self.project_id = data["id"]
            self.headers["X-Project-Id"]=str(self.project_id )
            return success, data

    def get_user_info(self):
        """获取用户信息

        Returns:
            _type_: 成功返回用户信息,失败返回false并打印错误
        """
        url = "https://api.apifox.com/api/v1/user?locale=zh-CN"
        return self.__request(url)

    def get_teams(self):
        """获取团队信息

        Returns:
            _type_: 成功返回团队信息,失败返回false并打印错误
        """
        url = "https://api.apifox.com/api/v1/user-teams?locale=zh-CN"
        return self.__request(url)

    def get_notices(self):
        """获取通知信息

        Returns:
            _type_: 成功返回通知信息,失败返回false并打印错误
        """
        url = "https://api.apifox.com/api/v1/notices?locale=zh-CN"
        return self.__request(url)

    def get_projects(self):
        """获取项目信息

        Returns:
            _type_: 成功返回项目信息,失败返回false并打印错误
        """
        url = "https://api.apifox.com/api/v1/user-projects?locale=zh-CN"
        return self.__request(url)

    def get_members(self, team_id):
        """获取团队成员信息

        Returns:
            _type_: 成功返回团队成员信息,失败返回false并打印错误
        """
        url = f"https://api.apifox.com/api/v1/teams/{team_id}/members?locale=zh-CN"
        return self.__request(url)

    def get_usage(self, team_id):
        """获取使用信息

        Returns:
            _type_: 成功返回使用信息,失败返回false并打印错误
        """
        url = f"https://api.apifox.com/api/v1/teams/{team_id}/usage?locale=zh-CN"
        return self.__request(url)

    def get_project_info(self):
        """获取项目信息

        Returns:
            _type_: 成功返回项目信息,失败返回false并打印错误
        """
        url = f"https://api.apifox.com/api/v1/projects/{self.project_id}/sprint-branches?locale=zh-CN"
        return self.__request(url)

    def get_project_settings(self):
        """获取项目设置

        Returns:
            _type_: 成功返回项目设置,失败返回false并打印错误
        """
        url = f"https://api.apifox.com/api/v1/projects/{self.project_id}/project-setting?locale=zh-CN"
        return self.__request(url)

    def get_environments(self):
        """获取环境信息

        Returns:
            _type_: 成功返回环境信息,失败返回false并打印错误
        """
        url = f"https://api.apifox.com/api/v1/projects/{self.project_id}/environments?locale=zh-CN"
        return self.__request(url)

    def get_api_folders(self):
        """获取API文件夹信息

        Returns:
            _type_: 成功返回API文件夹信息,失败返回false并打印错误
        """
        url = f"https://api.apifox.com/api/v1/projects/{self.project_id}/api-detail-folders?locale=zh-CN"
        return self.__request(url)

    def get_api_tree(self):
        """获取API树信息

        Returns:
            _type_: 成功返回API树信息,失败返回false并打印错误
        """
        url = f"https://api.apifox.com/api/v1/projects/{self.project_id}/api-tree-list?locale=zh-CN"
        return self.__request(url)

    def get_api_detail(self):
        """获取API详情

        Returns:
            _type_: 成功返回API详情,失败返回false并打印错误
        """
        url = "https://api.apifox.com/api/v1/api-details?locale=zh-CN"
        return self.__request(url)

    def create_team(self, name):
        """创建团队

        Args:
            name (str): 团队名称

        Returns:
            _type_: 成功返回团队信息,失败返回false并打印错误
        """
        success, data = self.get_teams()
        if not success:
            return success, data
        for item in data:
            if item["name"] == name:
                return True, item
        url = "https://api.apifox.com/api/v1/teams?locale=zh-CN"
        json_data = {"name": name}
        return self.__request(url, json=json_data)

    def delete_team(self, team_id):
        """删除团队

        Args:
            team_id (str): 团队ID

        Returns:
            _type_: 成功返回true,失败返回false并打印错误
        """
        url = f"https://api.apifox.com/api/v1/teams/{team_id}?locale=zh-CN"
        return self.__request(url, method="DELETE")

    def put_team(self, team_id, name):
        """修改团队名称

        Args:
            team_id (str): 团队ID

        Returns:
            _type_: 成功返回true,失败返回false并打印错误
        """
        url = f"https://api.apifox.com/api/v1/teams/{team_id}?locale=zh-CN"
        data = f"name={quote(name)}&id={team_id}"
        return self.__request(url, method="PUT", data=data)

    def create_project(self, name, team=""):
        """创建项目

        Args:
            name (str): 项目名称
            team (str): 团队ID,如果不填,则会根据项目名称自动创建一个团队

        Returns:
            _type_: 成功返回项目信息,失败返回false并打印错误
        """
        if team == "":
            team=f"{name}团队"
        try:
            if int(team):
                team_id = str(team)
        except Exception:
            is_find=False
            success, data = self.get_teams()
            if not success:
                return success, data
            for item in data:
                if item["name"] == team:
                    team_id = item["id"]
                    is_find=True
                    break
            if not is_find:
                success, data = self.create_team(item)
                if not success:
                    return success, data
                team_id = data["id"]

        success, data = self.get_user_info()
        if not success:
            return success, data
        membersRoleList = (
            f"[{{'username':'{data['name']}','userId':{data['id']} ,'roleType':1}}]"
        )

        url = "https://api.apifox.com/api/v1/projects?locale=zh-CN"
        data = f"type=HTTP&name={quote(name)}&isIncludeExample=false&memberPermission=0&language=zh-CN&teamId={team_id}&membersRoleList={quote(membersRoleList)}&icon=https%3A%2F%2Fcdn.apifox.com%2Fapp%2Fproject-icon%2Fbuiltin%2F4.jpg&toApiHub=false"
        return self.__request(url, data=data)

    def delete_project(self):
        """删除项目

        Args:
            team_id (str): 团队ID

        Returns:
            _type_: 成功返回true,失败返回false并打印错误
        """
        url = f"https://api.apifox.com/api/v1/projects/{self.project_id}?locale=zh-CN"
        return self.__request(url, method="DELETE")

    def create_folder(self, name, parent_id="0"):
        """创建文件夹

        Args:
            name (str): 文件夹名称
            parentId (int, optional): 父文件夹ID. Defaults to 0.

        Returns:
            _type_: 成功返回文件夹信息,失败返回false并打印错误
        """
        success,data=self.get_api_folders()
        if not success:
            return success,data
        for item in data:
            if item["name"]==name:
                return True,item
        url = "https://api.apifox.com/api/v1/api-detail-folders?locale=zh-CN"
        data = f"name={quote(name)}&parentId={parent_id}&type=http"
        return self.__request(url, data=data)

    def delete_folders(self, folder_id):
        """删除文件夹

        Args:
            folder_id (str): 文件夹ID
        Returns:
            _type_: 成功返回true,失败返回false并打印错误
        """
        url = (
            f"https://api.apifox.com/api/v1/api-detail-folders/{folder_id}?locale=zh-CN"
        )
        return self.__request(url, method="DELETE")

    def create_environment(self, name, base_urls):
        """创建环境

        Args:
            name (str): 环境名称
            base_url (list): 环境变量,格式:[{"name":"环境变量名称","baseUrl":"环境变量值"}],第一个为默认

        Returns:
            _type_: 成功返回环境信息,失败返回false并打印错误
        """
        success, data = self.get_environment_servers()
        if not success:
            return success, data
        env_ser_id = data["id"]
        base_url = {}
        need_add = False
        for i, _ in enumerate(base_urls):
            is_find = False
            for item in data["servers"]:
                if item["name"] == base_urls[i]["name"]:
                    id = item["id"]
                    is_find = True
                    break

            if not is_find:
                need_add = True
                id = str(uuid.uuid4())
                data["servers"].append(
                    {
                        "name": base_urls[i]["name"],
                        "id": id,
                    }
                )

            base_url[id] = base_urls[i]["baseUrl"]
            base_urls[i]["id"] = id
        if need_add:
            success, data = self.create_environment_servers(env_ser_id, data["servers"])
            if not success:
                return success, data

        url = "https://api.apifox.com/api/v1/environments?locale=zh-CN"
        data = f"name={quote(name)}&visibility=protected&baseUrls={quote(json.dumps(base_url))}&servers={quote(json.dumps(base_urls))}&variables=%5B%5D&parameters=%7B%22cookie%22%3A%5B%5D%2C%22query%22%3A%5B%5D%2C%22header%22%3A%5B%5D%2C%22body%22%3A%5B%5D%7D&tags=%5B%7B%22name%22%3A%22%22%2C%22color%22%3A%22%23FA541C%22%7D%5D"
        return self.__request(url, data=data)

    def create_var(self):
        """创建提取变量,token"""
        success, data = self.get_environment_servers()
        if not success:
            return success, data
        for item in data["postProcessors"]:
            if item["data"]["variableName"] == "token":
                return True, data
        data["postProcessors"].append(
            {
                "type": "extractor",
                "data": {
                    "variableName": "token",
                    "variableType": "environment",
                    "subject": "responseHeader",
                    "template": "",
                    "expression": "Authorization",
                    "extractSettings": {
                        "expression": "Authorization",
                        "continueExtractorSettings": {
                            "isContinueExtractValue": False,
                            "JsonArrayValueIndexValue": "",
                        },
                    },
                },
                "defaultEnable": True,
                "enable": True,
                "id": uuid.uuid4().hex[0:21],
            }
        )

        return self.create_environment_servers(
            data["id"], postProcessors=data["postProcessors"]
        )

    def get_environment_servers(self):
        """获取环境服务"""
        url = f"https://api.apifox.com/api/v1/projects/{self.project_id}/project-setting?locale=zh-CN"
        return self.__request(url)

    def create_environment_servers(self, env_ser_id, servers=None, postProcessors=None):
        """创建/更新/删除环境服务

        json_data格式:

            {"id":4933615,"servers":[{"name":"默认服务","id":"default"},{"name":"ok1","id":"8c656dc2-6ef5-45cb-a628-e8f90fc17f75"},{"name":"测试a","id":"075dccce-02f4-4536-9343-54b81cfcbf99"},{"name":"hao","id":"2aca706f-0a91-4781-ac42-4ad309a8df04"}]}

        """
        success,data=self.get_api_folders()
        if not success:
            return success, data
        if len(data)==1:
            success, data =self.create_folder("临时")
            if not success:
                return success, data
            folder_id = data["id"]

            
            


        url = f"https://api.apifox.com/api/v1/project-setting/{env_ser_id}?locale=zh-CN"
        json_data = {"id": env_ser_id}
        if servers:
            json_data["servers"] = servers
        elif postProcessors:
            json_data["auth"] = {"type": "bearer", "bearer": {"token": "{{token}}"}}
            json_data["postProcessors"] = postProcessors
        else:
            return False, "参数错误"
        success, data = self.__request(url, json=json_data, method="PUT")
        if folder_id:
            success, data=self.delete_folders(folder_id)
        return success, data

    def delete_environment(self, env_id):
        """删除环境"""
        url = f"https://api.apifox.com/api/v1/environments/{env_id}?locale=zh-CN"
        return self.__request(url, method="DELETE")

    def __find_api_by_folder_and_name(self,data, folder_id, api_name):
            # 遍历数据中的每个条目
        for item in data:
            # 检查当前条目的类型是否为apiDetailFolder
            if item['type'] == 'apiDetailFolder':
                # 递归地在子项中查找
                result = self.__find_api_by_folder_and_name(item['children'], folder_id, api_name)
                if result:
                    return result
            elif item['type'] == 'apiDetail':
                # 检查当前API的folderId和name是否符合条件
                if item['api']['folderId'] == folder_id and item['api']['name'] == api_name:
                    return item


    def create_api(self,folder_id,path,name,method,body={},parameters={},status="released",description="",responses=[],
    ):
        """创建/更新接口

        Args:
            folder_id (_type_): 目录ID
            path (_type_): 接口路径
            name (_type_): 接口名称
            method (_type_): 请求方式
            body (_type_): body参数
            parameters (_type_): uri参数
            status (str, optional): 接口状态. Defaults to "released|已发布 developing|开发中"
            description (str, optional): 接口描述. Defaults to "".
            responses (list, optional): 返回实例. Defaults to [].

        Returns:
            _type_: _description_
        """
        success,data=self.get_apis()
        if not success:
            return False,data
        data=self.__find_api_by_folder_and_name(data, folder_id, name)
        if data:
            api_id=data["api"]["id"]
            url = f"https://api.apifox.com/api/v1/api-details/{api_id}?locale=zh-CN"
            data=f"path={quote(path)}&method={method}&name={quote(name)}&folderId={folder_id}&status={status}&serverId=&responsibleId=0&tags=%5B%5D&description={quote(description)}&operationId=&sourceUrl=&responses={quote(json.dumps(responses))}&responseExamples=%5B%5D&codeSamples=%5B%5D&commonParameters=%7B%7D&customApiFields=%7B%7D&commonResponseStatus=%7B%7D&responseId=0&type=http&id={api_id}&parameters={quote(json.dumps(parameters))}&requestBody={quote(json.dumps(body))}&responseChildren=%5B%5D&auth=%7B%7D&advancedSettings=%7B%22disabledSystemHeaders%22%3A%7B%7D%7D&inheritPostProcessors=%7B%7D&inheritPreProcessors=%7B%7D&preProcessors=%5B%5D&postProcessors=%5B%5D"
            return self.__request(url, method="PUT", data=data)

        timestamp = int(time.time() * 1000)
        url = "https://api.apifox.com/api/v1/api-details?locale=zh-CN"
        data = f"path={quote(path)}&method={method}&name={quote(name)}&folderId={folder_id}&status={status}&serverId=&responsibleId=0&description={quote(description)}&operationId=&sourceUrl=&responses={quote(json.dumps(responses))}&responseExamples=%5B%5D&codeSamples=%5B%5D&commonParameters=%7B%7D&customApiFields=%7B%7D&commonResponseStatus=%7B%7D&responseId=0&type=http&parameters={quote(json.dumps(parameters))}&requestBody={quote(json.dumps(body))}&responseChildren=%5B%22TEMP.{timestamp}%22%5D&auth=%7B%7D&advancedSettings=%7B%22disabledSystemHeaders%22%3A%7B%7D%7D&inheritPostProcessors=%7B%7D&inheritPreProcessors=%7B%7D&preProcessors=%5B%5D&postProcessors=%5B%5D"
        return self.__request(url, method="POST", data=data)

    def get_apis(self):
        """获取接口列表"""
        url = f"https://api.apifox.com/api/v1/projects/{self.project_id}/api-tree-list?locale=zh-CN"
        return self.__request(url)

    def delete_api(self, api_id):
        """删除接口"""
        url = f"https://api.apifox.com/api/v1/api-details/{api_id}?locale=zh-CN"
        return self.__request(url, method="DELETE")

    def auto_api(self, func):
        
        # 当前被执行的文件路径 'D:\\new_project\\新建文件夹\\apifox.py'
        file_path = inspect.getfile(func)
        # 取文件名,不带后缀 apifox
        file_name = file_path.split("\\")[-1].replace(".py", "")
        # 拼接api地址,文件名+函数名,/apifox/test
        api_path = f"/{file_name}/{func.__name__}"
        # 获取注解,并用换行符分割
        docs = func.__doc__.split("\n")
        # 初始化变量
        key=summary = ""
        data = {"type": "application/json", "parameters": [], "jsonSchema": {"type":"object","properties":{},"x-apifox-orders":[],"required":[]}}
        params = {}
        # 处理分割后的注解
        for item in docs:
            # 去首尾空
            item = item.strip()
            # 如果是空,跳过
            if not item:
                continue
            # 通过冒号判断是否为键
            if item[-1] == ":":
                key = item[:-1]
                continue
            if key == "Name":
                name = item
                continue
            if key == "Method":
                method = item
                continue
            if key == "Summary":
                summary += f"{item}\n"
                continue
            if key == "Folder":
                ls = item.split("/")
                folder_id="0"
                for v in ls:
                    success,folder_data=self.create_folder(v,parent_id=folder_id)
                    if not success:
                        raise Exception(folder_data)
                    folder_id = folder_data["id"]
                continue
            if key == "Args":
                mock=description=""
                tmp = item.split(":")
                tmp[0] = tmp[0].replace("(", "")
                tmp[0] = tmp[0].replace(")", "")
                val = tmp[0].split(" ")
                if "," in val[1]:
                    val[1] = val[1].split(",")[0].strip()
                    if "&" in tmp[1]:
                        temp=tmp[1].split("&")
                        tmp[1]=temp[0].strip()
                        mock=temp[1].replace('"',"").strip()
                    if "|" in tmp[1]:
                        temp=tmp[1].split("|")
                        tmp[1]=temp[0].strip()
                        description=temp[1].replace('"',"").strip()
                else:
                    data["jsonSchema"]["required"].append(val[0])
                
                if val[1] == "str":
                    val[1] = "string"
                elif val[1] == "int":
                    val[1] = "integer"
                elif val[1] == "float":
                    val[1] = "number"
                elif val[1] == "bool":
                    val[1] = "boolean"
                elif val[1] == "list":
                    val[1] = "array"
                elif val[1] == "None":
                    val[1] = "null"
                params[val[0]]={"title":tmp[1]}
                params[val[0]]["mock"]={"mock":mock}
                params[val[0]]["description"]=description
                params[val[0]]["type"]=val[1]
                data["jsonSchema"]["x-apifox-orders"].append(val[0])

            if key in ["Returns", "Raises", "Args", "Yields"]:
                continue
        
        data["jsonSchema"]["properties"]=params
        if not folder_id or not name or not method:
            raise Exception("缺少必要参数,Folder或Name或Method")
        success,data=self.create_api(folder_id=folder_id,path=api_path, name=name, method=method, description=summary,body=data)
        if not success:
            raise Exception(data)
        return func


# a = Apifox(
#     "新程序",
#     "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjAxMTU2LCJ0cyI6IjhiYjUxNDUzNGE3MDEwODEiLCJpYXQiOjE3MjI0MDg4NDI2MzB9.xY0pj4fcJNegFmjzS9erhqWq40It2cV6eBUQIDSW-NI",
# )
# # print(a.create_project("小程序","2788445"))
# b = [
#     {"name": "测试a", "baseUrl": "http://localhost:8080"},
#     {"name": "hao", "baseUrl": "http://localhost1:808"},
# ]


# # su, data = a.set_project_id("小程序")
# # print(su, data)
# # # print(a.create_environment("4919256", "yaode", b))
# # # print(a.delete_environment("4919256","23153759"))
# # print(a.create_api("39073174","/aaa","测试","{}","POST"))
# # # su,data=a.get_projects()
# # # print(json.dumps(data))
# @a.auto_api
# def test( url:list, text:uuid,api:str="Apifox"):
#     """
#     Name:
#         测试的a

#     Method:
#         GET

#     Folder:
#         后台/用户

#     Summary:
#         okokok

#     Args:
#         text (int): 文本
#         api (str, optional): 地址api&"Apifox"

#     Returns:
#         _type_: _description_
#     """    

#     return "ok"


# test("39073174", "/aaa", "测试")
# # 4919256
