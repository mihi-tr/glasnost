GZDIR=/mnt/usb/glasnost/data/gz
DATADIR=/mnt/usb/glasnost/data/unpacked/
cwd=$PWD
cd $DATADIR
for FILE in `find $GZDIR -name "*.tgz"`; do 
    tar -xvzf $FILE --exclude="*.dump" --exclude="*.measurementlab.net.log";
    done

cd $cwd
