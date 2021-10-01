# How to use the QMC Workshop Image

* Install the latest version of VirtualBox (free), v6.1.26 when this file was updated. https://www.virtualbox.org/ 
* Download the workshop image file using the link provided by us. The file is 5GB in size, so will take several minutes to download even on the fastest networks, and potentially several hours. Be patient and try again at a different time or using a different network if initially unsuccessful.
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

# Setup notes for VirtualBox and QMC Workshop Image

The workshop image is currently created "by hand", but once proven out the 
intent is to fully automate creation of the image so that a "live" distribution
of QMCPACK can be provided.

* **Important: Do not freelance any activities involving passwords or access tokens (etc.) during this process because they may be recoverable from the image file.**
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
* Upload to Box.com site. Create/update shared link. Update bit.ly shortlink.
