#!/bin/bash
# Example hook script for a Waveshare 2.13" Touch E-Paper HAT.
#
# Source this file via the -H flag:
#   piphoto-rclone-sync -r myremote -p photos -H hooks-epaper-waveshare213.sh /media/card
#
# The display is driven by the Python helper below (epaper_display.py).
# Install dependencies on the Pi:
#   pip3 install waveshare-epaper pillow RPi.GPIO spidev
#
# Hook contract (arguments passed by piphoto-rclone-sync):
#   hook_start      mount_point dest_path
#   hook_file_begin filepath
#   hook_file_done  filepath remote_dest
#   hook_file_error filepath exit_code
#   hook_complete   files_synced files_failed

EPAPER_SCRIPT="$(dirname "${BASH_SOURCE[0]}")/epaper_display.py"

_epaper() {
    if command -v python3 &>/dev/null && [ -f "${EPAPER_SCRIPT}" ]; then
        python3 "${EPAPER_SCRIPT}" "$@" 2>/dev/null || true
    fi
}

hook_start() {
    local mount_point="$1" dest_path="$2"
    _epaper status "Syncing photos" "$(basename "${mount_point}") -> ${dest_path}"
}

hook_file_begin() {
    local filepath="$1"
    _epaper status "Uploading..." "$(basename "${filepath}")"
}

hook_file_done() {
    local filepath="$1" remote_dest="$2"
    _epaper status "Uploaded" "$(basename "${filepath}")"
}

hook_file_error() {
    local filepath="$1" exit_code="$2"
    _epaper error "Upload failed (${exit_code})" "$(basename "${filepath}")"
}

hook_complete() {
    local files_synced="$1" files_failed="$2"
    if [ "${files_failed}" -eq 0 ]; then
        _epaper done "Sync complete" "${files_synced} files uploaded"
    else
        _epaper error "Sync done w/ errors" "${files_synced} ok, ${files_failed} failed"
    fi
}
