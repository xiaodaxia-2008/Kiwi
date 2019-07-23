import difflib
import sys
import os

htm_diff = difflib.HtmlDiff(tabsize=4, wrapcolumn=130)
if len(sys.argv) != 3:
    print("Incorrect args, should be: python3 text_diff.py file1 file2")
    sys.exit()
file1 = sys.argv[1]
file2 = sys.argv[2]

with open(file1, "r") as f:
    f1 = f.readlines()
with open(file2, "r") as f:
    f2 = f.readlines()

savefile = os.path.join(os.getcwd(), "diff.html")

with open(savefile, 'w') as f:
    f.write(htm_diff.make_file(f1, f2))
print("Successfully generated diff file: %s" % savefile)
