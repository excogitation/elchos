import requests, ftputil, ftplib, os, pprint, threading, time, random

class FTP_Crawler:
	class MyFTPSession(ftplib.FTP):
		def __init__(self, host, userid, password, port):
		    """Act like ftplib.FTP's constructor but connect to another port."""
		    ftplib.FTP.__init__(self)
		    self.connect(host, port)
		    self.login(userid, password)

	def crawl_directory(self, ftp, directory):
		if directory != ".": ftp.chdir(directory) #Decend into directory
		current_path = ftp.getcwd() if directory != "." else ""
		names = ftp.listdir(ftp.curdir)
		
		for name in names:
			if not ftp.path.isfile(name):
				#Only create a new folder if we dont have it already
				folderlist = list(filter(lambda x: x["type"] == "folder", self.content_list)) #Get all content of type folder
				same_folders = list(filter(lambda x: x["path"] == current_path and x["name"] == name, folderlist))
				if len(same_folders) == 0: #This is a new, unknown dictionary				
					self.content_list.append({
						"type": "folder", 
						"nodes": [self.HOST if self.PORT==21 else self.HOST+":"+str(self.PORT)], #Create the hosting nodes array with the first entry 						
						"path": current_path, 
						"name": name
					})
				elif len(same_folders) == 1: #We already have this folder, just missing this node
					folder_index = self.content_list.index(same_folders[0]) #Get index of that folder
					self.content_list[folder_index]["nodes"].append(self.HOST if self.PORT==21 else self.HOST+":"+str(self.PORT)) #Append that node as hoster of this folder
					
				self.crawl_directory(ftp, name)
			else:
				#Only create new file node if we know it already
				filelist = list(filter(lambda x: x["type"] == "file", self.content_list)) #Get all content of type file
				same_files = list(filter(lambda x: x["size"] == ftp.stat(name).st_size and x["path"] == current_path and x["name"] == name, filelist)) #File has same size, path and name
				if len(same_files) == 0: #This is a new, unknown file
					self.content_list.append({
						"type": "file", 
						"size": ftp.stat(name).st_size, 
						"nodes": [self.HOST if self.PORT==21 else self.HOST+":"+str(self.PORT)], #Create the hosting nodes array with this as first entry
						"path": current_path, 
						"name": name
					})
				elif len(same_files) == 1: #We have the same file somewhere else
					file_index = self.content_list.index(same_files[0])
					self.content_list[file_index]["nodes"].append(self.HOST if self.PORT==21 else self.HOST+":"+str(self.PORT)) #Add this hosting nodefor that file
		
		ftp.chdir(ftp.pardir) #Go back to the parent directory

	def crawl(self):
		self.crawl_directory(self.ftp, self.ftp.curdir)
		return self.content_list

	def __init__(self, HOST, PORT, content_list):
		self.HOST = HOST
		self.PORT = PORT
		self.ftp = ftputil.FTPHost(HOST, "guest", "guest", port=PORT, session_factory=self.MyFTPSession)
		self.content_list = content_list
