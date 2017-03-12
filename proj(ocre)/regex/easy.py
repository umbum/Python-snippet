import re


pogrouping = re.compile(r"\b(\w+)\s+\1")
s = pogrouping.search("life is is wonderful")
print(s.group())



polookahead = re.compile("\w+(?=:)")
s2 = polookahead.search("https://naver.com/")
print(s2.group())

print("============")
po = re.compile("\w\w\w ")
s3 = po.finditer("asd dfew wt wet a  abd qwe cat pow law lamw")

print(next(s3).group())
print(next(s3).group())
