#! /bin/bash

case $1 in
	image_switch)
		curl -d 'aa' -o /dev/null -s -w %{http_code} http://aaaa
			;;
	exrate_ser)
		curl -o /dev/null -s -w %{http_code} http://ppp
			;;
esac
