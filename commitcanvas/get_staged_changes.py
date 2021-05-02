import io
import pandas as pd
from commitcanvas.generate_type import commit_data as cm

def staged_stats(diff,commit_subject):

    decoded_diff = diff.decode('utf-8')

    # convert to string output into pandas dataframe for easier calculations
    data = io.StringIO(decoded_diff)
    df = pd.read_csv(data, sep="\t",names = ["added","deleted","file_paths"])


    added = df.added.sum()
    deleted = df.deleted.sum()
    paths = df.file_paths.tolist()
    file_extensions = cm.get_file_extensions(paths)
    test_files_count = cm.test_files(paths)


    staged_changes_stats = {
        'commit_subject': commit_subject,
        "num_files": len(paths),
        "test_files": test_files_count,
        "test_files_ratio": cm.get_ratio(test_files_count,paths),
        "unique_file_extensions": file_extensions,
        "num_unique_file_extensions": len(file_extensions),
        "num_lines_added": added,
        "num_lines_removed": deleted,
        "num_lines_total": added + deleted,    
    }

    return (pd.DataFrame([staged_changes_stats]))