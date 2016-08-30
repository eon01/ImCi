from ImCi.imci import Check

check = Check()
urls = check.download()
scan = check.check_size(urls)
print (check.validate(scan))

