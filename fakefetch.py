#!/usr/bin/python3
#  _    __ _             
# | |  /_ | |            
# | |__ | | |_ ___ _ __  
# | '_ \| | __/ _ \ '_ \ 
# | |_) | | ||  __/ | | |
# |_.__/|_|\__\___|_| |_|
#                        
# 
# by 81+3|\|
# ---------------------------------------    

##imports
import os, platform, subprocess
import datetime, argparse
import distro_art


def parse_arguments():
    parser = argparse.ArgumentParser(description="Copy of Neofetch written in python")
    parser.add_argument("-d", "--distro", metavar="distro_name", default="arch", help="Change ascii art.")
    return parser.parse_args()


def get_os_info():
    try:
        os_inf = os.uname()
        return f" {os_inf.sysname} {os_inf.release} {os_inf.machine}"
    except Exception as e:
        return f' cannot be retrived: {e}'


def get_host_info():
    try:
        host_inf = platform.node()
        return f" {host_inf}"
    except Exception as e:
        return f' cannot be retrived: {e}'


def get_kernel_info():
    try:
        kernel_inf = platform.uname().release
        return f" {kernel_inf}"
    except Exception as e:
        return f' cannot be retrived: {e}'


def get_uptime():
    try:
        uptime_output = subprocess.check_output(['uptime', '-s']).decode('utf-8').strip()
        uptime_start_time = datetime.datetime.strptime(uptime_output, '%Y-%m-%d %H:%M:%S')

        uptime_duration = datetime.datetime.now() - uptime_start_time

        days = uptime_duration.days
        hours, remainder = divmod(uptime_duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        return f" {days}d {hours}h {minutes}m"
    except Exception as e:
        return f" cannot be retrieved: {e}"


def get_pkg_count():
    pkg_managers = []

    try:
        subprocess.check_output(['apt', '--version'])
        pkg_managers.append('apt')
    except FileNotFoundError:
        pass

    try:
        subprocess.check_output(['pacman', '--version'])
        pkg_managers.append('pacman')
    except FileNotFoundError:
        pass

    try:
        subprocess.check_output(['yay', '--version'])
        pkg_managers.append('yay')
    except FileNotFoundError:
        pass

    if not pkg_managers:
        return " Unknown package manager"

    try:
        total_pkg_count = 0

        for pkg_manager in pkg_managers:
            if pkg_manager == 'apt':
                pkg_count = int(subprocess.check_output(['dpkg', '--get-selections']).decode('utf-8').strip().count('\n'))
            elif pkg_manager == 'pacman':
                pkg_count = int(subprocess.check_output(['pacman', '-Qq']).decode('utf-8').strip().count('\n'))
            elif pkg_manager == 'yay':
                pkg_count = int(subprocess.check_output(['yay', '-Qq']).decode('utf-8').strip().count('\n'))
            else:
                pkg_count = 0

            total_pkg_count += pkg_count

        return f" {total_pkg_count} ({', '.join(pkg_managers)})"

    except Exception as e:
        return f' cannot be retrieved: {e}'


def get_shell_info():
    try:
        shell_inf = os.path.basename(os.environ['SHELL'])
        return f" {shell_inf}"
    except Exception as e:
        return f' cannot be retrived: {e}'

def get_terminal_info():
    try:
        terminal_inf = os.ttyname(0)
        return f" {terminal_inf}"
    except Exception as e:
        return f' cannot be retrived: {e}'


def get_cpu_info():
    try:
        cpu_inf = subprocess.check_output(['lscpu']).decode("UTF-8")
        return f" {cpu_inf.splitlines()[7].split(':')[1].strip()}"
    except Exception as e:
        return f' cannot be retrived: {e}'


def get_memory_info():
    try:
        memory_inf = subprocess.check_output(['free','-m']).decode("UTF-8")
        lines = memory_inf.splitlines()
        mem_tot = int(lines[1].split()[1])
        mem_use = int(lines[2].split()[2])
        return f" {mem_use} MiB / {mem_tot} MiB"
    except Exception as e:
        return f' cannot be retrived: {e}'


def get_distro_art(distro_name):
    distro_entry = distro_art.distro_art.get(distro_name, distro_art.distro_art["default"])
    art = distro_entry["art"]
    color_code = distro_entry.get("color", "")
    colored_art = "\n".join([f"{color_code}{line}\033[0m" for line in art.splitlines()])
    return colored_art

    
def get_distro_info(distro_name):
    distro_entry = distro_art.distro_art.get(distro_name, distro_art.distro_art["default"])
    color_code = distro_entry.get("color", "")

    info = f"""
{color_code}{os.getlogin()}\033[0m\033[1;37m@\033[0m{color_code}{platform.node()}\033[0m
\033[1;37m---------------\033[0m
{color_code}OS\033[0m\033[1;37m:\033[0m{get_os_info()}
{color_code}Hostname\033[0m\033[1;37m:\033[0m{get_host_info()}
{color_code}Kernel\033[0m\033[1;37m:\033[0m{get_kernel_info()}
{color_code}Uptime\033[0m\033[1;37m:\033[0m{get_uptime()}
{color_code}Packages\033[0m\033[1;37m:\033[0m{get_pkg_count()}
{color_code}Shell\033[0m\033[1;37m:\033[0m{get_shell_info()}
{color_code}Terminal\033[0m\033[1;37m:\033[0m{get_terminal_info()}
{color_code}CPU\033[0m\033[1;37m:\033[0m{get_cpu_info()}
{color_code}Memory\033[0m\033[1;37m:\033[0m{get_memory_info()}

\033[1;41m   \033[0m\033[1;42m   \033[0m\033[1;43m   \033[0m\033[1;44m   \033[0m\033[1;45m   \033[0m\033[1;46m   \033[0m\033[1;47m   \033[0m
"""
    return info


def get_result(distro_name="arch"):
    art_lines = get_distro_art(distro_name).splitlines()
    info_lines = get_distro_info(distro_name).splitlines()

    max_art_width = max(len(line) for line in art_lines)

    output_lines = [
        f"{art_lines[i]:<{max_art_width + 2}} {info_lines[i]}" if i < len(info_lines) else art_lines[i]
        for i in range(len(art_lines))
    ]

    return "\n".join(output_lines)

if __name__ == "__main__":
    args = parse_arguments()

    print(get_result(args.distro))

#love from 81+3|\| <3
