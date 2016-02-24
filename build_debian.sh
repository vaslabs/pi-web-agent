#!/bin/bash
#requires bash 4.0+
#turn on extglob for directory exclusion patterns
shopt -s extglob
#consider dot files
shopt -s dotglob
####Ensure the right input is given
###realy basic validation does it exist? ask for it
declare -A ARGSV
ACCEPTED[0]=maintainerName
ACCEPTED[1]=email
ACCEPTED[2]=license
ACCEPTED[3]=release
CONTROLPROPERTIES[0]=source
CONTROLPROPERTIES[1]=section
CONTROLPROPERTIES[2]=homepage
CONTROLPROPERTIES[3]=architecture
CONTROLPROPERTIES[4]=depends
CONTROLPROPERTIES[5]=description
i=1
for K in "${!ACCEPTED[@]}"; do
	ARGSV[${ACCEPTED[$K]}]="${!i}"
	if [ -z  "${ARGSV["${ACCEPTED[$K]}"]}" ]; then
        	echo "Please enter ${ACCEPTED[$K]}:"
        	read ARGSV[${ACCEPTED[$K]}]
		if [ -z "${ARGSV[${ACCEPTED[$K]}]}" ]; then
        		echo "Doh! come back when you know your ${ACCEPTED[$K]}"&&exit 1
		fi
	fi
	let "i++"
done
for i in "${!ARGSV[@]}"; do echo "key  : $i"; echo "value: ${ARGSV[$i]}"; done
#####Initialize everything here
PACKAGENAME=pi-web-agent
RELEASENAME=$PACKAGENAME-${ARGSV[release]}
PROJDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd );
PROGNAME=$(basename $0)
#####Functions
function ok(){
	echo -e "[ \e[1;32m 0K \e[0m ] $1"
}
function poop(){

	echo -e "[ \e[1;31m ABORTING \e[0m ] ${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
	exit 1
}
function build {
	if cd ./src/$RELEASENAME&&sh ./build.sh $RELEASE &&cd $PROJDIR;then
		ok "build complete"
	else
		poop "build failed"
	fi
}
function cleanBuild {
        if rm -rf ./src/*&&mkdir ./src/$RELEASENAME\
	 &&cp -rf ./!(src) ./src/$RELEASENAME&&build;then
		ok "clean build complete"
	else
		poop "clean build failed"
	fi
}
function removeHiddenSrc {
	if find ./src/$RELEASENAME -name '.*' ! -name '.' ! -name '..' -exec rm -rf '{}' \; ;then
		ok "hidden files removed successfully "
	else
		poop "Oh parots...I didn't manage to remove those hidden files"
	fi	
}
function tarRelease {
	cd ./src/
	if tar -zcvf /tmp/$RELEASENAME.tar.gz $RELEASENAME \
 	--exclude "./src/$RELEASENAME/.git"\
	&&mv /tmp/$RELEASENAME.tar.gz $RELEASENAME/$RELEASENAME.tar.gz ;then
		ok "release compression complete"
	else
		poop "release compression failed"
	fi
	cd $PROJDIR
}
###long description needs a seperate function
###as it is multiline
function longDescriptionToControl {
	if DESCRIPTION=$(./JSONFetchKey.py longDescription < package.json |fold -w 80 -s| sed 's|^| |')\
 	 &&sed -i.bak "s|.*long description.*|`echo "$DESCRIPTION"|awk '{printf("%s\\\\n", $0);}'|sed -e 's/\\\n$//'`|g"\
	 src/$RELEASENAME/debian/control;then
        	ok "long decription added to control"
	else
        	poop "Oh parrots, couldn't add long decription to control"
	fi

}
function propertyToControl {
	KEY=$1
	if VAL=$(./JSONFetchKey.py $KEY < package.json)\
	 &&PROP=`echo ${KEY:0:1} | tr  '[a-z]' '[A-Z]'`${KEY:1}\
	 &&sed -i.bak "s|^$PROP:.*|$PROP: ${VAL}|" src/$RELEASENAME/debian/control; then
		ok "$PROP added to control"
	else
		poop "Oh parrots, couldn't add $PROP to control"
	fi

}
function propertiesToControl {
	for K in "${!CONTROLPROPERTIES[@]}"; do
		propertyToControl ${CONTROLPROPERTIES[$K]}
	done
}
testcommand()
{
 	if [ -z "$(command -v $1)" ]
 	then 
  		return 1 #failure nothing returned
 	else
  		return 0 #succes location returned and command works
 	fi
}
#check bash version
#requires bash 4.0+

dpkg --compare-versions 4.0 lt ${BASH_VERSION%%[^0-9.]*}\
&& ok "Your bash version rocks"\
|| poop "Your bash version is from the age of dinasaurs"

#####install dependencies
if $(testcommand dh_make);then
	ok "Your system rocks dh_make already installed"
else
	sudo apt-get install dh-make && testcommand dh_make\
	&&ok "dh_make now installed"|| poop "Oh parrots, could not install dhmake"
fi
<<"COMMENT"
if [ -z "$RELEASE" ]; then
        echo -e "This build will \e[0;34m not \e[0m be used for a release"
else
        echo -e "This build will be used for Release:\e[0m $RELEASE \e[0m"
        echo -e "Creating Branch \e[0;34m $RELEASE\e[0m"
        git checkout -b "$RELEASE"
        echo "Pushing new branch to origin"
        git push origin "$RELEASE"
        echo "Now your branches are:"
        git branch
fi;
COMMENT
#main logic
#make sure you are in the right directory
cd $PROJDIR
cleanBuild&&tarRelease
###go to the directory where the code was build
###and run dhmake
cd ./src/$RELEASENAME\
&&DEBFULLNAME="${ARGSV[maintainerName]}" \
dh_make -s -y -e ${ARGSV[email]} --copyright ${ARGSV[license]} -f $RELEASENAME.tar.gz -r dh7\
&&ok "dh_make done!"|| poop "Oh parrots, the dh_make thingy failed"

cd $PROJDIR
propertiesToControl
longDescriptionToControl
rm src/$RELEASENAME/debian/*.ex

cp ./buildfiles/debian/postinst src/$RELEASENAME/debian/postinst\
&&ok "postinst included successfully"|| poop "Oh parrots, fialed to include postinst"

cp ./buildfiles/debian/prerm src/$RELEASENAME/debian/prerm\
&&ok "prerm included successfully"|| poop "Oh parrots, failed to include prerm"

cp ./buildfiles/debian/copyright src/$RELEASENAME/debian/copyright\
&&ok "copyright included successfully"|| poop "Oh parrots, failed to include copyright" 

rm src/$RELEASENAME/$RELEASENAME.tar.gz 
rm src/$RELEASENAME/debian/files
cd src/$RELEASENAME/
fakeroot dpkg-buildpackage -F
echo $PROJDIR
cd $PROJDIR
rm bin/*
cp src/*.deb bin/.
##commit current state
#if [ ! -z "$RELEASE" ]; then
#        git add .
#        git commit -m "Version build for release $RELEASE"
#        git push origin "$RELEASE"
#fi;
