import inspect, json
from datetime import datetime
import os

def auto_api(func):
    file_path = inspect.getfile(func)
    file_name = file_path.split("\\")[-1].replace(".py", "")
    api_url = f"/{file_name}/{func.__name__}"
    docs = func.__doc__.split("\n")
    tip = ""
    doc_path = ""
    doc_name = ""
    params = ""
    example = {}
    for doc in docs:
        if not doc:
            continue
        doc = doc.strip()
        if not tip:
            if doc[-1] == ":":
                tip = doc
            else:
                description = doc
        else:
            if not doc:
                continue
            print(doc)
            if doc[-1] == ":":
                tip = doc
                continue
            else:
                if tip == "Path:":
                    tmp_list = doc.split("/")
                    doc_name = tmp_list[-1]
                    doc = doc.replace("/" + doc_name, "")
                    doc_path = f"./docs/{doc}"
                elif tip == "Args:":
                    tmp = doc.split(":")
                    tmp[0] = tmp[0].replace("(", "")
                    tmp[0] = tmp[0].replace(")", "")
                    val = tmp[0].split(" ")
                    if "," in val[1]:
                        val[1] = val[1].replace(",", "")
                        params += f"\n|{val[0]}|{val[1]}|否|{tmp[1]}|"
                    else:
                        params += f"\n|{val[0]}|{val[1]}|是|{tmp[1]}|"
                    example[f"{val[0]}"] = ""

    with open("template_api.md", "r", encoding="utf-8") as f:
        template = f.read()

    template = template.replace("^请求地址^", api_url)
    template = template.replace("^请求方式^", "POST")
    template = template.replace("^描述信息^", description)
    template = template.replace(
        "^更新时间^", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    template = template.replace(
        "^请求参数^", f"|名称|类型|必填|说明|\n|-|-|:-:|-|{params}"
    )
    template = template.replace(
        "^请求示例^",
        f"```json\n{json.dumps(example,indent=4, ensure_ascii=False)}\n```",
    )
    os.makedirs(doc_path, exist_ok=True)

    with open(f"{doc_path}/{doc_name}.md", "w", encoding="utf-8") as f:
        f.write(template)

    # """_summary_

    # Path:
    #     前台/用户/登录

    # Args:
    #     phone (str): _description_
    #     password (str): _description_
    #     ok (str, optional): _description_. Defaults to "".

    # Returns:
    #     str: _description_
    # """
    return func