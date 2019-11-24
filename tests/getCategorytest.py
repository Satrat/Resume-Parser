from getCategory import *

# Tests

# software total phrase count -> 57
assert(softwareScore("resume") == 0.0)
assert(softwareScore("This is a resume") == 0.0)
assert(softwareScore("c") == (1.0/57))
assert(softwareScore("c c++ c#") == (3.0/57))

# engineeringScore array length -> 27
assert(engineeringScore("resume") == 0.0)
assert(engineeringScore("This is a resume") == 0.0)
assert(engineeringScore("chemical") == (1.0/27))
assert(engineeringScore("civil engineering build") == (3.0/27))

# financeScore array length -> 24
assert(financeScore("resume") == 0.0)
assert(financeScore("This is a resume") == 0.0)
assert(financeScore("powerpoint") == (1.0/24))
assert(financeScore("forecasting trend analysis team") == (3.0/24))

# managementScore array length -> 23
assert(managementScore("resume") == 0.0)
assert(managementScore("This is a resume") == 0.0)
assert(managementScore("evaluations") == (1.0/23))
assert(managementScore("operational development firing budget") == (3.0/23))

# mainCategoryAndScore
assert(mainCategoryAndScore("resume") == ('computer science',0.0))
assert(mainCategoryAndScore("This is a resume") == ('computer science',0.0))
assert(mainCategoryAndScore("powerpoint") == ('finance',(1.0/24)))
assert(mainCategoryAndScore("operational development c firing budget engineering") == ('business management',(3.0/23)))
assert(mainCategoryAndScore("sml c firing budget engineering") == ('business management',(2.0/23)))
assert(mainCategoryAndScore("build sml hiring engineering") == ('engineering',(2.0/27)))


