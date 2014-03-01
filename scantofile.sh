#! /bin/bash
set +o noclobber
#
#   $1 = scanner device
#   $2 = friendly name
#

#   
#       100,200,300,400,600
#
resolution=200
function=$1
user=$2
BASE=~/ownCloud/Scanner
mkdir -p $BASE
output_tmp=$BASE/$(date | sed s/' '/'_'/g | sed s/'\:'/'_'/g)

sleep  0.01

echo "Scan from $2($1)"
scanadf --resolution $resolution -x 212 -y 301 -o"$output_tmp"_%04d
for pnmfile in $(ls "$output_tmp"*)
do
   echo pnmtojpeg  "$pnmfile"  "$pnmfile".jpg
   pnmtojpeg --quality=85 "$pnmfile"  > "$pnmfile".jpg
   echo convert  "$pnmfile".jpg  "$pnmfile".pdf
   convert "$pnmfile".jpg "$pnmfile".pdf
   rm -f "$pnmfile"
   rm -f "$pnmfile".jpg
done

echo Merge $(ls "$output_tmp"*.pdf)
gs -q -sPAPERSIZE=a4 -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="$output_tmp".pdf $(ls "$output_tmp"*.pdf)



if [ "$1" == 'email' ]; then
  echo Send mail
  ./sendfile.py $1 $2 "$output_tmp".pdf
  rm "$output_tmp".pdf
fi



#cleanup

for psfile in $(ls "$output_tmp"_*.pdf)
do
   rm $psfile
done

echo Done!
