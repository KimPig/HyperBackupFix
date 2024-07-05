import os
import re
import argparse
import logging

def setup_logging(log_dir, root_directory):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    base_name = os.path.basename(root_directory)
    log_file_name = f"{base_name}.log"
    log_file_path = os.path.join(log_dir, log_file_name)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )

def get_file_size(file_path):
    return os.path.getsize(file_path)

def find_duplicates(files):
    file_dict = {}
    pattern_with_ext = re.compile(r'^(.*) \((\d+)\)(\.\w+)$')
    pattern_without_ext = re.compile(r'^(.*) \((\d+)\)$')

    for file in files:
        match_with_ext = pattern_with_ext.match(file)
        match_without_ext = pattern_without_ext.match(file)
        if match_with_ext:
            base_name, num, ext = match_with_ext.groups()
            original_name = f"{base_name}{ext}"
            if original_name not in file_dict:
                file_dict[original_name] = []
            file_dict[original_name].append(file)
        elif match_without_ext:
            base_name, num = match_without_ext.groups()
            original_name = base_name
            if original_name not in file_dict:
                file_dict[original_name] = []
            file_dict[original_name].append(file)
    
    return file_dict

def process_files(directory):
    logging.info(f"Processing directory: {directory}")
    files = os.listdir(directory)
    duplicates = find_duplicates(files)

    for original_file in duplicates:
        original_path = os.path.join(directory, original_file)
        if os.path.exists(original_path):
            max_file = original_path
            max_size = get_file_size(original_path)

            for dup_file in duplicates[original_file]:
                dup_path = os.path.join(directory, dup_file)
                dup_size = get_file_size(dup_path)

                if dup_size > max_size:
                    max_file = dup_path
                    max_size = dup_size
            
            # Remove all other duplicates
            for dup_file in duplicates[original_file]:
                dup_path = os.path.join(directory, dup_file)
                if dup_path != max_file:
                    os.remove(dup_path)
                    logging.info(f"Removed: {dup_path}")
            
            if max_file != original_path:
                os.remove(original_path)
                os.rename(max_file, original_path)
                logging.info(f"Renamed: {max_file} to {original_path}")

def main(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        process_files(dirpath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Duplicate file cleaner")
    parser.add_argument("root_directory", help="Root directory to start cleaning from")
    args = parser.parse_args()
    
    log_directory = os.path.join(os.path.dirname(__file__), 'logs')
    setup_logging(log_directory, args.root_directory)
    
    try:
        main(args.root_directory)
        logging.info("Cleanup completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
