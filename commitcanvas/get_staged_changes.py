import io
import pandas as pd
from commitcanvas.generate_type import commit_data as cm


def staged_stats(stats,file_names,commit_subject):

    decoded_diff = stats.decode('utf-8')
    decoded_files = file_names.decode('utf-8')
    stats_list = [int(s) for s in decoded_diff.split() if s.isdigit()]
    files_list = decoded_files.split("\n")

    added = stats_list[1]
    deleted = stats_list[2]
    file_extensions = cm.get_file_extensions(files_list)
    test_files_count = cm.test_files(files_list)


    staged_changes_stats = {
        'commit_subject': commit_subject,
        "num_files": stats_list[1],
        "test_files": test_files_count,
        "test_files_ratio": cm.get_ratio(test_files_count,files_list),
        "unique_file_extensions": file_extensions,
        "num_unique_file_extensions": len(file_extensions),
        "num_lines_added": added,
        "num_lines_removed": deleted,
        "num_lines_total": added + deleted,    
    }

    return (pd.DataFrame([staged_changes_stats]))