if True:
    print "Simple True matches work."


if False:
    pass
else:
    print "Else against a False test passes"


foo = False
var2 = 'a'

if foo:
    print "This should not print"
elif var2:
    print "Var2 does print: ", var2
else:
    print "Not on here"

var1 = var2 = False
if var1:
    print "Nope"
elif var2:
    print "Still no"
else:
    print "The else statement"

