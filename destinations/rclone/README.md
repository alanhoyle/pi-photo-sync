# Synchronizing to Remote Storage with rclone

This guide walks you through having your photos uploaded to a remote storage backend using `rclone`.

The `piphoto-rclone-sync` script will upload the photos using the `rclone` tool configured with a remote backend.

In the remote storage, the images are organized in directories named `YYYY/YYYY-MM-DD/` based on the EXIF data of the file. For example:

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

This script is installed by default when you install `piphoto`, but to use it, you will need to install and configure [rclone](https://rclone.org/) as described below.

## Usage

The `piphoto-rclone-sync` script will read options from `/etc/piphoto.rclone.conf` or the command line (see `piphoto-rclone-sync -h` for options).

## Install and Configure rclone

_rclone_ is a command-line program to manage files on cloud storage.

<https://rclone.org/>

The above URL will have the most up-to-date instructions for installation, but the basics are:

1. Install `rclone` on your Raspberry Pi:

    ``` shell
    sudo apt update
    sudo apt install rclone
    ```

2. Configure a remote backend:

    ``` shell
    rclone config
    ```

    Follow the interactive prompts to create and configure a remote. For example, you might create a remote named `remote:` that connects to Google Drive, S3, or another cloud storage provider.

3. Test the remote configuration:

    ``` shell
    rclone ls remote:
    ```

    This should list the contents of your remote storage.

## Configuration

The `piphoto-rclone-sync` script reads from `/etc/piphoto.rclone.conf`. An example config is provided in `piphoto.rclone.conf.example`.

The variables that need to be set are:

- **`rclone_executable`** - If `rclone` is not on the user's PATH, this needs to be the full path to the `rclone` binary.

- **`rclone_remote`** - The name of the remote backend configured in `rclone`.

- **`dest_path`** - The path in the remote storage to store the photos.

- **`rclone_options`** - Additional options to pass to `rclone` (e.g., `--transfers=4`, `--progress`).

## Testing photo sync with rclone

Once `piphoto-rclone-sync` is configured, it should be tested by running the following:

``` shell
piphoto-rclone-sync /path/to/images
```

to ensure it's working properly.

## Setting up PiPhoto

Finally, setup your PiPhoto to use `piphoto-rclone-sync` to copy the images to the remote storage. In your `piphoto.conf` file:

``` shell
sync_command="piphoto-rclone-sync"
```

## Caveats

This should organize images in the remote folder by capture date gathered from the images' EXIF metadata, similar to the [Copying and Organizing over SSH](../ssh-copy-and-organize/README.md) setup.
