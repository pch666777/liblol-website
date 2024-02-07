# coding=utf-8
import pandas as pd


def indexmd():

    df = pd.read_csv(
        "../static/data/loongapplist-latest.csv", engine="python", encoding="utf-8-sig"
    )
    df.sort_values("应用编号", ascending=True, inplace=True)
    # 删除开源软件
    df.drop((df[df["开发者"] == "开源软件"]).index, inplace=True)
    # 删除二进制翻译软件
    df.drop((df[df["开发者"] == "二进制翻译软件"]).index, inplace=True)
    # 删除开源软件（云顶书院迁移）
    df.drop((df[df["开发者"] == "开源软件（云顶书院迁移）"]).index, inplace=True)
    # 添加兼容性
    df = df.assign(兼容性="未测试")
    # 添加liblol版本
    df = df.assign(liblol版本="最新")
    # 修改页面链接
    for url in df["页面链接"]:
        url_new = "[查看](" + str(url) + ")"
        df.loc[df["页面链接"] == url, "页面链接"] = url_new
    # 添加每个app单独的页面超链接
    for id in df["应用编号"]:
        url = "[查看](" + "./" + str(id) + ")"
        df.loc[df["应用编号"] == id, "安装教程"] = url
    # 删除以下几列
    df.drop(columns="可执行文件", axis=1, inplace=True)
    df.drop(columns="图片链接", axis=1, inplace=True)
    df.drop(columns="应用类型", axis=1, inplace=True)
    df.drop(columns="文件大小", axis=1, inplace=True)
    df.drop(columns="更新时间", axis=1, inplace=True)
    df.drop(columns="开发者", axis=1, inplace=True)
    df.drop(columns="下载链接", axis=1, inplace=True)
    df.rename(
        columns={
            "应用编号": "编号",
            "安装教程": "详细信息",
            "版本号": "版本",
        },
        inplace=True,
    )
    # 生成文档头
    title = "---\ntitle: 龙芯应用合作社\ntoc: false\nweight: 5\n---\n"
    with open("../content/docs/apps/loong/_index.md", "w", encoding="utf-8-sig") as md:
        md.write(title)
        df.fillna("", inplace=True)
        df.to_markdown(buf=md, index=False)


def appmd():
    df = pd.read_csv(
        "../static/data/loongapplist-latest.csv", engine="python", encoding="utf-8-sig"
    )
    df.drop(columns="可执行文件", axis=1, inplace=True)
    df.drop(columns="图片链接", axis=1, inplace=True)
    df.drop(columns="文件大小", axis=1, inplace=True)
    df.sort_values("应用编号", ascending=True, inplace=True)
    # 删除开源软件
    df.drop((df[df["开发者"] == "开源软件"]).index, inplace=True)
    # 删除二进制翻译软件
    df.drop((df[df["开发者"] == "二进制翻译软件"]).index, inplace=True)
    # 删除开源软件（云顶书院迁移）
    df.drop((df[df["开发者"] == "开源软件（云顶书院迁移）"]).index, inplace=True)
    df.rename(
        columns={
            "应用编号": "编号",
            "安装教程": "详细信息",
            "版本号": "版本",
        },
        inplace=True,
    )
    df = df.assign(兼容性="未测试")
    # 添加liblol版本
    df = df.assign(liblol版本="最新")
    # 编辑页面链接
    for url in df["页面链接"]:
        url_new = "[跳转](" + str(url) + ")"
        df.loc[df["页面链接"] == url, "页面链接"] = url_new
    # 编辑下载链接
    for time in df["更新时间"]:
        time_new = str(time)
        time_new = time_new.replace("T", " ")
        df.loc[df["更新时间"] == time, "更新时间"] = time_new
    for url in df["下载链接"]:
        url_new = "[下载](" + str(url) + ")"
        df.loc[df["下载链接"] == url, "下载链接"] = url_new
    # 以appid生成文件名
    for id in df["编号"]:
        filename = "../content/docs/apps/loong/" + str(id) + ".md"
        title = str(df.loc[df["编号"] == id, "应用名称"].values)
        title = title[2:-2]
        head = (
            ("---\nid: " + str(id) + "\ntitle: ")
            + title
            + "\ntoc: true\nweight: "
            + str(id)
            + "\n---\n"
            + "\n## 应用信息 \n"
        )
        df.rename(
            columns={
                "应用编号": "编号",
                "安装教程": "详细信息",
                "版本号": "版本",
            },
            inplace=True,
        )
        appinfo = df.loc[df["编号"] == id]
        body = (
            "\n### 安装libLoL及该应用 \n参考[使用方法](/docs/usage) \n### 额外操作 \n"
        )
        footer = "\n\n## 历史版本 \n "
        # body = str(body)
        # print(body)
        with open(filename, "w", encoding="utf-8-sig") as file:
            file.write(head)
            appinfo.to_markdown(buf=file, index=False)
            file.write(body)
            file.write(footer)


indexmd()
appmd()
