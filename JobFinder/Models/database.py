import json
from JobFinder.Models.job import Job
import numpy as np, scipy.stats as st

class Database:

	def __init__(self, source):
		self.data = dict()
		with open(source, 'r') as f:
			for line in f:
				jl = Job(line)
				self.data[jl.id] = jl

	def get_job_from_id(self, id):
		if id in self.data.keys():
			return self.data[id]
		else:
			return None

	def get_jobs_from_ids(self, id_list):
		result = []
		for id in id_list:
			result.append(self.data[id])
		return [jl.__dict__ for jl in result]

	def get_jobs_in_region(self, region_code):
		return [jl.__dict__ for jl in self.data.values() if jl.region_code == region_code]

	def get_all_jobs(self):
		return [jl.__dict__ for jl in self.data.values()]

	def get_jobs(self):
		return self.data

	def pr(self):
		for k, v in self.data.iteritems():
			print(v.to_json())