import os

def get_result_file_path(stream_result_path,filename):
    try:
        filename_result=stream_result_path+'/'+filename.replace(':', '').replace('\\', '/')
        filename_dir=os.path.dirname(filename_result)
        if not os.path.exists(filename_dir):
            os.makedirs(filename_dir)
    except Exception as e:
        raise Exception(e)
    finally:
        return filename_result