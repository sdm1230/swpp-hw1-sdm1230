from babyname_parser import BabynameParser
parser = BabynameParser("babydata", 2003)
"""
print(parser.year)
print(parser.filename)
print(parser.rank_to_names_tuples)
print(parser.parse(lambda rank_to_names_tuple: rank_to_names_tuple[2]))
"""
l=["kay","may","bi"]
m="ky"
if m in l:
    print(True)