
number_version = (0, 0, 1)
string_version = '.'.join([str(num) for num in number_version])

dev_version = "1"
if dev_version:
    version = string_version + '-dev' + dev_version
else:
    version = string_version
