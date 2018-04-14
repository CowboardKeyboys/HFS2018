import json
import time
from dashboard.static.data.job_listing import job_listing
import numpy as np, scipy.stats as st

class database:

	def __init__(self, source):
		self.data = dict()
		with open(source, 'r') as f:
			for line in f:
				jl = job_listing(line)
				self.data[jl.id] = jl

	def get_job_from_id(self, id):
		if id in self.data.keys():
			return self.data[id].to_json()
		else:
			return ""

	def get_jobs_from_ids(self, id_list):
		result = []
		for id in id_list:
			result.append(self.data[id])
		return json.dumps([jl.__dict__ for jl in result])


	def get_jobs_in_region(self, region_code):
		return json.dumps([jl.__dict__ for jl in self.data.values() if jl.region_code == region_code])

	def get_all_jobs(self):
		return json.dumps([jl.__dict__ for jl in self.data.values()])

	def get_training_data(self):
		desc = []
		id = []
		a = [len(t.location_desc) for t in self.data.values()[:100:]]
		leftQ, rightQ = st.t.interval(0.99, len(a)-1, loc=np.mean(a), scale=st.sem(a))
		median = np.median(a)
		for line in self.data.values():
			if len(line.location_desc)>leftQ and len(line.location_desc)<rightQ:
				desc.append(line.location_desc)
				id.append(line.id)
		return desc, id

	def pr(self):
		for k, v in self.data.iteritems():
			print(v.to_json())



def test():
	db = database("100000.json")
	#print db.get_job_from_id('0017-482230').to_json()
	#print db.get_jobs_in_region('0883')
	#print db.get_all_jobs()
	#print db.get_jobs_from_ids(["0017-544186", "0017-627299", "0017-667999"])
	#print "data loaded."
	#time.sleep(20000)
	x,y = db.get_training_data()
	print(str(len(x)))
	print(str(len(y)))


if __name__ == "__main__":
	test()
