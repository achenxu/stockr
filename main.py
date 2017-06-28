import threading, sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from stockr.lib import utilities, bot

def main():
    task_file_name = sys.argv[1]
    script_dir = os.path.dirname(__file__)
    task_file_path = os.path.join(script_dir, 'sites/{}'.format(task_file_name))
    sites = []
    with open(task_file_path, 'r') as task_file:
        sites = task_file.readlines()
    sites = [site.strip() for site in sites]
    stockr_bot = bot.Stockr(proxy_file_name='proxies.txt')
    for site in sites:
        thread = threading.Thread(target=stockr_bot.run, args=(utilities.get_domain(site),))
        thread.start()

if __name__ == '__main__':
    main()