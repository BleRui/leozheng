#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os,re
sys.path.append("../common")
sys.path.append("../scm")
import codecc_config as config
import codecc_web,json,file
import scm
import main,time
import pid_config
import util
import traceback

offline_properties_info ={}
params_sub = {}


def main_input(message):             #工具扫描主类
    global params_sub
    start_date = util.get_datetime() #开始时间
    config.load_properties()
    
    config.get_stream_name_and_tool(message)
    
    tool_type = config.properties_info['TOOL_TYPE']
    stream_name = config.properties_info['STREAM_NAME'] 
    
    #load multi tool properties
    config.load_mutil_tool_properties(tool_type)
    
    #map CodeCC API data
    config.map_properties_info(offline_properties_info)
    
    #map command properties info
    config.map_offline_properties_info(offline_properties_info)
    
    #verify all properties
    # config.verify_info()
    
    #update the properties
    config.properties_update()
    
    config.generate_config(config.properties_info)

    if "SUB_PATH" in config.properties_info:
        os.environ["PATH"] = config.properties_info['SUB_PATH'] + os.pathsep + os.environ["PATH"]
        
    #开始清空pid文件
    pid_config.clean_pid(config.properties_info["PID_FILE"])
    #添加自身pid
    pid_config.add_pid(str(os.getpid()), config.properties_info["PID_FILE"])
      
    if 'OFFLINE' in config.properties_info:
        #排队开始
        params_sub = {'stepNum': str(1), 'startTime': str(int(time.time())), 'endTime': '0', 'msg': '', 'flag': 3}
        codecc_web.codecc_upload_task_log(config.params_root, params_sub)
        
    #排队结束
    params_sub = {'stepNum': str(1), 'startTime': '0', 'endTime': str(int(time.time())), 'msg': '', 'flag': 1}
    codecc_web.codecc_upload_task_log(config.params_root, params_sub)
    
    #下载开始
    params_sub = {'stepNum': str(2), 'startTime': str(int(time.time())), 'endTime': '0', 'msg': '', 'flag': 3}
    codecc_web.codecc_upload_task_log(config.params_root, params_sub)     

    #download source code
    latest_info = main.download_code(config.properties_info)

    #下载结束
    params_sub = {'stepNum': str(2), 'startTime': '0', 'endTime': str(int(time.time())), 'msg': str(latest_info), 'flag': 1}
    codecc_web.codecc_upload_task_log(config.params_root, params_sub)
    
    #git项目，获取本地remote url和branch
    config.properties_git_info_update()
       
    #扫描开始
    scan_finish_message = ""
    params_sub = {'stepNum': str(3), 'startTime': str(int(time.time())), 'endTime': '0', 'msg': '', 'flag': 3}
    codecc_web.codecc_upload_task_log(config.params_root, params_sub)
    
    if tool_type == "cpplint":
        if "SUB_PATH" in config.properties_info and 'PY27_PATH' in config.properties_info:
            config.properties_info['SUB_PATH'] = config.properties_info["PY27_PATH"] + os.pathsep + config.properties_info["SUB_PATH"]
        file.skip(config.properties_info)
    elif tool_type == "pylint" or tool_type == "eslint" or tool_type == "checkstyle" or \
        tool_type == "stylecop" or tool_type == "ccn" or tool_type == "detekt" or \
            tool_type == "sensitive" or tool_type == "phpcs" or tool_type == "occheck" or \
            tool_type == "spotbugs":
        if "SUB_PATH" in config.properties_info and 'PY35_PATH' in config.properties_info:
            config.properties_info['SUB_PATH'] = config.properties_info["PY35_PATH"] + os.pathsep + config.properties_info["SUB_PATH"]
        file.skip(config.properties_info)
    elif tool_type == "dupc" or tool_type == "goml":
        if "SUB_PATH" in config.properties_info and 'PY35_PATH' in config.properties_info:
            config.properties_info['SUB_PATH'] = config.properties_info["PY35_PATH"] + os.pathsep + config.properties_info["SUB_PATH"]
    main.main_scan(config.properties_info)
    #print(util.get_datetime()+" "+tool_type+" generate scm blame and info")
    scm.generate_blame_and_info(config.properties_info)
    
    if tool_type == "goml" and os.path.exists(config.properties_info['STREAM_DATA_PATH']+'/go_build.log'):
        with open(config.properties_info['STREAM_DATA_PATH']+'/go_build.log', "r", encoding = 'utf-8') as go_build_file:
            scan_finish_message = go_build_file.read()
        
    #扫描结束
    params_sub = {'stepNum': str(3), 'startTime': '0', 'endTime': str(int(time.time())), 'msg': scan_finish_message, 'flag': 1}
    codecc_web.codecc_upload_task_log(config.params_root, params_sub)
    #提交开始
    params_sub = {'stepNum': str(4), 'startTime': str(int(time.time())), 'endTime': '0', 'msg': '', 'flag': 3}
    codecc_web.codecc_upload_task_log(config.params_root, params_sub)
    
    #json the scan data
    if os.path.exists(config.properties_info["STREAM_DATA_PATH"]):
        #print(util.get_datetime()+" "+tool_type+" generate json from stream data")
        #提交数据
        if tool_type == "dupc":
            main.dupc_generate_data_json(config.properties_info)
        else:
            main.generate_data_json(config.properties_info)
        #提交平均圈复杂度数
        if tool_type == "ccn":
            codecc_web.codecc_upload_avg_ccn(stream_name, config.properties_info['TASK_ID'], config.properties_info['PROJECT_AVG_FILE_CC_LIST'])
            
    #提交结束
    params_sub = {'stepNum': str(4), 'startTime': '0', 'endTime': str(int(time.time())), 'msg': '', 'flag': 1}  
    codecc_web.codecc_upload_task_log(config.params_root, params_sub)
    print (config)
    if not 'IGNORE_DELETE_LOG' in config.properties_info:
        #删除临时文件
        private_key="/tmp/."+stream_name+'_'+tool_type+"_private_key"
        file.delete_file_folder(private_key)
        if os.path.exists(config.properties_info["STREAM_DATA_PATH"]):
            file.delete_file_folder(config.properties_info["STREAM_DATA_PATH"])
        
    #结束清空pid文件
    pid_config.clean_pid(config.properties_info["PID_FILE"])

    finish_date = util.get_datetime()
    print(tool_type+' scan finish: '+start_date+' to '+finish_date)
        
if __name__ == "__main__" :
    # sys.argv = [
    #     "scan.py",
    #     "guan_java_checkstyle",
    #     "-DLANDUN_BUILDID=b-585d11edb74945569a41b4c490c45996",
    #     "-DSCAN_TOOLS=checkstyle",
    #     "-DOFFLINE=true",
    #     "-DDATA_ROOT_PATH=D:/CodeCC_Test/data/devops/workspace",
    #     "-DSTREAM_CODE_PATH=D:/CodeCC_Test/data/devops/workspace",
    #     "-DPY27_PATH=D:/CodeCC_Test/data/devops/codecc/software/python2/bin",
    #     "-DPY35_PATH=D:/CodeCC_Test/data/devops/codecc/software/python3/bin",
    #     "-DPY27_PYLINT_PATH=D:/CodeCC_Test/data/devops/workspace",
    #     "-DPY35_PYLINT_PATH=D:/CodeCC_Test/data/devops/workspace",
    #     "-DSUB_PATH=D:/CodeCC_Test/data/devops/codecc/software/jdk/bin:D:/CodeCC_Test/data/devops/codecc/software/node/bin:D:/CodeCC_Test/data/devops/codecc/software/gometalinter/bin:D:/CodeCC_Test/data/devops/codecc/software/go/bin:D:/CodeCC_Test/data/devops/codecc/software/mono/bin:D:/CodeCC_Test/data/devops/codecc/software/php/bin:D:/CodeCC_Test/data/devops/codecc/software/libzip/bin",
    #     "-DCERT_TYPE=HTTP",
    #     "-DSCM_TYPE=git",
    #     "-DREPO_URL_MAP={\"5wZe\":\"http://git.canwaysoft.cn:8888/zhongguan/test_java.git\"}",
    #     "-DREPO_RELPATH_MAP={\"5wZe\":\"\"}",
    #     "-DSUB_CODE_PATH_LIST=",
    #     "-DREPO_SCM_RELPATH_MAP={\"5wZe\":\"\"}",
    #     "-DDEVOPS_PROJECT_ID=guanpro",
    #     "-DDEVOPS_BUILD_TYPE=DOCKER",
    #     "-DDEVOPS_AGENT_ID=ejmqvnrp",
    #     "-DDEVOPS_AGENT_SECRET_KEY=dI0fpQMLPeRQa0J7xpjETKcqpKor8Dm",
    #     "-DLD_ENV_TYPE=PUBLIC",
    #     "-DMOUNT_PATH=D:/CodeCC_Test/data/devops/codecc",
    #     "-DIGNORE_DELETE_LOG=true"
    # ]
    sys.argv=[
        "scan.py",
        "test_java_checkstyke_checkstyle",
        "-DLANDUN_BUILDID=b-add7400f37d24b43ac44f2dc50b15de7",
        "-DSCAN_TOOLS=checkstyle",
        "-DOFFLINE=true",
        "-DDATA_ROOT_PATH=/data/devops/workspace",
        "-DSTREAM_CODE_PATH=/data/devops/workspace",
        "-DPY27_PATH=/data/devops/codecc/software/python2/bin",
        "-DPY35_PATH=/data/devops/codecc/software/python3/bin",
        "-DPY27_PYLINT_PATH=/data/devops/workspace",
        "-DPY35_PYLINT_PATH=/data/devops/workspace",
        "-DSUB_PATH=/data/devops/codecc/software/jdk/bin:/data/devops/codecc/software/node/bin:/data/devops/codecc/software/gometalinter/bin:/data/devops/codecc/software/go/bin:/data/devops/codecc/software/mono/bin:/data/devops/codecc/software/php/bin:/data/devops/codecc/software/libzip/bin",
        "-DCERT_TYPE=HTTP",
        "-DSCM_TYPE=git",
        "-DREPO_URL_MAP={\"5wZe\":\"http://git.canwaysoft.cn:8888/zhongguan/test_java.git\"}",
        "-DREPO_RELPATH_MAP={\"5wZe\":\"\"}",
        "-DSUB_CODE_PATH_LIST=",
        "-DREPO_SCM_RELPATH_MAP={\"5wZe\":\"\"}",
        "-DDEVOPS_PROJECT_ID=guanpro",
        "-DDEVOPS_BUILD_TYPE=DOCKER",
        "-DDEVOPS_AGENT_ID=kmxoyyxp",
        "-DDEVOPS_AGENT_SECRET_KEY=CSb1Uy62uUKR5qXYvjFU2XWov73s8Dz",
        "-DLD_ENV_TYPE=PUBLIC",
        "-DMOUNT_PATH=/data/devops/codecc"
    ]
    print(sys.argv)
    try:
        if len(sys.argv) == 2:
            main_input(sys.argv[1])
        elif len(sys.argv) > 3:
            for i in range(len(sys.argv)-2):                                           #判断命令格式是否正确
                if not "=" in sys.argv[i+2] or not "-D" in sys.argv[i+2]:               #如果没有=或者-D,
                    print("Usage python %s [stream_name] -Dxxx=xxx" % sys.argv[0])   #sys.argv[0]:"scan.py"
                    sys.exit()
            for i in range(len(sys.argv)-2):
                tmp = sys.argv[i+2].split("=",1)                                          #以=为分隔符，分隔一次成两个
                if tmp[0].__eq__("-DSCM_TYPE") and tmp[1].__eq__("code_tfs_git"):      #将参数-DSCM为"code_tfs_git":
                    offline_properties_info[tmp[0].replace("-D", "")] = "git"
                else:
                    offline_properties_info[tmp[0].replace("-D","")] = tmp[1].replace("\n", "")
            
            main_input(sys.argv[1])
        else:
            print(util.get_datetime()+ " Usage python %s [stream_name]_[cpplint&astyle&pylint] " % sys.argv[0])
            sys.exit()
    except Exception as e:
        params_sub['startTime'] = '0'
        params_sub['endTime'] = str(int(time.time()) / 1000)
        params_sub['flag'] = 2
        params_sub['msg'] = 'Exception Error: '+str(e)
        codecc_web.codecc_upload_task_log(config.params_root, params_sub) 
        traceback.print_exc()
        sys.exit(1)
        
        
