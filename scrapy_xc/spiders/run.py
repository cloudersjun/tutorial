from scrapy import cmdline
name = "dmoz"
cmd = "scrapy crawl {0}".format(name)
cmdline.execute(cmd.split())