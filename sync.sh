#!/bin/bash

root=$PWD
cd $1
git pull
cd $root

change=0

function sync {

	root=$PWD
	
	cd $1

	for i in *
	do

	 j=$root/$2/$i



	 if [ ! -e $j ]
	 then
		change=1
		cp -a $i $root/$2/$i

	 elif [ -d $i ]
	 then

		cd $root

		sync $1/$i $2/$i

		cd $1

	 elif [ ! -z "$(diff $i $j )" ]
	 then

		change=1
		cp $i $root/$2/$i

	 fi
	done

	cd $root

}

echo > sync.txt

sync $1 $2


resultado="$(cat sync.txt)"

if [ $change -gt 0 ]
then

cd $2

git add .
git commit -m sincronizando
git push

cd $root

date >> sync.txt
echo >> sync.txt
echo "Um commit foi realizado no repositorio e ja foi repassado" >> sync.txt

cat sync.txt | sendemail -l email.log\
 -f "Tubs@GIT"\
 -u "Aviso"\
 -t "eduardo.gil.s.cardoso@gmail.com"\
 -s "smtp.gmail.com:587"\
 -xu "tubskleyson@gmail.com"\
 -xp "abcdasquebradas"

fi

echo Ultima sincronização : $(date) > sync.time
