import curses
import dns.resolver
import time

def query_dns(hostname, dns_server):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    
    start_time = time.time()
    
    try:
        answers = resolver.resolve(hostname)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        ip_addresses = [answer.address for answer in answers]
        return f"{hostname} (@{dns_server}): {', '.join(ip_addresses)} [took {elapsed_time:.4f}s]"  # noqa: E501
    except dns.resolver.NXDOMAIN:
        return f"{hostname} @ {dns_server} NXDOMAIN"

def draw_input_box(stdscr, text, y, x, width):
    stdscr.addch(y, x, '+')
    stdscr.addch(y, x + width, '+')
    stdscr.addch(y + 2, x, '+')
    stdscr.addch(y + 2, x + width, '+')
    
    stdscr.addstr(y + 1, x + 2, text)
    stdscr.hline(y, x + 1, '-', width - 1)
    stdscr.hline(y + 2, x + 1, '-', width - 1)

def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    input_box_width = 50
    input_box_x = width // 2 - input_box_width // 2
    input_box_y = height // 2 - 1

    draw_input_box(stdscr, "Enter your hostname:", input_box_y, input_box_x, input_box_width)  # noqa: E501
    stdscr.refresh()

    curses.echo()
    hostname_prompt_length = len("Enter your hostname: ")
    hostname = stdscr.getstr(input_box_y + 1, input_box_x + hostname_prompt_length + 2, input_box_width - hostname_prompt_length - 2).decode()  # noqa: E501
    curses.noecho() 

    dns_servers = ['1.1.1.1', '8.8.8.8', '9.9.9.9', '62.149.128.4']
    results = []

    for dns_server in dns_servers:
        result = query_dns(hostname, dns_server)
        results.append(result)

    stdscr.clear()
    curses.curs_set(0)
    y = height // 2 - len(results) // 2
    for result in results:
        x = width // 2 - len(result) // 2
        stdscr.addstr(y, x, result)
        y += 1

    stdscr.addstr(height - 2, width // 2 - 18, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
