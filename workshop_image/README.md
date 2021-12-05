# How to use the QMC Workshop Image and Virtual Machine

QMC can be easily tried out using the virtual machine provided here. It contains
QMCPACK, Quantum ESPRESSO, PySCF, and DIRAC, as well as all the workshop files.
The virtual machine provides a familiar desktop GUI environment with no risk of
interference with other installed software. The installation scripts are
provided and can be used as inspiration for a direct installation.

## x86-based Windows, Linux, and macOS

* Install the latest version of VirtualBox (free, no cost) from
  https://www.virtualbox.org/  . We used v6.1.30 to make the image. 
* Download the workshop image file from https://bit.ly/qmcworkshopimage . The
  file is nearly 6GB in size, so will take several minutes to download even on
  the fastest networks, and potentially several hours. Be patient and try again
  at a different time or using a different network if initially unsuccessful.
* Run VirtualBox and import the image to setup the workshop virtual machine:
 * In VirtualBox, select the menu File->Import Appliance. Import the QMCWorkshopImage.ova that was just downloaded.
 * Customize the "Appliance" Settings during Import to suit your computer. e.g. Increase the CPU count to match the machine you are running on (maybe 4 for laptop, 16-128 for a workstation), Increase the memory (4GB should be OK on laptops).  Not setting the core count and memory sufficiently large will result in poor performance. Consider renaming the machine.
 * Complete importing the virtual machine. Initial setup may take a few minutes.
 * In the main VirtualBox window select the new machine, then "Start". You should see Ubuntu boot and a standard desktop appear.
 * The virtual machine is setup to automatically log in as user "qmcuser". Should you need to authenticate the word you need is "workshop21" (without quotes).
 * You can get a terminal (or other application) by clicking the square of dots icon at the bottom left and either typing or selecting the application you want.
 * Inside a terminal, e.g. "qmcpack", "qmcpack_complex", "pw.x", "pam-dirac", and "VESTA" are on the path. NEXUS and PySCF are available through python. These were installed in $HOME/apps
 * You can install any standard Linux software, e.g. via "sudo apt-get install your_favorite_editor". emacs and gnuplot are already installed.
* Convenience tip: Right click on the Terminal icon & make a favorite to keep in the task bar.

## m1-based macOS machines

We provide a virtual machine for UTM, an open source virtualization and
emulation package. Ubuntu Linux for ARM is virtualized and runs at close to full
speed on the m1. The beta daily release of Ubuntu 22 is used for compatibility
and performance. UTM its support for m1 are less mature than longer established
software such as BirtualBox, so if any difficulties are found, do check for more
recent software versions.

* Install the latest version of UTM for mac (free, open source) from https://mac.getutm.app . You
  can also purchase from the Mac App Store to contribute financially to the
  project.
* Download the workshop image file from https://bit.ly/qmcworkshopimagem1 . The
  file is nearly 6GB in size, so will take several minutes to download even on the
  fastest networks, and potentially several hours. Be patient and try again at a
  different time or using a different network if initially unsuccessful.
* Unzip the downloaded image file to obtain QMCWorkshopUTMImage.utm
* Import the VirtualMachine from the UTM application menu, File->Import Virtual
  Machine
* Start the newly created virtual machine using the large "play" icon
* The virtual machine is setup to automatically log in as user "qmcuser". Should you need to authenticate the word you need is "workshop21" (without quotes).
* You can get a terminal (or other application) by clicking the square of dots icon at the bottom left and either typing or selecting the application you want.
* Inside a terminal, e.g. "qmcpack", "qmcpack_complex", "pw.x"are on the path.
  NEXUS and PySCF are available through python. These were installed in
  $HOME/apps. VESTA is not available because it is an x86 application. DIRAC
  21.1 was not successfully installed because it fails to compile with recent
  gcc compilers due to non-standards compliant fortran.

# Instructions for building the QMC Workshop Image

These instructions allow either recreating the exact virtual machine and
workshop image used in the workshop or the production of a customized version.

**Important: Do not freelance any activities involving passwords or access
  tokens (etc.) while making a virtual machine because they may be recoverable from the
  image file.**

## VirtualBox on x86 machines

The workshop image is currently created "by hand", but once proven out the 
intent is to fully automate creation of the image so that a "live" distribution
of QMCPACK can be provided.

* Download Ubuntu 20.04 LTS base image http://www.releases.ubuntu.com/20.04/
* Create new machine in VirtualBox
  * Used 4GB memory, variable 16GB hard drive
* Before initial start:
  * Set maximum video memory 128MB to avoid black screen on resize
  * Set 4 CPUs, not default 1. For the workshop we assume an at least 4 core setup.
* Start the VM and work through the Ubuntu installer:
  * Set US Keyboard
  * Minimal installation
  * Download updates during install
  * Don't install 3rd party software
  * Erase disk and install Ubuntu
  * Set New York time

* name: Workshop
* computer name: WorkshopVBX
* username: qmcuser
* magic word: workshop21
* **set login automatically**
* (Standard install questions... long wait + reboot)
* Allow software updater to run and reboot as needed
* Settings (at top right) ->Privacy->Screen Lock disable

* In terminal
```
# Expect the install to take a few hours
# Install script uses sudo in the beginning
# will need password input if not run before
cd $HOME
sudo apt-get -y install git
git clone https://github.com/QMCPACK/qmc_workshop_2021.git
nohup ./qmc_workshop_2021/workshop_image/ubuntu_setup.sh >& out&
tail -f out
```
* There are customization options in the setup script to enable or disable
  different applications.
* Reboot when finished (Due to updates+required kernel extensions for Guest additions)
* Devices->Install Guest Additions CD. Install integrations.
* Reboot
* Check `which qmcpack` works
* VirtualBox Image compression (ESSENTIAL TO REDUCE <5GB)
  * In a Terminal `dd if=/dev/zero of=/var/tmp/bigemptyfile bs=4096k ; rm /var/tmp/bigemptyfile`
  * shutdown VM
  * `VBoxManage modifymedium --compact /path/to/thedisk.vdi`
  * e.g. `VBoxManage modifymedium --compact /Users/pk7/VirtualBox\ VMs/WorkshopUbuntu/WorkshopUbuntu.vdi` or `vboxmanage` with Linux hosts (capitalization varies)
* Export image using VirtualBox. Set title, URL etc. as desired.

## UTM on m1 macOS machines

* Install the latest version of UTM from https://mac.getutm.app/ (currently 2.4.1)
* Download the Ubuntu 22.04 LTS Daily beta build from
  http://cdimage.ubuntu.com/daily-live/current/ e.g.
  http://cdimage.ubuntu.com/daily-live/current/jammy-desktop-arm64.iso  (about
  2.5GB)
* In UTM:
  * Create New Virtual Machine 
    * Information: Name: Workshop, Style: OS
    * System: Architecture ARM64 (aarch64), Memory: 4096 MB
    * Drives: Create 2 New Drives: VirtIO 16GB and Removable USB Interface.
    * Save
  * Select Workshop VM. Before starting, select CD/DVD, browsw and set to
    downloaded jammy-desktop-arm64.iso
  * Start VM (large "play" button)
    * Select Ubuntu
    * Run Install Ubuntu 22 LTS when desktop appears
      * Minimal installation, download updates while installing
      * Erase disk and install ubuntu
      * name: Workshop
      * computer name: WorkshopUTM
      * username: qmcuser
      * magic word: workshop21
      * **set login automatically**
      * (Standard install questions... long wait + reboot)
      * UTM often fails to restart at this point. Restart the VM. (triangle in
        window title bar to the left of the VM name)
      * Allow software updater to run and reboot as needed
      * Settings (at top right) ->Privacy->Screen Lock disable
      * In terminal
        ```
        # Expect the install to take a few hours
        # Install script uses sudo in the beginning
        # will need password input if not run before
        cd $HOME
        sudo apt-get -y install git
        git clone https://github.com/QMCPACK/qmc_workshop_2021.git
        nohup ./qmc_workshop_2021/workshop_image/ubuntu_setup.sh >& out&
        tail -f out
        ```
      * There are customization options in the setup script to enable or disable
  different applications. 
      * Use magic word for new keyring if prompted
      * Reboot
      * Check `which qmcpack` works
      * Power Off the VM
      * Clear the CD/DVD with the .iso
      * "Share" the VM, Save As QMCWorkshopUTMImage.utm
      * Compress the image to convert the ~16GB image file to ~6GB.

