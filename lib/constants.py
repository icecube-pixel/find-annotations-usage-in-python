from string import Template

_github_base_url = "https://api.github.com/search/repositories?q="
_language = "python"
_query_str = Template("python language:$lang&sort=stars&order=desc&page=$PAGE&per_page=$PER_PAGE")
sleep_counter = 1 # 1 sec