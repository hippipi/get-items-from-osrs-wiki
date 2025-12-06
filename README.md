# get-items-from-osrs-wiki
A small tool to get an updated item list from wiki and filter out silly stuff

## get_items_from_wiki.py
- Uses a generator to request batches of up to 500 results from OSRS wiki with request parameters
- Results are from the category 'Category:Items' - can be customised if you wish
- All results are written to 'items_results.txt'
- Regex pattern is loaded from 'items_filters.txt'
- Filtered results (using regex pattern) are written to 'items_filtered.txt'

### get_all_items()
- Fetches all item pages from the OSRS wiki
- Takes about 18 seconds to run on my PC (fetching ~12,000 items - December 2025)

### refine_items()
- Filters 'items_results.txt' using 'items_filters.txt' loaded as a single regex pattern
- Edit 'items_filters.txt' if you want to add/remove/change filters
- Otherwise comment out this function if not wanting to filter results or have no filters text file
- Takes about 0.5 seconds to run on my PC

## Get pages from other categories
I've made it easy to swap which category you want to get results from:
- Change 'category_name' to the category - find a category from https://oldschool.runescape.wiki/w/Special:Categories
- If wanting to filter results, ensure you create your own filter file named '<category_name>_filters.txt'

*For example, if the category is 'Non-player_characters' ensure you have a filter for 'Non-player_characters_filters.txt' if wanting to filter those results - otherwise comment out the `refine_items()` function*