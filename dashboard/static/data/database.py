import json
from job_listing import job_listing

class database:

	def __init__(self, source):
		self.data = dict()
		with open(source, 'r') as f:
			for line in f:
				jl = job_listing(line)
				self.data[jl.id] = jl
				
	def get_job_from_id(self, id):
		if id in self.data.keys():
			return self.data[id]
		else:
			return ""
		
	def get_jobs_in_region(self, region_code):
		return json.dumps([jl.__dict__ for jl in self.data.values() if jl.region_code == region_code])
		
	def get_all_jobs(self):
		return json.dumps([jl.__dict__ for jl in self.data.values()])
				
	def pr(self):
		for k, v in self.data.iteritems():
			print v.to_json()
				
				
				
def test():
	db = database("200.json")
	#print db.get_job_from_id('0017-482230').to_json()
	#print db.get_jobs_in_region('0883')
	print db.get_all_jobs()
	
	
if __name__ == "__main__":
	test()
	

