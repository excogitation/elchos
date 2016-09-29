import requests, ftputil, ftplib, os, pprint, threading, time, random
from flask import Flask, render_template, request
from Crawler import FTP_Crawler

new_nodes = []
node_list = []
content_list = []

def node_manager():
	#Adds new nodes and removes nodes that timed out
	global new_nodes, content_list, node_list
	while True:
		for (HOST, PORT, ARRIVAL) in new_nodes:
			#Crawl this server
			print("Starting to crawl " + HOST)
			crawler = FTP_Crawler(HOST, PORT, content_list)
			content_list = crawler.crawl()
			print("Finished crawling " + HOST)
			new_nodes.remove((HOST, PORT, ARRIVAL)) #Remove the server from the new list
			node_list.append((HOST, PORT, ARRIVAL)) #Add the server to the known servers list

		for server in node_list: 
			if server[2]+300 <= time.time(): remove_node(server) #Remove timed out node
			
		time.sleep(2)
			
def remove_node(node):
	global node_list, content_list
	HOST = node[0]
	PORT = node[1]
	ARRIVAL = node[2]
	
	#Remove all content hosted by this nide
	host_string = HOST if PORT == 21 else HOST+":"+str(PORT) #Create the base string to search for
	for i, content in enumerate(content_list):
		if host_string in content["nodes"]: #Server was hosting this file/folder
			content_list[i]["nodes"].remove(host_string) #Remove us from the hosting list
			
	content_list = list(filter(lambda x: False if len(x["nodes"]) == 0 else True, content_list)) #Remove files served by nobody
		
	node_list.remove(node) #Remove the node itself
	print("Node " + HOST + " removed due to timeout")
	print(content_list)

#Start the node manager thread
node_manager_thread = threading.Thread(target=node_manager)
node_manager_thread.daemon = True
node_manager_thread.start()

#Start the HTTP server
app = Flask(__name__, static_folder="static")
@app.route("/favicon.ico")
def return_favicon(): return "" 

@app.route("/api/ping", methods=["POST"])
def register_node():
	global node_list, new_server
	r = request.get_json(force=True)
	node_host = r["IP"]
	node_port = r["PORT"]
	
	#Search for the server in the known servers
	for i in range(0, len(node_list)):
		if node_host == node_list[i][0] and node_port == node_list[i][1]: #We know this server already
			node_list[i] = (node_list[i][0], node_list[i][1], time.time())
			print("Server " + node_host + " is alive")
			return "success"
	
	#Search for the server in the uncrawled servers
	for i in range(0, len(new_nodes)):
		if node_host == new_nodes[i][0] and node_port == new_nodes[i][1]: #We know this server already
			new_nodes[i] = (new_nodes[i][0], new_nodes[i][1], time.time())
			print("Server " + node_host + " is alive")
			return "success"
	
	#We have not found the server, add and crawl it
	print("New node " + node_host)
	new_nodes.append((node_host, node_port, time.time()))
	return "success"

@app.route("/api/search", methods=["POST"])
def search_files():
	global node_list, content_list
	found_content = []
	print(request.form["searchterm"])
	search_term = request.form["searchterm"].replace(" ", "").strip().upper()
	if "<" in search_term or ">" in search_term or "/" in search_term: return "Nope" #XSS prevention
	for available_content in content_list:
		if search_term in available_content["name"].replace(" ", "").strip().upper(): found_content.append(available_content) #Append the file found
	return render_template(
		"listing.html", 
		content=found_content, 
		site_title="Search for " + request.form["searchterm"], 
		nodecount=len(node_list)
	)

@app.route("/", defaults={"path": ""}, methods=["GET"])
@app.route("/<path:path>", methods=["GET"])
def catch_all(path):
	global node_list, content_list
	folder_content = []
	path = "/" + path #Add a leading slash to the path requested
	if path[-1] == "/": path = path[:-1] #Remove a possible trailing slash
	print(path)
	for available_content in content_list:
		if available_content["path"] == path:
			random.shuffle(available_content["nodes"]) #Shuffle the source list (Load Distribution)
			print("Attaching " + str(available_content))
			folder_content.append(available_content)

	print("Files in " + path + ": " + str(folder_content))
	return render_template(
		"listing.html", 
		content=folder_content, 
		site_title="Listing of " + path if path!="" else "Welcome to elchOS (" + str(len(node_list)) + " nodes)", 
		nodecount=len(node_list)
	)
		
app.run(debug=True)

