#!/usr/bin/python
# -*- coding: utf-8 -*-
import http.client, util, sys, json, os, network
import urllib.request
import codecc_config as config
import ssl

# 不认证https
ssl._create_default_https_context = ssl._create_unverified_context


def get_conn():
    if 443 == int(config.params_root['codeccApiPort']):
        return http.client.HTTPSConnection(config.params_root['codeccApiServer'], config.params_root['codeccApiPort'])
    else:
        return http.client.HTTPConnection(config.params_root['codeccApiServer'], config.params_root['codeccApiPort'])


def codecc_upload_task_log(params1, params2):
    params = dict(params1.items() | params2.items())
    print(config.params_root)
    headers = {"Content-type": "application/json", "x-devops-build-id": config.params_root['pipelineBuildId'],
               "x-devops-vm-sid": config.params_root['DEVOPS_AGENT_VM_SID'],
               "x-devops-project-id": config.params_root['DEVOPS_PROJECT_ID'],
               "x-devops-build-type": config.params_root['DEVOPS_BUILD_TYPE'],
               "x-devops-agent-id": config.params_root['DEVOPS_AGENT_ID'],
               "x-devops-agent-secret-key": config.params_root['DEVOPS_AGENT_SECRET_KEY']}
    jdata = json.dumps(params)
    try:
        conn = get_conn()
        conn.request("POST", "/ms/defect/api/build/tasklog/", jdata, headers)
        response = conn.getresponse()
        data = response.read()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()


def codecc_upload_file_json(file_json):
    headers = {"Content-type": "application/json", "x-devops-build-id": config.params_root['pipelineBuildId'],
               "x-devops-vm-sid": config.params_root['DEVOPS_AGENT_VM_SID'],
               "x-devops-project-id": config.params_root['DEVOPS_PROJECT_ID'],
               "x-devops-build-type": config.params_root['DEVOPS_BUILD_TYPE'],
               "x-devops-agent-id": config.params_root['DEVOPS_AGENT_ID'],
               "x-devops-agent-secret-key": config.params_root['DEVOPS_AGENT_SECRET_KEY']}
    try:
        conn = get_conn()
        conn.request("POST", "/ms/defect/api/build/defects/", file_json, headers)
        response = conn.getresponse()
        data = response.read()
    except Exception as e:
        raise Exception(e)
    finally:
        conn.close()


def get_config_data_by_codecc(stream, tool_type, headers):
    try:
        conn = get_conn()
        conn.request("GET", "/ms/task/api/build/tool/config/streamName/" + stream + "/toolType/" + tool_type.upper(),
                     {}, headers)
        response = conn.getresponse()
        # data = response.read()
        data = {
            "status": 0,
            "code": "0",
            "data": {
                "url": "http://git.canwaysoft.cn:8888/zhongguan/test_java.git",
                "task_id": 100063,
                "stream_name": "test_java_checkstyke",
                "multi_tool_type": "CHECKSTYLE",
                "SKIP_PATHS": "",
                "skip_checkers": "com.puppycrawl.tools.checkstyle.checks.blocks.RightCurlyCheck;com.puppycrawl.tools.checkstyle.checks.metrics.CyclomaticComplexityCheck;com.puppycrawl.tools.checkstyle.checks.regexp.RegexpSinglelineJavaCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.JavadocVariableCheck;com.puppycrawl.tools.checkstyle.checks.DescendantTokenCheck;com.puppycrawl.tools.checkstyle.checks.annotation.PackageAnnotationCheck;com.puppycrawl.tools.checkstyle.checks.coding.ParameterAssignmentCheck;com.puppycrawl.tools.checkstyle.checks.annotation.AnnotationUseStyleCheck;com.puppycrawl.tools.checkstyle.checks.sizes.MethodCountCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.NonEmptyAtclauseDescriptionCheck;com.puppycrawl.tools.checkstyle.checks.coding.PackageDeclarationCheck;com.puppycrawl.tools.checkstyle.checks.sizes.LineLengthCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.TypecastParenPadCheck;com.puppycrawl.tools.checkstyle.checks.naming.LocalVariableNameCheck;com.puppycrawl.tools.checkstyle.checks.naming.CatchParameterNameCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.JavadocTypeCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.AtclauseOrderCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.SingleSpaceSeparatorCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.WhitespaceAfterCheck;com.puppycrawl.tools.checkstyle.checks.coding.IllegalCatchCheck;com.puppycrawl.tools.checkstyle.checks.regexp.RegexpSinglelineCheck;com.puppycrawl.tools.checkstyle.checks.regexp.RegexpMultilineCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.EmptyForInitializerPadCheck;com.puppycrawl.tools.checkstyle.checks.metrics.ClassFanOutComplexityCheck;com.puppycrawl.tools.checkstyle.checks.annotation.MissingDeprecatedCheck;com.puppycrawl.tools.checkstyle.checks.UncommentedMainCheck;com.puppycrawl.tools.checkstyle.checks.AvoidEscapedUnicodeCharactersCheck;com.puppycrawl.tools.checkstyle.checks.sizes.OuterTypeNumberCheck;com.puppycrawl.tools.checkstyle.checks.coding.SuperCloneCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.SingleLineJavadocCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.JavadocTagContinuationIndentationCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.OperatorWrapCheck;com.puppycrawl.tools.checkstyle.checks.coding.ArrayTrailingCommaCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.EmptyForIteratorPadCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.WriteTagCheck;com.puppycrawl.tools.checkstyle.checks.TranslationCheck;com.puppycrawl.tools.checkstyle.checks.design.VisibilityModifierCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.FileTabCharacterCheck;com.puppycrawl.tools.checkstyle.checks.imports.ImportOrderCheck;com.puppycrawl.tools.checkstyle.checks.naming.InterfaceTypeParameterNameCheck;com.puppycrawl.tools.checkstyle.checks.OuterTypeFilenameCheck;com.puppycrawl.tools.checkstyle.checks.coding.DefaultComesLastCheck;com.puppycrawl.tools.checkstyle.checks.design.DesignForExtensionCheck;com.puppycrawl.tools.checkstyle.checks.coding.MissingCtorCheck;com.puppycrawl.tools.checkstyle.checks.NewlineAtEndOfFileCheck;com.puppycrawl.tools.checkstyle.checks.imports.CustomImportOrderCheck;com.puppycrawl.tools.checkstyle.checks.annotation.SuppressWarningsCheck;com.puppycrawl.tools.checkstyle.checks.coding.MissingSwitchDefaultCheck;com.puppycrawl.tools.checkstyle.checks.imports.ImportControlCheck;com.puppycrawl.tools.checkstyle.checks.coding.MagicNumberCheck;com.puppycrawl.tools.checkstyle.checks.design.FinalClassCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.ParenPadCheck;com.puppycrawl.tools.checkstyle.checks.coding.NoFinalizerCheck;com.puppycrawl.tools.checkstyle.checks.design.MutableExceptionCheck;com.puppycrawl.tools.checkstyle.checks.naming.StaticVariableNameCheck;com.puppycrawl.tools.checkstyle.checks.coding.CovariantEqualsCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.MethodParamPadCheck;com.puppycrawl.tools.checkstyle.checks.imports.AvoidStarImportCheck;com.puppycrawl.tools.checkstyle.checks.coding.SimplifyBooleanReturnCheck;com.puppycrawl.tools.checkstyle.checks.sizes.ExecutableStatementCountCheck;com.puppycrawl.tools.checkstyle.checks.coding.AvoidInlineConditionalsCheck;com.puppycrawl.tools.checkstyle.checks.design.ThrowsCountCheck;com.puppycrawl.tools.checkstyle.checks.coding.RequireThisCheck;com.puppycrawl.tools.checkstyle.checks.naming.LambdaParameterNameCheck;com.puppycrawl.tools.checkstyle.checks.coding.ReturnCountCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.EmptyLineSeparatorCheck;com.puppycrawl.tools.checkstyle.checks.header.RegexpHeaderCheck;com.puppycrawl.tools.checkstyle.checks.coding.IllegalTokenTextCheck;com.puppycrawl.tools.checkstyle.checks.FinalParametersCheck;com.puppycrawl.tools.checkstyle.checks.indentation.CommentsIndentationCheck;com.puppycrawl.tools.checkstyle.checks.TrailingCommentCheck;com.puppycrawl.tools.checkstyle.checks.naming.AbbreviationAsWordInNameCheck;com.puppycrawl.tools.checkstyle.checks.annotation.AnnotationOnSameLineCheck;com.puppycrawl.tools.checkstyle.checks.design.OneTopLevelClassCheck;com.puppycrawl.tools.checkstyle.checks.coding.SuperFinalizeCheck;com.puppycrawl.tools.checkstyle.checks.blocks.LeftCurlyCheck;com.puppycrawl.tools.checkstyle.checks.coding.MultipleStringLiteralsCheck;com.puppycrawl.tools.checkstyle.checks.metrics.ClassDataAbstractionCouplingCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.NoWhitespaceAfterCheck;com.puppycrawl.tools.checkstyle.checks.regexp.RegexpCheck;com.puppycrawl.tools.checkstyle.checks.design.InnerTypeLastCheck;com.puppycrawl.tools.checkstyle.checks.sizes.AnonInnerLengthCheck;com.puppycrawl.tools.checkstyle.checks.header.HeaderCheck;com.puppycrawl.tools.checkstyle.checks.naming.MethodTypeParameterNameCheck;com.puppycrawl.tools.checkstyle.checks.coding.FinalLocalVariableCheck;com.puppycrawl.tools.checkstyle.checks.coding.UnnecessaryParenthesesCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.JavadocMethodCheck;com.puppycrawl.tools.checkstyle.checks.coding.HiddenFieldCheck;com.puppycrawl.tools.checkstyle.checks.regexp.RegexpOnFilenameCheck;com.tencent.checks.EscapeSequenceCheck;com.puppycrawl.tools.checkstyle.checks.design.InterfaceIsTypeCheck;com.puppycrawl.tools.checkstyle.checks.indentation.IndentationCheck;com.puppycrawl.tools.checkstyle.checks.UniquePropertiesCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.WhitespaceAroundCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.NoLineWrapCheck;com.puppycrawl.tools.checkstyle.checks.coding.IllegalTypeCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.GenericWhitespaceCheck;com.puppycrawl.tools.checkstyle.checks.design.HideUtilityClassConstructorCheck;com.puppycrawl.tools.checkstyle.checks.naming.ClassTypeParameterNameCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.JavadocStyleCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.JavadocPackageCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.NoWhitespaceBeforeCheck;com.puppycrawl.tools.checkstyle.checks.coding.NoCloneCheck;com.puppycrawl.tools.checkstyle.checks.coding.ExplicitInitializationCheck;com.puppycrawl.tools.checkstyle.checks.naming.PackageNameCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.JavadocParagraphCheck;com.puppycrawl.tools.checkstyle.checks.javadoc.SummaryJavadocCheck;com.puppycrawl.tools.checkstyle.checks.annotation.AnnotationLocationCheck;com.puppycrawl.tools.checkstyle.checks.imports.AvoidStaticImportCheck;com.puppycrawl.tools.checkstyle.checks.naming.LocalFinalVariableNameCheck;com.puppycrawl.tools.checkstyle.checks.coding.IllegalInstantiationCheck;com.puppycrawl.tools.checkstyle.checks.coding.ModifiedControlVariableCheck",
                "scm_type": "GIT",
                "git_branch": "master",
                "proj_owner": "zhongguan",
                "open_checkers": "com.puppycrawl.tools.checkstyle.checks.naming.MemberNameCheck;com.puppycrawl.tools.checkstyle.checks.modifier.ModifierOrderCheck;com.puppycrawl.tools.checkstyle.checks.coding.IllegalTokenCheck;com.puppycrawl.tools.checkstyle.checks.coding.EqualsAvoidNullCheck;com.puppycrawl.tools.checkstyle.checks.naming.TypeNameCheck;com.puppycrawl.tools.checkstyle.checks.imports.RedundantImportCheck;com.puppycrawl.tools.checkstyle.checks.blocks.EmptyBlockCheck;com.puppycrawl.tools.checkstyle.checks.metrics.JavaNCSSCheck;com.puppycrawl.tools.checkstyle.checks.naming.ConstantNameCheck;com.puppycrawl.tools.checkstyle.checks.coding.EqualsHashCodeCheck;com.puppycrawl.tools.checkstyle.checks.coding.NestedIfDepthCheck;com.puppycrawl.tools.checkstyle.checks.UpperEllCheck;com.puppycrawl.tools.checkstyle.checks.coding.NestedForDepthCheck;com.puppycrawl.tools.checkstyle.checks.coding.DeclarationOrderCheck;com.puppycrawl.tools.checkstyle.checks.annotation.MissingOverrideCheck;com.puppycrawl.tools.checkstyle.checks.naming.AbstractClassNameCheck;com.puppycrawl.tools.checkstyle.checks.TodoCommentCheck;com.puppycrawl.tools.checkstyle.checks.coding.InnerAssignmentCheck;com.puppycrawl.tools.checkstyle.checks.coding.NestedTryDepthCheck;com.puppycrawl.tools.checkstyle.checks.imports.UnusedImportsCheck;com.puppycrawl.tools.checkstyle.checks.metrics.BooleanExpressionComplexityCheck;com.puppycrawl.tools.checkstyle.checks.coding.EmptyStatementCheck;com.puppycrawl.tools.checkstyle.checks.blocks.AvoidNestedBlocksCheck;com.puppycrawl.tools.checkstyle.checks.coding.SimplifyBooleanExpressionCheck;com.puppycrawl.tools.checkstyle.checks.whitespace.SeparatorWrapCheck;com.puppycrawl.tools.checkstyle.checks.coding.FallThroughCheck;com.puppycrawl.tools.checkstyle.checks.modifier.RedundantModifierCheck;com.puppycrawl.tools.checkstyle.checks.sizes.ParameterNumberCheck;com.puppycrawl.tools.checkstyle.checks.blocks.EmptyCatchBlockCheck;com.puppycrawl.tools.checkstyle.checks.coding.StringLiteralEqualityCheck;com.puppycrawl.tools.checkstyle.checks.imports.IllegalImportCheck;com.puppycrawl.tools.checkstyle.checks.sizes.FileLengthCheck;com.puppycrawl.tools.checkstyle.checks.ArrayTypeStyleCheck;com.puppycrawl.tools.checkstyle.checks.coding.OneStatementPerLineCheck;com.puppycrawl.tools.checkstyle.checks.coding.OverloadMethodsDeclarationOrderCheck;com.puppycrawl.tools.checkstyle.checks.blocks.NeedBracesCheck;com.puppycrawl.tools.checkstyle.checks.naming.MethodNameCheck;com.puppycrawl.tools.checkstyle.checks.coding.VariableDeclarationUsageDistanceCheck;com.puppycrawl.tools.checkstyle.checks.metrics.NPathComplexityCheck;com.puppycrawl.tools.checkstyle.checks.coding.IllegalThrowsCheck;com.puppycrawl.tools.checkstyle.checks.coding.MultipleVariableDeclarationsCheck;com.puppycrawl.tools.checkstyle.checks.sizes.MethodLengthCheck;com.puppycrawl.tools.checkstyle.checks.naming.ParameterNameCheck",
                "checker_options": "{}"
            }
        }
        conn.close()
    except Exception as e:
        print(stream + " get_mutil_tools_config_data")
        print(e)
        raise Exception(e)
    return data


def codecc_upload_avg_ccn(stream, task_id, project_avg_file_cc_list):
    status = False
    headers = {"Content-type": "application/json", "x-devops-build-id": config.params_root['pipelineBuildId'],
               "x-devops-vm-sid": config.params_root['DEVOPS_AGENT_VM_SID'],
               "x-devops-project-id": config.params_root['DEVOPS_PROJECT_ID'],
               "x-devops-build-type": config.params_root['DEVOPS_BUILD_TYPE'],
               "x-devops-agent-id": config.params_root['DEVOPS_AGENT_ID'],
               "x-devops-agent-secret-key": config.params_root['DEVOPS_AGENT_SECRET_KEY']}
    try:
        all_file_avg_cc = 0.000
        total_cc = 0.000
        total_count = 0
        if os.path.isfile(project_avg_file_cc_list):
            with open(project_avg_file_cc_list, "r", encoding='utf-8') as file:
                alllines = file.readlines()
                for line in alllines:
                    line = line.strip()
                    if '' == line.replace(' ', ''):
                        continue
                    line_array = line.split(':')
                    if float(line_array[0]) > 0:
                        total_cc += float(line_array[0])
                        total_count += int(line_array[1])
                if int(total_count) > 0:
                    all_file_avg_cc = '{:.3f}'.format(float(total_cc / total_count))
        # print(util.get_datetime()+" avg files cc count: "+str(all_file_avg_cc))
        post_param = {"stream_name": stream, "task_id": task_id, "averageCCN": str(all_file_avg_cc)}
        jdata = json.dumps(post_param)
        conn = get_conn()
        conn.request("POST", "/ms/defect/api/build/defects/statistic/ccn", jdata, headers)
        response = conn.getresponse()
        data = response.read()
        # print("return data: " + data)
    except Exception as e:
        raise Exception(e)

    return status


def upload_project_dupc_summary(summary_json):
    headers = {"Content-type": "application/json", "x-devops-build-id": config.params_root['pipelineBuildId'],
               "x-devops-vm-sid": config.params_root['DEVOPS_AGENT_VM_SID'],
               "x-devops-project-id": config.params_root['DEVOPS_PROJECT_ID'],
               "x-devops-build-type": config.params_root['DEVOPS_BUILD_TYPE'],
               "x-devops-agent-id": config.params_root['DEVOPS_AGENT_ID'],
               "x-devops-agent-secret-key": config.params_root['DEVOPS_AGENT_SECRET_KEY']}
    try:
        conn = get_conn()
        conn.request("POST", "/ms/defect/api/build/defects/statistic/dupc", summary_json, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
    # if status:
    #    print(util.get_datetime()+" summary_json upload data to codecc successful!")
    # else:
    #    print(util.get_datetime()+" summary_json upload data to codecc failed!")
    except Exception as e:
        raise Exception(e)


def upload_goml_project_dir_struct_checker(tool_type, dir_checker, go_build_status):
    status = False
    headers = {"Content-type": "application/json", "x-devops-build-id": config.params_root['pipelineBuildId'],
               "x-devops-vm-sid": config.params_root['DEVOPS_AGENT_VM_SID'],
               "x-devops-project-id": config.params_root['DEVOPS_PROJECT_ID'],
               "x-devops-build-type": config.params_root['DEVOPS_BUILD_TYPE'],
               "x-devops-agent-id": config.params_root['DEVOPS_AGENT_ID'],
               "x-devops-agent-secret-key": config.params_root['DEVOPS_AGENT_SECRET_KEY']}
    try:
        conn = get_conn()
        conn.request("POST", "/ms/defect/api/build/tasklog/suggest/param")
        post_param = {"taskId": config.params_root['taskId'], "toolName": tool_type,
                      "dirStructSuggestParam": dir_checker, "compileResult": go_build_status}
        jdata = json.dumps(post_param)
        response = conn.getresponse()
        data = response.read()
        data_array = json.loads(str(data.decode()))
        status = data_array["data"] == str(True)
    except Exception as e:
        raise Exception(e)

    return status


def codecc_get_proj_language(proj_id):
    headers = {"Content-type": "application/json", "x-devops-build-id": config.params_root['pipelineBuildId'],
               "x-devops-vm-sid": config.params_root['DEVOPS_AGENT_VM_SID'],
               "x-devops-project-id": config.params_root['DEVOPS_PROJECT_ID'],
               "x-devops-build-type": config.params_root['DEVOPS_BUILD_TYPE'],
               "x-devops-agent-id": config.params_root['DEVOPS_AGENT_ID'],
               "x-devops-agent-secret-key": config.params_root['DEVOPS_AGENT_SECRET_KEY']}
    code_lang = '1'
    try:
        conn = get_conn()
        conn.request("GET", "/ms/task/api/build/task/taskId/" + str(proj_id), {}, headers)
        response = conn.getresponse()
        data = response.read()
        data_array = json.loads(str(data.decode()))
        if "codeLang" in data_array["data"]:
            code_lang = data_array["data"]["codeLang"]
            print(code_lang)
    except Exception as e:
        raise Exception(e)
    return code_lang
