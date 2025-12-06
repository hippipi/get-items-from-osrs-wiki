import requests
import re

# Function (mostly) taken from https://www.mediawiki.org/wiki/API:Continue#Examples (Example 3)
def query(request: dict, category: str) -> None:
	request['action'] = 'query'
	request['format'] = 'json'
	request['list'] = 'categorymembers'
	request['cmtitle'] = category
	request['cmtype'] = 'page'
	request['cmlimit'] = '500'
	last_continue = {}
	while True:
		# Clone original request
		req = request.copy()
		# Modify it with the values returned in the 'continue' section of the last result
		req.update(last_continue)
		# Call API
		result = requests.get('https://oldschool.runescape.wiki/api.php?', params = req).json()
		if 'error' in result:
			raise Exception(result['error'])
		if 'warnings' in result:
			print(result['warnings'])
		if 'query' in result:
			yield result['query']
		if 'continue' not in result:
			break
		last_continue = result['continue']

# Fetch items from wiki with generator and write to file
def get_all_items(fname_results: str = 'items_results.txt', category: str = 'Category:Items') -> None:
	# Delete file contents
	with open(fname_results, 'w') as file:
		file.write('')
	# Write new file contents - takes ~18 seconds for 12k items (December 2025)
	with open(fname_results, 'a') as file:
		for result in query(request = {'generator': 'allpages'}, category = category):
			try:
				for page in result['categorymembers']:
					file.write(f"{page['title']}\n")
					# Remove print debug if annoying - but nice to show progress
					print(f"{page['title']}")
			except KeyError as e:
				break
	print('Finished fetching from wiki!')

# Filter items using regex filter from file
def refine_items(
	fname_results: str = 'items_results.txt',
	fname_filters: str = 'items_filters.txt',
	fname_filtered_results: str = 'items_filtered.txt'
	) -> None:
	# Get regex pattern to match against item names
	patterns = []
	with open(fname_filters, 'r') as file:
		for line in file.read().splitlines():
			patterns.append(line.lower())
	pattern = "|".join(patterns)
	# Go through items and filter out items that match regex pattern
	data = []
	with open(fname_results, 'r') as file:
		for line in file.read().splitlines():
			matched = True if re.search(pattern, line.lower()) else False
			if not matched: data.append(line)
	# Write new file of filtered results
	with open(fname_filtered_results, 'w') as file:
		file.write('\n'.join(data))
	print('Finished filtering results!')

if __name__ == '__main__':
	# Category - find name from 'https://oldschool.runescape.wiki/w/Special:Categories'
	category_name = "Items".replace(' ','_') # 'Items' category is the original project
	category = f'Category:{category_name}'
	# Filenames
	results_file = f'{category_name.lower()}_results.txt'
	filters_file = f'{category_name.lower()}_filters.txt' # ensure there is a file named this!
	filtered_file = f'{category_name.lower()}_filtered.txt'

	# Fetch updated list of items and write to results_file
	get_all_items(results_file, category)

	# Filter results_file using filters_file and write to filtered_file
	refine_items(results_file, filters_file, filtered_file)