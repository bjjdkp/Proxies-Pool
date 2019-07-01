# --*-- coding:utf-8 --*--

import gc
import sys
import getopt
from db import init_source_ips
from checkips import port_scan

"""

    按实际流程顺序

单次运行
1. 下载 apnic 文件， 根据文件生成源ip   -s
2. 使用 nmap 扫描指定端口   -n
3. 扫描结果验证，保存结果      -c


实时维护，以接口形式开放
#  以年为周期更新所有源ip ， 暂时不考虑
4. 开放api，并根据结果引入代理评分机制，持续更新代理池  -u

all 顺序执行以上所有操作    -a
"""

"""
代理池启动函数
"""


def _get_commands_list():
    return [
        ("-s", "Download ip file from apnic,generate all ips"),
        ("-n", "scan by nmap"),
        ("-c", "check proxy for scan result"),
        ("-u", "open api for proxy check result"),
        ("-a", "execute all commands in order"),
    ]


def _print_commands():
    print("Usage:")
    print("   python proxy_pool.py [options]\n")
    print("Available options:")
    cmds = _get_commands_list()
    for cmdname, cmddesc in cmds:
        print("  %-13s %s" % (cmdname, cmddesc))


def _print_unknown_command(cmdname=None):
    if cmdname:
        print(cmdname)
    print('Use "-h" to see available options')


def execute(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        opts, args = getopt.getopt(argv[1:], "sncuah", ["source", "nmap",
                                                        "check", "use",
                                                        "all", "help"])
    except getopt.error as msg:
        _print_unknown_command(msg)
        sys.exit(2)
    else:
        if len(args):
            _print_unknown_command("Unknown command: %s\n" % args[0])
            sys.exit(2)

    for o, a in opts:
        if o in ("-s", "--source"):
            init_source_ips.init_source_ips()

        elif o in ("-n", "--nmap"):
            port_scan.PortScan().run()

        elif o in ("-c", "--check"):
            pass

        elif o in ("-u", "--use"):
            pass

        elif o in ("-a", "--all"):
            pass

        elif o in ("-h", "--help"):
            _print_commands()
            sys.exit(0)


if __name__ == "__main__":
    try:
        execute()
    finally:
        gc.collect()



