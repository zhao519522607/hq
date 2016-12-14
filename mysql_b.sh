#! /bin/bash

#while read line
#do
#   sed -i '1d' lst/$line.list
#done < list


while read line
do
  sed -i '/TABLE_NAME/d' time/$line.dt
done < list
