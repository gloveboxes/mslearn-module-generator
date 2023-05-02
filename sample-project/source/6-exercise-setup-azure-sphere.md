Install the following software on your computer.

## Troubleshooting

1. If you have trouble connecting to the Azure Sphere over USB be sure to disable any VPNs you might have enabled.
2. The **TAP-Windows Adapter V9** installed with VPN clients, including OpenVPN client is not compatible with the **TAP-Windows Adapter V9** required and installed by the Azure Sphere SDK. You will need to uninstall the VPN client and reinstall the Azure Sphere SDK for Visual Studio.
3. Windows Users. If running the IoT Central ShowIoTCentralConfig command fails with a missing library message then delete the folder from ShowIoTCentralConfig from AppData\\Local\\Temp\\.net.

## Azure Sphere SDK version

This learning module requires Azure Sphere SDK version 20.11 or newer.

## Windows 10 users

This learning module supports developers on Linux and Windows using Visual Studio Code. However, if you are a Windows user comfortable using Visual Studio then you can still complete the exercises appreciating that the IDE screenshots included in this module will be different.

You need to do the following:

1. Install the latest Azure Sphere SDK.
1. Install CMake and Ninja.
1. Install Visual Studio Code.
1. Install the Visual Studio Code Azure Sphere extension.
1. Claim your device.
1. Configure networking for the device.

The following [Quickstart: Install the Azure Sphere SDK for Windows](/azure-sphere/install/install-sdk?azure-portal=true&pivots=vs-code) will step you through the process.

### Install the Git client for Windows

The Git client is required to clone the Learning Path Labs and the Azure Sphere SDK Samples.

Install [Git for Windows](https://git-scm.com/downloads?azure-portal=true).

### Install the GNU Arm Embedded Toolchain for Windows

1. Download the [GNU Arm Embedded Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads?azure-portal=true) for Windows.
2. Install the GNU Arm Embedded Toolchain

## Ubuntu 18.04 or 20.04 LTS users

You need to do the following:

1. Install the Azure Sphere SDK.
    **Ensure you install the new azsphere CLI v2**.
1. Set up the device connection.
1. Install CMake and Ninja.
1. Install Visual Studio Code.
1. Install the Visual Studio Code Azure Sphere extension.
1. Claim your device.
1. Configure networking for the device.



The following [Quickstart: Install the Azure Sphere SDK for Linux](/azure-sphere/install/install-sdk-linux?azure-portal=true&pivots=vs-code-linux) will step you through the process.

### Install the Git client for Linux

The Git client is required to clone the Learning Path Labs and the Azure Sphere SDK Samples.

```
sudo apt install git
```

### Install the GNU Arm Embedded Toolchain for Linux

Install the GNU Arm Embedded Toolchain for Linux

1. Download the [GNU Arm Embedded Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads?azure-portal=true). At the time of writing this is *Version 10-2020-q4-major*.
2. Install the downloaded package. The following installs the toolchain in the /opt directory.

    ```bash
    sudo tar -xjvf gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2 -C /opt
    ```

3. Update your path. Open ~/.bashrc and add to the end.

    ```bash
    export PATH=$PATH:/opt/gcc-arm-none-eabi-10-2020-q4-major/bin
    ```

4. Optional: The real-time core debugger relies on the *libncurses.so.5* library. Depending on your system setup, this library may already be install, if not, then run the following commands.

    ```bash
    sudo add-apt-repository universe
    sudo apt-get install libncurses5
    ```

## Recommended Visual Studio Code Extension

The Peacock extension allows you to change the color of your Visual Studio Code workspace. The Peacock extension is useful when you have multiple instances of Visual Studio Code open. In one of the exercises an instance of Visual Studio Code will be attached to the real-time core, and another instance will be attached to the high-level application core.

   1. Open Extensions sideBar panel in Visual Studio Code
      - Or choose the menu options for View → Extensions
   1. Search for Peacock
   1. Click Install
   1. Click Reload, if required

## Delete existing applications on Azure Sphere

1. From the Windows **PowerShell command line** or Linux **Terminal**, run the following command to delete any existing applications on the device.

   ```
   azsphere device sideload delete
   ```

2. Restart Azure Sphere.

   ```
   azsphere device restart
   ```

## Enable high-level core development

1. From the Windows **PowerShell command line** or Linux **Terminal**, run the following command to enable high-level app development on the device.

   ```
   azsphere device enable-development
   ```

## Enable real-time core development

### Windows 10 users

1. Open the Windows **PowerShell command line** as **Administrator**, and run the following command to enable real-time core development on the device.

   ```
   azsphere device enable-development -r
   ```

2. Close the Windows **PowerShell command line**

### Linux users

1. Open the Linux **Terminal** and run the following command to enable real-time core development on the device.

   ```bash
   azsphere device enable-development -r
   ```

## Clone the Azure Sphere Developer Learning Path

> [!NOTE]
> Clone the *Azure Sphere Developer Learning Path* to a directory close to the root directory on your computer. For example, **c:\lab**, or **~/**. The reason is that the Azure Sphere build process uses CMake which can struggle with long path and directory names.

```
git clone --depth 1 https://github.com/MicrosoftDocs/Azure-Sphere-Developer-Learning-Path.git Azure-Sphere
```

## Clone the Azure Sphere samples

The Azure Sphere samples repository includes a tool required for listing Azure IoT Central network endpoints.

Clone this repository into the same directory that you cloned the Azure Sphere Developer Learning Path into.

```
git clone --depth 1 https://github.com/Azure/azure-sphere-samples.git
```