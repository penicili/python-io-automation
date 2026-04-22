"""
1. File System I/O
Study Case: Log Analyzer & Rotator
Konteks: Log apache di /var/log/apache2/access.log
Perintah:
- Analisa log, hitung jumlah error, warning dan info
- Report dalam bentuk JSON
- Archive log ke /archive/*.log.gz
- Hapus Archive 
"""
import pathlib
import json
import shutil
import gzip
from datetime import datetime

# Paths
log_path = pathlib.Path("/var/log/apache2/access.log")
report_path = pathlib.Path("report.json")
archive_dir = pathlib.Path("/archive")

# Vars
archived_log_age = 7 # days


def read_log(log_path):
    with log_path.open() as f:
        return f.readlines()

def analyze_log(log_lines):
    report = {
        "error": 0,
        "warning": 0,
        "info": 0
    }
    for line in log_lines:
        if "error" in line.lower():
            report["error"] += 1
        elif "warning" in line.lower():
            report["warning"] += 1
        elif "info" in line.lower():
            report["info"] += 1
    return json.dumps(report, indent=4)

def parse_line_time(line):
    # contoh baris log
    # [Sun Dec 04 04:51:18 2005] [error] mod_jk child workerEnv in error state 6
    # ambil bagian di dalem []
    time_str = line.split("]")[0].strip("[")
    # parse ke datetime 
    return datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
    

def archive_log(log_lines, archive_dir, days):
    # Cek umur log
    archived_log = []
    kept_lines = []
    for i in log_lines:
        log_time = parse_line_time(i)
        if (datetime.now() - log_time).days > days:
            # Archive log
            archived_log.append(i)
        else:
            kept_lines.append(i)
    if archived_log:
        # Current date as archive name
        archive_filename = archive_dir / f'access_{datetime.now().strftime("%Y%m%d")}.log.gz'
        
        with gzip.open(archive_filename, "wt") as f:
            f.writelines(archived_log)
        # hapus baris log yang udah dimasukin di archive
        with log_path.open("w") as f:
            f.writelines(kept_lines)
            
            
def main():
    print ("Log archiver & analyzer")
    print ("==========================")
    print (f"reading log from {log_path}")
    log_lines = read_log(log_path)
    
    print ("Analyzing log...")
    report = analyze_log(log_lines)
    print ("Report:")
    print (report)
    
    print (f'Saving report to {report_path} as JSON')
    with report_path.open("w") as f:
        f.write(report)
    print (f'Archiving logs to {archive_dir}')
    archive_log(log_lines, archive_dir, archived_log_age)
    

if __name__ == "__main__":
    main()