#!/usr/bin/env python
#~*~coding:utf8~*~
import sys,os,json
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)) + "/lib")
import optparse
import ConfigParser
import check,state
import serverlist
from arg import *

def printServerlist():
    for i in getserverlist():
        #print i
        if isinstance(i,list):
            print i[0] + "@" + i[1]
        else:
            print i 
    #print json.dumps(getserverlist())
def arg_init():
    global options
    global config
    config = ConfigParser.ConfigParser()
    dir = os.path.dirname(os.path.abspath(__file__))
    conf = dir + "/conf"
    #切换目录到文件所在目录
    parser = optparse.OptionParser() 
    parser.add_option("-g","--game",dest="game",help="指定项目名称，比如:gcmob")
    parser.add_option("-a","--action",dest="action",help="指定操作类型，比如:deploy,update")
    parser.add_option("-l","--language",dest="language",help="指定语言，比如:cn,vn,ft")
    parser.add_option("-s","--servername", dest="servername", help="指定游戏服名称，比如:feiliu_1")
    parser.add_option("-i","--ip", dest="ip", help="ip地址，比如:1.1.1.1")
    parser.add_option("--port", dest="port",default=22,type="int", help="ssh连接端口号，默认22")
    parser.add_option("-S","--starttime", dest="starttime", help="游戏开服时间")
    parser.add_option("-C","--cleartime", dest="cleartime", help="游戏清档时间")
    parser.add_option("-u","--uniqserver", dest="uniqserver",action="store_true", help="去重服务器ip")
    parser.add_option("-f","--serverfile", dest="serverfile", help="服务器列表文件")
    #parser.add_option("--restart", dest="restart",action="store_true", help="部署游戏混服是否重启游戏服")
    parser.add_option("--restart", dest="restart",type="choice",choices=["yes","no"], help="部署游戏混服是否重启游戏服")
    parser.add_option("--mainserver", dest="mainserver", help="混服主服名")
    parser.add_option("--title", dest="title", help="游戏www标题")
    parser.add_option("--gameurl", dest="gameurl", help="游戏域名")
    parser.add_option("--asturl", dest="asturl", help="游戏域名对应的ast的cname域名")
    parser.add_option("--skipcheck", dest="skipcheck",action="store_true", help="布服前不进行游戏是否存在检查")
    parser.add_option("--startdate", dest="startdate", help="游戏列表开服开始时间")
    parser.add_option("--enddate", dest="enddate", help="游戏列表开服结束时间")
    parser.add_option("--serverlist", dest="serverlist", help="游戏服列表，游戏精确匹配")
    parser.add_option("--excludeServerlist", dest="excludeServerlist", help="游戏服排除列表，正则精确匹配")
    parser.add_option("--templatetype", dest="templatetype", type="string", help="模板生成类型，[sql,common,conf,www,properties,nginx]")
    parser.add_option("--version", dest="version", type="string", help="更新的版本")
    parser.add_option("--updateType", dest="updateType",type="choice",choices=["appstore","appstore64","jailbreak","all"],help="更新类型，比如:appstore")
    parser.add_option("-H",dest="hd",action="store_true",help="是否高清模式")
    parser.add_option("--recoverDate",dest="recoverDate",help="还原数据库完整备份日期")
    #更新参数列表
    #parser.add_option("--sqlOrNot",dest="sqlOrNot",type="choice",choices=["yes","no"],help="是否执行sql，必须为{yes|no}")
    parser.add_option("--sqlFile",dest="sqlFile",help="如果需要执行sql，指定sql文件名称")
    #parser.add_option("--backendChangeOrNot",dest="backendChangeOrNot",type="choice",choices=["yes","no"],help="是否需要修改游戏服后端目录，必须为{yes|no}")
    #parser.add_option("--backendUpload",dest="backendUpload",type="choice",choices=["yes","no"],help="是否需要上传后端，必须为{yes|no}")
    parser.add_option("--backendName",dest="backendName",help="如果要更改后端目录或者上传后端包，指定后端目录名称")
    parser.add_option("--frontName",dest="frontName",help="前端更新目录名称")
    parser.add_option("--executeVersionList",dest="executeVersionList",help="指定需要更新的版本号，多个使用','隔开，比如:1.1.1.1,1.1.1.0")
    parser.add_option("--resourceDir",dest="resourceDir",help="放置更新需要的文件的ftp地址目录")
    parser.add_option("--replaceFile",dest="replaceFile",help="需要替换的文件列表，多个以','隔开，比如:backend/apps/job.properties=job.properties|...")
    parser.add_option("--addFile",dest="addFile",help="需要添加的文件列表，多个以','隔开，比如:backend/apps/=job.properties|...")
    parser.add_option("--addContent",dest="addContent",help="添加配置内容列表，多个以','隔开，比如:backend/apps/job.properties=add_job.properties|...")
    parser.add_option("--specialScript",dest="specialScript",help="额外更新脚本在rundeck的绝对路径")
    parser.add_option("--executeFirst",dest="executeFirst",type="choice",choices=["yes","no"],help="如果有额外更新的脚本,指定执行\时间, yes:停服后即执行脚本,no:更新完毕后执行该脚本")
    #命令执行
    parser.add_option("--cmd",dest="cmd",help="执行命令，${flag}表示游戏服比如:feiliu_1,${game}表示项目名比如:gcmob")
    #动更参数
    parser.add_option("--hotswapType",dest="hotswapType",type="choice",choices=["update","remote"],help="动更类型")
    parser.add_option("--keyword",dest="keyword",help="动更关键字")
    #重启参数
    parser.add_option("--restartType",dest="restartType",type="choice",choices=["start","stop","restart"],help="重启类型")
    #服务器恢复参数
    parser.add_option("--recoverType",dest="recoverType",type="choice",choices=["recoverhadoop","recoverbinlog"],help="恢复类型")
    parser.add_option("--failureip",dest="failureip",help="故障ip")
    parser.add_option("--recoverip",dest="recoverip",help="恢复ip")
    #添加ip白名单
    parser.add_option("--yx",dest="yx",help="需要添加白名单的yx")
    parser.add_option("--iplist",dest="iplist",help="白名单列表")
    parser.add_option("--localfile",dest="localfile",help="本地文件")
    parser.add_option("--remotefile",dest="remotefile",help="远端文件路径")
    parser.add_option("--gamerooms",dest="gamerooms",help="机房中文名称,eg:泰国机房")
    parser.add_option("--projecttag",dest="projecttag",help="项目表示，eg:gcld_th")
    ##部署游戏服的参数列表
    group = optparse.OptionGroup(parser, "游戏部署参数",
                        "-a deploy -g game -l language -s server -C cleartime -i ip [--skipcheck] [--title wwwTitle] [--gameurl gameurl] [--asturl astUrl]")
    parser.add_option_group(group)
    #命令执行参数列表
    group = optparse.OptionGroup(parser, "命令执行参数",
                        "-a cmd -g game -l language --serverlist 游戏服 [游戏服列表参数通用] --cmd 命令(${flag}替换为游戏，${game}替换为项目)")
    parser.add_option_group(group)
    #上传文件参数列表
    group = optparse.OptionGroup(parser, "上传文件参数",
                        "-a put -g game -l language --serverlist 游戏服 [游戏服列表参数通用] --localfile 本地文件 --remotefile 远端路径(${flag}替换为游戏，${game}替换为项目)")
    parser.add_option_group(group)
    ##恢复游戏服的参数列表
    group = optparse.OptionGroup(parser, "游戏恢复参数",
                        "-a recover -g game -l language -s {servername,server_ip} -i ip --recoverType [{recoverhadoop,recoverbinlog}]")
    parser.add_option_group(group)
    #移动整机游戏服到另一台
    group = optparse.OptionGroup(parser, "迁移整机参数",
                        "-a moveserver -g game -l language --failureip failureip --recoverip recoverip")
    parser.add_option_group(group)
    #mysql binlog 还原
    group = optparse.OptionGroup(parser, "binlog还原参数",
                        "-a recoverbinlog -g game -l language --failureip failureip --recoverDate recoverDate --serverfile 还原数据库列表")
    parser.add_option_group(group)
    ##部署游戏服混服的参数列表
    group = optparse.OptionGroup(parser, "游戏混服部署参数",
                        "-a deploymix -g game -l language -s server --mainserver mainserver [--restart {yes|no}] [--skipcheck] [--title wwwTitle] [--gameurl gameurl] [--asturl astUrl]")
    parser.add_option_group(group)
    ##重设清档时间的参数列表
    group = optparse.OptionGroup(parser, "重设清档时间参数",
                        "-a resetcleartime -g game -l language -s server -C cleartime -S starttime")
    parser.add_option_group(group)
    ##重设清档时间的参数列表
    group = optparse.OptionGroup(parser, "添加联运白名单参数",
                        "-a addwhiteip -g game -l language --yx yx --iplist iplist")
    parser.add_option_group(group)
    ##游戏模板生成的参数列表
    group1 = optparse.OptionGroup(parser, "游戏模板生成参数",
                        "-a template -g game -l language -s server [-i ip] [--port port] --templatetype {all|[sql][,common][,gametemplate][,www][,properties][,nginx]}")
    parser.add_option_group(group1)
    ##游戏所有模板生成的参数列表
    group1 = optparse.OptionGroup(parser, "所有游戏模板生成参数",
                        "-a alltemplate -g game -l language --templatetype {all|[sql][,common][,gametemplate][,www][,properties][,nginx]}")
    parser.add_option_group(group1)
    ##游戏服列表的参数列表
    group2 = optparse.OptionGroup(parser, "获取游戏服列表参数",
                        "-a serverlist -g game -l language --startdate 开始开服时间 --enddate 结束开服时间 --serverlist 服务器匹配 --excludeServerlist 排除服务器")
    parser.add_option_group(group2)
    #手游前端测试环境动态更新
    group2 = optparse.OptionGroup(parser, "手游前端测试环境动态更新列表参数",
                        "-a mobileWwwTestUpdate -g game -l language --updateType 更新类型 --version 更新版本号 [-H](是否区分高清资源)")
    parser.add_option_group(group2)
    #手游前端正式环境动态更新
    group2 = optparse.OptionGroup(parser, "手游前端正式环境动态更新列表参数",
                        "-a mobileWwwUpdate -g game -l language --updateType 更新类型 --version 更新版本号 [-H](是否区分高清资源)")
    parser.add_option_group(group2)
    #游戏后端更新
    group2 = optparse.OptionGroup(parser, "游戏更新参数",
                        #"-a update -g game -l language [--startdate 游戏开服日期] [--enddate 游戏开服结束日期] --serverlist 游戏列表正则表达式 --excludeServerlist 排除服务器 --restart {yes|no} --sqlOrNot {yes|no} [--sqlFile sqlFile] --backendChangeOrNot {yes|no} --backendUpload {yes|no} [--backendName name] [--executeVersionList versionList] [--resourceDir dirname] [--replaceFile replaceFilelist] [--addFile addFile] [--addContent addContent] [--specialScript scriptPath] [--executeFirst {yes|no}]")
                        "-a update -g game -l language [--startdate 游戏开服日期] [--enddate 游戏开服结束日期] --serverlist 游戏列表正则表达式 --excludeServerlist 排除服务器 --restart {yes|no} --sqlFile sqlFile --backendName name --frontName frontName [--executeVersionList versionList] [--resourceDir dirname] [--replaceFile replaceFilelist] [--addFile addFile] [--addContent addContent] [--specialScript scriptPath] [--executeFirst {yes|no}]")
    parser.add_option_group(group2)
    #动更
    group2 = optparse.OptionGroup(parser, "hotswap动更参数",
                        "-a hotswap -g game -l language [--startdate 游戏开服日期] [--enddate 游戏开服结束日期] --serverlist 游戏列表正则表达式 --excludeServerlist 排除服务器 --hotswapType {update|remote} --keyword 关键字")
    parser.add_option_group(group2)

    (options, args) = parser.parse_args() 

    global game,language,action
    game = options.game
    language = options.language
    action = options.action
    checkArg(options.game,"游戏项目不能为空")
    checkArg(options.language,"游戏语言不能为空")
    checkArg(options.action,"操作类型不能为空")
    config.read("%s/%s.conf"%(conf,options.game))
    checkSection(config,options.language)
    state.game = game
    state.language = language
    state.action = action
    state.options = options
if __name__ == "__main__" :
    arg_init()
    if options.action == "deploy":
        from func import deploy
        newserver = deploy.deploy(game,language,options.servername,options.ip,options.cleartime,title=options.title,gameurl=options.gameurl,asturl=options.asturl,skipcheck=options.skipcheck)
        newserver.run()
    elif options.action == "recover":
        #from func import recover
        from func import recover3
        recoverserver = recover3.recover(game,language,options.servername,options.ip,options.recoverType)
        recoverserver.run()
    elif options.action == "deploymix":
        from func import deployMix
        newserver = deployMix.deploy(game,language,options.servername,options.mainserver,options.restart,title=options.title,gameurl=options.gameurl,asturl=options.asturl,skipcheck=options.skipcheck)
        newserver.run()
    elif options.action == "serverlist":
        printServerlist()
    elif options.action == "mobileWwwTestUpdate":
        from func import mobile_www_test_update
        mobile_www_test_update.init(game,language,options.version,options.updateType,options.hd)
    elif options.action == "mobileWwwUpdate":
        from func import mobile_www_update
        mobile_www_update.update(game,language,options.version,options.updateType,options.hd)
    elif options.action == "template":
        from func import template
        newserverTemplate = template.template(game,language,options.servername,options.ip,options.port)
        if options.templatetype:
            type = options.templatetype.split(",")
            for i in type:
                if i.strip() == "":
                    continue
                check = False
                if i.strip() in ["sql","all"]:
                    newserverTemplate.updateServerSql()
                    check = True
                if i.strip() in ["common","all"]:
                    newserverTemplate.updateServerLib()
                    check = True
                if i.strip() in ["gametemplate","all"]:
                    newserverTemplate.updateServerConf()
                    check = True
                if i.strip() in ["properties","all"]:
                    newserverTemplate.updateServerProperties()
                    check = True
                if i.strip() in ["www","all"]:
                    newserverTemplate.updateServerWww()
                    check = True
                if i.strip() in ["nginx","all"]:
                    newserverTemplate.updateServerNginxConf()
                    check = True
                if not check:
                    print "不支持的模板类型:" + i
                    sys.exit(1)
        else:
            print "请输入生成模板的类型"
    elif options.action == "update":
        from func import update
        #update.update(options.sqlOrNot,options.sqlFile,options.backendUpload,options.backendChangeOrNot,options.backendName,options.executeVersionList,options.restart,options.resourceDir,options.replaceFile,options.addFile,options.addContent,options.specialScript,options.executeFirst,frontName)
        update.update(options.sqlFile,options.backendName,options.executeVersionList,options.restart,options.resourceDir,options.replaceFile,options.addFile,options.addContent,options.specialScript,options.executeFirst,options.frontName)
    elif options.action == "hotswap":
        from func import hotswap
        hotswap.hotswap(options.hotswapType,options.keyword)
    elif options.action == "cmd":
        from func import cmd
        cmd.cmd(options.cmd)
    elif options.action == "put":
        from func import put
        put.put(options.localfile,options.remotefile)
    elif options.action == "test":
        from func import test
        test.test()
    elif options.action == "restart":
        from func import restart
        restart.restart(options.restartType)
    elif options.action == "moveserver":
        from func import recoverByProject
        recoverByProject.recoverByProject(options.failureip,options.recoverip)
    elif options.action == "resetcleartime":
        from func import resetClearTime
        resetClearTime.reset(options.cleartime,options.starttime,options.servername)
    elif options.action == "addwhiteip":
        from func import addwhiteip
        addwhiteip.addwhiteip(options.iplist,options.yx)
    elif options.action == "alltemplate":
        from func import alltemplate
        alltemplate.alltemplate(options.templatetype)
    elif options.action == "recoverbinlog":
        from func import recoverByMysql
        recoverByMysql.recoverByMysql(options.failureip,options.recoverDate,options.serverfile)
    elif options.action == "assetrooms":
        from func import assets_count
        assets_count.assetrooms(options.gamerooms,options.projecttag)
