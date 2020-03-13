#!/usr/bin/python
# -*- coding: utf-8 -*-


def message_filter(category, message, tool_type, stream_info):
    if tool_type == 'cpplint':
        message = cpplint_filter(category, message, stream_info)
    return message

def cpplint_filter(category, message, stream_info):
    if "build/header_guard" in category:
        temp_msg = ''
        msg_list = []
        split_str = ''
        if 'ifndef' in message:
            msg_list = message.split('is:')
            split_str = 'is:'
        elif 'endif' in message:
            msg_list = message.split('//')
            split_str = '//'
        if len(msg_list) > 1:
            temp_msg = msg_list[0] + split_str
            msg_list_2 = msg_list[1].split('CPPLINT')
            if len(msg_list_2) > 1:
                if "LAST_URI_STR" in stream_info:
                    temp_msg += ' '+stream_info["LAST_URI_STR"].upper()+msg_list_2[1]
                message = temp_msg
    return message