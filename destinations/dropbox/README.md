# Synchronizing to Dropbox

This guide walks you through having your photos uploaded to Dropbox.

The `piphoto-dropbox-sync` will upload the photos using the Dropbox Uploader tool connected to a Dropbox App key .

In the Dropbox, the images are organized in directories named `YYYY/YYYY-MM-DD/` based on the exif data of the file. For example:

``` text
2024
├── 2024-11-01
│   ├── DSC_1536.NEF
│   ├── DSC_1537.NEF
│   └── DSC_1538.NEF
├── 2024-11-07
│   ├── DSC_1001.NEF
│   ├── DSC_1002.NEF
│   └── DSC_1003.NEF
...
```

This script is installed by default when you install `piphoto`, but to use it, you will need to install [Dropbox Uploader](https://github.com/andreafabrizi/Dropbox-Uploader/) as described below

## Usage

The `piphoto-dropbox-sync` will read options from `/etc/piphoto.dropbox.conf` or the command line (see `piphoto-dropbox-sync -h` for options).

## Install Dropbox Uploader

_Dropbox Uploader_ is a tool that can upload and download files to/from the Dropbox cloud service.

<https://github.com/andreafabrizi/Dropbox-Uploader/>

The above URL will have the most up-to-date instructions for installation, but the basics are:

1. Clone the git repository to a directory on your Raspberry Pi:

    ``` shell
    git clone https://github.com/andreafabrizi/Dropbox-Uploader.git
    ```

2. Add execute permissions to the downloaded script:

    ``` shell
    chmod +x Dropbox-Uploader/dropbox_uploader.sh
    ```

3. Run the script and follow the directions to create an App, an API key, and connect your Dropbox:

    ``` shell
    $ ./dropbox_uploader.sh

    This is the first time you run this script, please follow the instructions:

    (note: Dropbox will change their API on 2021-09-30.
    When using dropbox_uploader.sh configured in the past with the old API, have a look at README.md, before continue.)

    1) Open the following URL in your Browser, and log in using your account: https://www.dropbox.com/developers/apps
    2) Click on "Create App", then select "Choose an API: Scoped Access"
    3) Choose the type of access you need: App folder
    4) Enter the "App Name" that you prefer (e.g. MyUploader23592122016593), must be unique

    Now, click on the "Create App" button.

    5) Now the new configuration is opened, switch to tab "permissions"
    and check "files.metadata.read/write" and "files.content.read/write"
    Now, click on the "Submit" button.

    [... etc ...]
    ```

    NOTE: If you do not follow the instructions to add permissions you will need to create a new Access Code after adding them. Permissions do not apply retroactively.

    This step will create a file named `.dropbox-uploader` in your pi user's $HOME directory.

    Optional:  Copy the `dropbox_uploader.sh` into `/usr/local/bin` on the pi.

    ``` shell
    sudo cp -v dropbox_uploader.sh /usr/local/bin
    ```

## Test Dropbox Uploader

Test the dropbox_uploader.sh by running the following:

``` shell
dropbox_uploader.sh upload some_file /
```

## Configuration

The `piphoto-dropbox-sync` script reads from `/etc/piphoto.dropbox.conf`. An example config is provided in `piphoto.dropbox.conf.example`.

The variables that need to be set are:

- **`dropbox_uploader_sh`** - If the script is not on the user's PATH, this needs to be the full path to the dropbox_uploader.sh

- **`dropbox_uploader_config`** - The path to the `.dropbox-uploader` config file

- **`dest_path`** - The path in the Dropbox App to put the photos.

  Note: Dropbox Apps can be set up to have full access to the Dropbox folder, or only to an application-specific directory.  This is configured when the app is created at the Dropbox Developers page.

  - If "Full Dropbox", the `/` refers to the top level of the Dropbox directory, i.e. something like  `$USER/Dropbox/`
  - If "App folder", the `/` refers to a directory for the app in the Dropbox/Apps directory, e.g.  `$HOME/Dropbox/Apps/name-of-the-app/`

## Testing photo sync to Dropbox

Once `piphoto-dropbox-sync` is configured, it should be tested by running the following:

``` shell
piphoto-dropbox-sync /path/to/images
```

to ensure it's working properly.

## Setting up PiPhoto

Finally, setup your PiPhoto to use `piphoto-dropbox-sync` to copy the images to the Dropbox cloud. In your `piphoto.conf` file:

``` shell
sync_command="piphoto-dropbox-sync"
```

## Caveats

This should organize images in the remote folder by capture date gathered from the images' EXIF metadata, similar to the [Copying and Organizing over SSH](../ssh-copy-and-organize/README.md) setup.
