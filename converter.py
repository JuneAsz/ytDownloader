import ffmpy
import os

def convert(file_name: str, file_output: str):
    ff = ffmpy.FFmpeg(inputs={file_name: None}, outputs={file_output: None})
    ff.run()
    print("CONVERT COMPLETE ============================")
    print(file_name)
    os.remove(file_name)

