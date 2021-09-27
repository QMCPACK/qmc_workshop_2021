#!/bin/bash

#
# Setup script to install QMCPACK, Quantum Espresso (QE/PWSCF), PySCF, DIRAC
# and workshop files for QMCPACK 2021 workshop https://qmc2021.ornl.gov/
#
# Assumes a vanilla Ubuntu 20.04 LTS or similar
#
# Script is safely rerunnable
#
# Use configuration options below for customization
#
# Installed applications have their own unique licenses 
#
# Installs in $HOME/apps :
#
# QMCPACK and NEXUS workflow software
# Quantum ESPRESSO (QE) 6.8
# PySCF 1.7.5
# DIRAC 21.1
# VESTA 3.5.7
#
# vim, emacs, xcrysden, and gnuplot are installed for convenience
#
# Getting started on a vanilla base Ubuntu:
#
# sudo apt-get -y install git
# cd $HOME
# git clone https://github.com/QMCPACK/qmc_workshop_2021.git
# ./qmc_workshop_2021/workshop_image/setup_ubuntu.sh
# or
# nohup ./qmc_workshop_2021/workshop_image/setup_ubuntu.sh >& out&
# tail -f out
#
# Sudoer password is needed for initial package installs and updates
# Installation may take 2h depending on underlying hardware
#

echo -- START `date`

#
# Scripte configuration options
#
INSTALL_SYSTEM_PACKAGES=1
INSTALL_QMCPACK=1
INSTALL_QE=1 # Subset of INSTALL_QMCPACK. Requires INSTALL_QMCPACK=1
INSTALL_PYSCF=1
INSTALL_DIRAC=1
INSTALL_VESTA=1
SETUP_DESKTOP=1
UPDATE_WORKSHOP_FILES=1

#
# Package updates and installation
#

if  [ $INSTALL_SYSTEM_PACKAGES -eq 1 ]; then
sudo apt-get -y update
sudo apt-get -y install build-essential gcc make perl dkms # Needed for VirtualBox Guest additions
sudo apt-get -y install cmake g++ gfortran libopenmpi-dev libboost-dev libhdf5-dev libxml2-dev fftw3-dev libopenblas-dev

# Requirements for full NEXUS demo:
sudo apt-get -y install python-is-python3 python3-pip python3-numpy python3-scipy python3-matplotlib python3-pydot python3-pandas python3-h5py
pip install --user mpi4py
pip install --user spglib
pip install --user seekpath

# Nice to have tools
sudo apt-get -y install vim emacs-nox gnuplot xcrysden

# Cleanup
sudo apt-get -y autoremove
fi

#
# Application setup
# 
if [ ! -e $HOME/apps ]; then
    mkdir $HOME/apps
fi

## QP install ahead of other apps
#sudo apt-get -y install ninja-build m4 unzip
#sudo apt-get -y install python # QP dependencies assume python availability
#cd $HOME/apps
#if [ ! -e qp2 ]; then
#    echo --- Building QP2 `date`
#    CC=gcc
#    CXX=g++
#    F90=gfortran
#    F95=gfortran
#    F77=gfortran
#    git clone https://github.com/QuantumPackage/qp2.git 
#    cd qp2
#    ./configure -i all
## Default 
##    ./configure -c config/gfortran.cfg
## Workaround for AWS     
#    sed 's/-Ofast -march=native/-O3 -march=broadwell/g' config/gfortran.cfg >config/gfortran_safe.cfg
#    ./configure -c config/gfortran_safe.cfg
## Failed attempt to use MKL. Is unreliable.    
##    sed -e 's/-lblas -llapack/-L\/opt\/intel\/compilers_and_libraries_2019.3.199\/linux\/mkl\/lib\/intel64 -Wl,--no-as-needed -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core -liomp5 -lpthread -lm -ldl/g' config/gfortran.cfg >config/gfortran_mkl.cfg
##    ./configure -c config/gfortran_mkl.cfg
#    source quantum_package.rc
#    ninja
#    cd plugins
#    git clone https://github.com/QuantumPackage/QMCPACK_ff.git qmcpack
#    sed -i s/"QMCPack"/"qmcpack"/ qmcpack/save_for_qmcpack.irp.f
#    cd ../
#    qp_plugins install qmcpack
#    sed -i s/"  read_wf = .False."/"  \!read_wf = .False."/g    src/determinants/determinants.irp.f
#    ninja
#fi
#
#echo --- Intel files setup `date`
## Setup Intel MKL and MPI
## Instructions from https://software.intel.com/en-us/articles/installing-intel-free-libs-and-python-apt-repo
#wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
#sudo apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
#rm -f GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB
##Full Intel MKL+Python products 
#sudo wget https://apt.repos.intel.com/setup/intelproducts.list -O /etc/apt/sources.list.d/intelproducts.list 
##MKL:  
##sudo sh -c 'echo deb https://apt.repos.intel.com/mkl all main > /etc/apt/sources.list.d/intel-mkl.list'  
##Intel MPI
##sudo sh -c 'echo deb https://apt.repos.intel.com/mpi all main > /etc/apt/sources.list.d/intel-mpi.list'
#sudo apt-get -y update
#sudo apt-get -y install intel-mkl-2019.3-062 #Be patient
#sudo apt-get -y install intel-mpi-2019.3-062 #Be patient


## Setup Intel MKL variables, path
#source /opt/intel/mkl/bin/mklvars.sh intel64
## Setup Intel MPI variables, path
#source /opt/intel/impi/2019.3.199/intel64/bin/mpivars.sh
#
#
#if [ ! -e $HOME/apps ]; then
#    mkdir $HOME/apps
#fi
#cd $HOME/apps
#
## HDF5 installation
#if [ ! -e hdf5-hdf5-1_10_5-gcc-impi/lib/libhdf5.a ]; then   
#echo --- Installing HDF5 `date`
#    wget https://github.com/live-clones/hdf5/archive/hdf5-1_10_5.tar.gz
#    tar xvf hdf5-1_10_5.tar.gz
#    #XXX rm -f hdf5-1_10_5.tar.gz
#    mkdir hdf5-hdf5-1_10_5-gcc-impi
#    cd hdf5-hdf5-1_10_5-gcc-impi/
#    INSTALLDIR=`pwd`
#    echo INSTALLDIR=$INSTALLDIR
#    CC=mpigcc FC=mpif90 ../hdf5-hdf5-1_10_5/configure --enable-shared --enable-parallel --enable-fortran  --prefix=$INSTALLDIR >&configure.out
#    make >&make.out
#    make install 
#    cd ..
#fi


#CC="mpigcc" HDF5_MPI="ON" HDF5_DIR=$HOME/apps/hdf5-hdf5-1_10_5-gcc-impi pip install --user --no-binary=h5py h5py
#exit 1

#
# QMCPACK and patched QE setup
#
# QMCPACK files are needed for QE for pw2qmcpack.x
#
echo --- QMCPACK and QE setup
if  [ $INSTALL_QMCPACK -eq 1 ]; then
cd $HOME/apps
if [ ! -e qmcpack ]; then
    mkdir qmcpack
fi
cd qmcpack
if [ ! -e qmcpack ]; then
    git clone https://github.com/QMCPACK/qmcpack.git --depth 1
    cd qmcpack
    # For reproducible builds, use a fixed commit or version:
    #    git checkout f95f17d2abb3cf3304553f3fd54aac3c712a1278
    #    git checkout v3.11.0
    cd ..
else
    cd qmcpack
    git pull
    cd ..
fi

# QE
if  [ $INSTALL_QE -eq 1 ]; then

if [ ! -e $HOME/apps/qe-6.8/bin/pw.x ]; then
    echo --- Patching and Building QE `date`
    cd $HOME/apps/qmcpack/qmcpack/external_codes/quantum_espresso/
    ./download_and_patch_qe6.8.sh
    cd qe-6.8
    mkdir build; cd build
    if [ -e $HOME/apps/qe-6.8 ]; then
	rm -r -f $HOME/apps/qe-6.8
	mkdir $HOME/apps/qe-6.8
    fi
    cmake -DCMAKE_C_COMPILER=mpicc -DCMAKE_Fortran_COMPILER=mpif90 -DCMAKE_INSTALL_PREFIX=$HOME/apps/qe-6.8 ..
    echo --- Make
    time make  -j 4
    make install
    cd ../..
    # If successfully installed we remove the whole QE directory tree and archive file
    if [ -e $HOME/apps/qe-6.8/bin/pw.x ]; then
	rm -r -f qe-6.8 qe-6.8.tar.gz
    fi
    cd $HOME/apps
fi
fi


cd $HOME/apps/qmcpack
if [ ! -e bin/qmcpack ]; then
    echo --- Building QMCPACK `date`
    if [ -e build ]; then
	rm -r -f build
    fi
    
    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX=$HOME/apps/qmcpack -DCMAKE_CXX_COMPILER=mpicxx -DCMAKE_C_COMPILER=mpicc -DQE_BIN=$HOME/apps/qe-6.8/build/bin ../qmcpack/
    time make -j 4
    make install
    ctest -L unit
    cd ..
    rm -r -f build
fi

if [ ! -e bin/qmcpack_complex ]; then
    echo --- Building QMCPACK Complex `date`
    if [ -e build_complex ]; then
	rm -r -f build_complex
    fi
    mkdir build_complex
    cd build_complex
    cmake -DQMC_COMPLEX=1 -DCMAKE_CXX_COMPILER=mpicxx -DCMAKE_C_COMPILER=mpicc -DQE_BIN=$HOME/apps/qe-6.8/build/bin ../qmcpack/
    time make -j 4
    ctest -L unit
    cp -p bin/qmcpack_complex $HOME/apps/qmcpack/bin
#    cd ../build/bin
#    ln -sf ../../build_complex/bin/qmcpack_complex qmcpack_complex
    cd ..
    rm -r -f build_complex
    cd ..
fi

fi

#
# PySCF
#

if  [ $INSTALL_PYSCF -eq 1 ]; then

    export PYSCF_HOME=$HOME/apps/pyscf
echo --- PYSCF_HOME set to ${PYSCF_HOME}
if [ ! -e ${PYSCF_HOME}/pyscf/setup.py ]; then
    echo --- Downloading and installing PYSCF

    if [ -e $HOME/apps/pyscf ]; then
	rm -r -f $HOME/apps/pyscf
    fi

    if [ ! -e $HOME/apps ]; then
	mkdir $HOME/apps
    fi
    
       
    
mkdir $HOME/apps/pyscf
cd $HOME/apps/pyscf

#git clone https://github.com/pyscf/pyscf.git
#cd pyscf
#git checkout v1.7.5 # Released 2020-10-04
wget https://github.com/pyscf/pyscf/archive/v1.7.5.tar.gz
tar xvf v1.7.5.tar.gz
rm -f v1.7.5.tar.gz
mv pyscf-1.7.5 pyscf
cd pyscf
    
topdir=`pwd`
here=`pwd`/opt
herelib=`pwd`/opt/lib
mkdir opt
cd opt

echo --- libcint
git clone https://github.com/sunqm/libcint.git
cd libcint
git checkout v4.0.7
mkdir build
cd build
cmake -DWITH_F12=1 -DWITH_RANGE_COULOMB=1 -DWITH_COULOMB_ERF=1 \
    -DCMAKE_INSTALL_PREFIX:PATH=$here -DCMAKE_INSTALL_LIBDIR:PATH=lib ..
make -j 4
make install

cd ..
cd ..


echo --- libxc
git clone https://gitlab.com/libxc/libxc.git
cd libxc
git checkout 4.3.4
autoreconf -i
./configure --prefix=$here --libdir=$herelib --enable-vxc --enable-fxc --enable-kxc \
    --enable-shared --disable-static --enable-shared --disable-fortran LIBS=-lm
make -j 4
make install
cd ..


echo --- xcfun library
git clone https://github.com/dftlibs/xcfun.git
cd xcfun
git checkout 8ec13b06e06feccbc9e968665977df14d7bfdff8
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=RELEASE -DBUILD_SHARED_LIBS=1 -DXC_MAX_ORDER=3 -DXCFUN_ENABLE_TESTS=0 \
    -DCMAKE_INSTALL_PREFIX:PATH=$here -DCMAKE_INSTALL_LIBDIR:PATH=lib ..
make -j 4
make install
cd ..
cd ..

rm -r -f libcint libxc xcfun # After installation, source not required
echo --- PySCF dependency setup complete
cd ..


echo --- Top level PySCF directory `pwd`
cd pyscf/lib
mkdir build
cd build
cmake -DBUILD_LIBCINT=0 -DBUILD_LIBXC=0 -DBUILD_XCFUN=0 -DCMAKE_INSTALL_PREFIX:PATH=$here ..
make -j 4
echo --- PySCF build done
export PYTHONPATH=$topdir:$PYTHONPATH
export LD_LIBRARY_PATH=$herelib:$LD_LIBRARY_PATH
echo export PYTHONPATH=$topdir:\$PYTHONPATH
echo export LD_LIBRARY_PATH=$herelib:\$LD_LIBRARY_PATH

else
    echo -- Found existing PySCF installation
fi
fi

#
# DIRAC
#

if  [ $INSTALL_DIRAC -eq 1 ]; then

if [ ! -e $HOME/apps/dirac/share ]; then

if [ ! -e $HOME/apps/dirac ]; then
    mkdir $HOME/apps/dirac
fi

cd $HOME/apps/dirac
if [ ! -e DIRAC-21.1-Source.tar.gz ]; then
    wget https://zenodo.org/record/5512841/files/DIRAC-21.1-Source.tar.gz
fi
tar xvf DIRAC-21.1-Source.tar.gz
cd DIRAC-21.1-Source
./setup --prefix=$HOME/apps/dirac
cd build
make -j 4
#make test
make install

cd ../..

rm -r -f DIRAC-21.1-Source  DIRAC-21.1-Source.tar.gz

fi
fi

    


#
# VESTA
#
if  [ $INSTALL_VESTA -eq 1 ]; then
if [ ! -e $HOME/apps/vesta/VESTA-gtk3/VESTA ]; then
echo --- Installing VESTA
if [ ! -e $HOME/apps/vesta ]; then
    mkdir $HOME/apps/vesta
fi
cd $HOME/apps/vesta
if [ ! -e VESTA-gtk3.tar.bz2 ]; then
    wget https://jp-minerals.org/vesta/archives/3.5.7/VESTA-gtk3.tar.bz2
fi
tar xvf VESTA-gtk3.tar.bz2 
rm -f VESTA-gtk3.tar.bz2
# To run VESTA put $HOME/apps/vesta/VESTA-gtk3 on the path
fi

fi

cd $HOME
echo --- Shell setup `date`
HAVESETUP=`grep -c START-QMCPACK-RELATED $HOME/.bashrc`
if  [ $HAVESETUP -eq 0 ]; then
    echo --- Modifying .bashrc to add PATHs
cat >>$HOME/.bashrc <<EOF
# START-QMCPACK-RELATED
# QMCPACK and NEXUS
export PATH=\$HOME/apps/qmcpack/bin:\$PATH
export PATH=\$HOME/apps/qmcpack/qmcpack/nexus/bin:\$PATH
export PYTHONPATH=\$HOME/apps/qmcpack/qmcpack/nexus/lib:\$PYTHONPATH
export PYTHONPATH=\$HOME/apps/qmcpack/qmcpack/utils/afqmctools:\$PYTHONPATH
# QE
export PATH=\$HOME/apps/qe-6.8/bin:\$PATH
# PySCF
export PYTHONPATH=\$HOME/apps/pyscf:\$PYTHONPATH
export PYTHONPATH=\$HOME/apps/qmcpack/qmcpack/src/QMCTools:\$PYTHONPATH
export LD_LIBRARY_PATH=\$HOME/apps/pyscf/pyscf/opt/lib:\$LD_LIBRARY_PATH
## QP
#source \$HOME/apps/qp2/quantum_package.rc
# DIRAC
export PATH=\$HOME/apps/dirac/bin:\$PATH
# VESTA
export PATH=\$HOME/apps/vesta/VESTA-gtk3:\$PATH
# END-QMCPACK-RELATED
EOF
else
    echo --- .bashrc already contains setup information. Not modifying.
fi
# Add setup info to current shell for convenience
# QMCPACK and NEXUS
export PATH=$HOME/apps/qmcpack/bin:$PATH
export PATH=$HOME/apps/qmcpack/qmcpack/nexus/bin:$PATH
export PYTHONPATH=$HOME/apps/qmcpack/qmcpack/nexus/lib:$PYTHONPATH
# QE
export PATH=$HOME/apps/qe-6.8/bin:$PATH
# PySCF
export PYTHONPATH=$HOME/apps/pyscf:$PYTHONPATH
export PYTHONPATH=$HOME/apps/qmcpack/qmcpack/src/QMCTools:$PYTHONPATH
export LD_LIBRARY_PATH=$HOME/apps/pyscf/pyscf/opt/lib:$LD_LIBRARY_PATH
## QP
#source $HOME/apps/qp2/quantum_package.rc
# DIRAC
export PATH=$HOME/apps/dirac/bin:$PATH
# VESTA
export PATH=$HOME/apps/vesta/VESTA-gtk3:$PATH

if  [ $SETUP_DESKTOP -eq 1 ]; then

echo -- Ubuntu Desktop convenience
if [ ! -e $HOME/.config/autostart/gnome-terminal-desktop ]; then

    if [ ! -e $HOME/.config ]; then
	mkdir $HOME/.config
    fi
    if [ ! -e $HOME/.config/autostart ]; then
	mkdir $HOME/.config/autostart
    fi
    
cat >$HOME/.config/autostart/gnome-terminal.desktop<<EOF
[Desktop Entry]
Type=Application
Exec=gnome-terminal
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=Terminal
Name=Terminal
Comment[en_US]=
Comment=
EOF
echo "Added startup Terminal"
fi
if [ ! -e $HOME/Desktop/WORKSHOP_README.txt ]; then
    if [ ! -e $HOME/Desktop ]; then
	mkdir $HOME/Desktop
    fi
    cat >$HOME/Desktop/WORKSHOP_README.txt<<EOF
QMC Workshop 2021 Image based on Ubuntu 20.04 LTS

https://qmc2021.ornl.gov

https://github.com/QMCPACK/qmc_workshop_2021

This image contains installed versions of

QMCPACK
NEXUS
Quantum ESPRESSO (QE) 6.8
PySCF 1.7.5
DIRAC 21.1

See the individual packages for details of their licenses

For visualization "VESTA" is available, and for editing vim and emacs are already installed.

Programs are installed in \$HOME/apps configured to be available on the \$PATH . e.g. "pw.x", "VESTA".

Install additional packages from the Ubuntu registry e.g. sudo apt-get install package_name

To update the workshop files:

cd \$HOME/qmc_workshop_2021
git pull

To update the QMCPACK and NEXUS sources:

cd \$HOME/qmcpack/qmcpack
git pull
EOF
echo "Added Desktop WORKSHOP_README.txt"
fi
fi

if  [ $UPDATE_WORKSHOP_FILES -eq 1 ]; then
echo --- Workshop files `date`
# In case the install script was copied in vs run the workshop git
# setup workshop git otherwise update
cd $HOME
if [ ! -e qmc_workshop_2021 ]; then
    git clone https://github.com/QMCPACK/qmc_workshop_2021.git
else
    cd qmc_workshop_2021
    git pull
    cd ..
fi
fi
echo -- END `date`

