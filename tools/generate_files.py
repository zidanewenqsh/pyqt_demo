import os

def generate_files(prefix: str, number_range: tuple, suffix: str, save_path: str):
    """
    Generate a set of empty files with specified prefix, number range, and suffix, saved in the given path.
    
    Args:
        prefix (str): The prefix for the file names.
        number_range (tuple): A tuple of two integers specifying the start and end of the number range (inclusive).
        suffix (str): The file extension (e.g., '.txt').
        save_path (str): The directory where the files will be created.
    """
    # Ensure the save path exists
    os.makedirs(save_path, exist_ok=True)
    
    # Generate files within the range
    for i in range(number_range[0], number_range[1] + 1):
        # Construct file name
        file_name = f"{prefix}{i}{suffix}"
        file_path = os.path.join(save_path, file_name)
        if os.path.exists(file_path):
            print(f"File '{file_name}' already exists in '{save_path}'.")
            continue 
        # Create an empty file
        with open(file_path, 'w') as f:
            pass  # Just create the file, no content written

    print(f"Generated {number_range[1] - number_range[0] + 1} files in '{save_path}'.")

# 示例使用
if __name__ == "__main__":
    generate_files(
        prefix="wanlh",
        number_range=(10, 32),
        suffix=".py",
        save_path="./"
    )
