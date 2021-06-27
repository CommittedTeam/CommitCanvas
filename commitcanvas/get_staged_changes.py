# pyright: reportMissingImports=false
import pandas as pd
from reporover import parse

# string1 = "1 file changed, 1 insertion(+), 1 deletion(-)"
# string2 = "1 file changed, 1 deletion(-)
def short_stat(decoded_diff):
    added = None
    deleted = None
    changes = decoded_diff.split(",")
    for i in changes:
        if ("+" in i):
            added = [int(s) for s in i.split() if s.isdigit()][0]
        if ("-" in i):
            deleted = [int(s) for s in i.split() if s.isdigit()][0]

    if (not added):
        added = 0
    if (not deleted):
        deleted = 0

    return (added,deleted)

def staged_stats(stats,file_names,commit_subject):

    decoded_diff = stats.decode('utf-8')
    added,deleted = short_stat(decoded_diff)

    decoded_files = file_names.decode('utf-8')
    files_list = decoded_files.split("\n")

    file_extensions = parse.get_file_extensions(files_list)
    test_files_count = parse.test_files(files_list)


    staged_changes_stats = {
        'commit_subject': commit_subject,
        "num_files": len(files_list),
        "test_files": test_files_count,
        "test_files_ratio": parse.get_ratio(test_files_count,files_list),
        "unique_file_extensions": file_extensions,
        "num_unique_file_extensions": len(file_extensions),
        "num_lines_added": added,
        "num_lines_removed": deleted,
        "num_lines_total": added + deleted,    
    }

    return (pd.DataFrame([staged_changes_stats]))