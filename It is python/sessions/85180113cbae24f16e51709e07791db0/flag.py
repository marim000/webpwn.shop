import subprocess
def main():
	print(subprocess.run(args=["cat", './flag.txt'], capture_output=True, text=True))