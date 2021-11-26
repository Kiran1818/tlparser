import re
import sys
import base64
import streamlit as st

def getTimeLog(line):
	filename = sys.argv[1]

	report = []
	timeList = []
	flag = False
	count = 1
	totalDiff = 0

	def isCorrect(tempTime):
		first = ""
		second = ""
		if "am" in tempTime:
			first = tempTime.split(" - ")[0].split("am")[0]
			second = tempTime.split(" - ")[1].split("am")[0]
		else:
			first = tempTime.split(" - ")[0].split("pm")[0]
			second = tempTime.split(" - ")[1].split("pm")[0] 

		first_h = int(first.split(":")[0])
		if first_h == 12:
			first_h = 0
		first_m = int(first.split(":")[1])
		second_h = int(second.split(":")[0])
		if second_h == 12:
			second_h = 0
		second_m = int(second.split(":")[1])

		timeDiff = (second_h  * 60 + second_m) - (first_h  * 60 + first_m)
		return timeDiff

	def isCorrectPMAM(tempTime):
		first = tempTime.split(" - ")[0].split("pm")[0]
		second = tempTime.split(" - ")[1].split("am")[0]

		first_h = int(first.split(":")[0])
		first_m = int(first.split(":")[1])
		second_h = int(second.split(":")[0])
		if second_h < 12:
			second_h += 12
		second_m = int(second.split(":")[1])
		timeDiff = (second_h  * 60 + second_m) - (first_h  * 60 + first_m)
		return timeDiff

	def isCorrectAMPM(tempTime):
		first = tempTime.split(" - ")[0].split("am")[0]
		second = tempTime.split(" - ")[1].split("pm")[0]
		first_h = int(first.split(":")[0])
		first_m = int(first.split(":")[1])
		second_h = int(second.split(":")[0])
		if second_h != 12:
			second_h += 12
		second_m = int(second.split(":")[1])
		timeDiff = (second_h  * 60 + second_m) - (first_h  * 60 + first_m)
		return timeDiff

	for temp in line:
		flagCor = False
		if flag:
			if re.findall(r"\d+:\d+am - \d+:\d+am", temp.lower()):
				tempTime = re.findall(r"\d+:\d+am - \d+:\d+am", temp.lower())
				if isCorrect(tempTime[0]) >= 0:
					timeList.append(tempTime[0])
					totalDiff += isCorrect(tempTime[0])
				else:
					report.append(count)
			elif re.findall(r"\d+:\d+am - \d+:\d+pm", temp.lower()):
				tempTime = re.findall(r"\d+:\d+am - \d+:\d+pm", temp.lower())
				totalDiff += isCorrectAMPM(tempTime[0])
				timeList.append(tempTime[0])
			elif re.findall(r"\d+:\d+pm - \d+:\d+pm", temp.lower()):
				tempTime = re.findall(r"\d+:\d+pm - \d+:\d+pm", temp.lower())
				if isCorrect(tempTime[0]) >= 0:
					timeList.append(tempTime[0])
					totalDiff += isCorrect(tempTime[0])
				else:
					report.append(count)
			elif re.findall(r"\d+:\d+pm - \d+:\d+am", temp.lower()):
				tempTime = re.findall(r"\d+:\d+pm - \d+:\d+am", temp.lower())
				totalDiff += isCorrectPMAM(tempTime[0])
				timeList.append(tempTime[0])
			else:
				report.append(count)
		else:
			if "Time Log" in temp:
				flag = True
		count += 1

	print(totalDiff)
	print("Total Period: " + str(totalDiff // 60) + "h " + str(totalDiff % 60) + "m")
	for temp in report:
		print(str(temp) + " line has some thing error")

if __name__ == "__main__":
		# read file
	st.title("Webpage for TimeLog Parser")
	background = "background.jpg"
	background_ext = "jpg"
	st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{background_ext};base64,{base64.b64encode(open(background, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
	with st.expander("data upload"):
		docx_file = st.file_uploader("Upload File",type=['txt','docx','pdf'])
		if st.button("Process"):
			if docx_file is not None:
				file_details = {"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
				st.write(file_details)
				# Check File Type
				if docx_file.type == "text/plain":
					line = str(docx_file.read(),"utf-8")
					getTimeLog(line)
