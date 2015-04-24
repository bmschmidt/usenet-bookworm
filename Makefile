

bookworm:
	git clone git@github.com:bmschmidt/Presidio $@
	$(MAKE) -C bookworm

input.txt:
	python parse.py

utzoo-wiseman-usenet-archive.zip:
	wget https://archive.org/compress/utzoo-wiseman-usenet-archive/formats=GZIPPED%20TAR&file=/utzoo-wiseman-usenet-archive.zip
	mv "formats=GZIPPED TAR" $@

