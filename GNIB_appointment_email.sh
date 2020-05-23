/bin/bash /home/dineshr/GNIB.sh > /tmp/GNIB_Approintments.txt

GNIB_File_Count=`cat /tmp/GNIB_Approintments.txt|grep -v "work appointments" | grep -v "No appointments available" |grep -v "August" | grep -v "July"|wc -l`

#GNIB_File_Count=`cat /tmp/GNIB_Approintments.txt|grep -v "work appointments" | grep -v "No appointments available"|wc -l`

if [ $GNIB_File_Count -gt 0 ]; then
mailx -r dineshr@xxxx.com -s "GNIB Available - Go and Book immediately for -- `cat /tmp/GNIB_Approintments.txt|tail -1`" dineshr@xxxxx.com < /tmp/GNIB_Approintments.txt
fi
