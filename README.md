# dragonBrowser

A custom browser based on the tutorial of "https://browser.engineering"

## installation

1. clone this repo
2. go in the dragonBrowser
3. run python3 browser.py

## Examples
### 0 argument
`python3 browser.py`
`
This is a Directory(/) with this contents:
Directory: boot
Directory: dev
Directory: home
Directory: proc
Directory: run
Directory: sys
Directory: tmp
Directory: root
Directory: bin
Directory: lib
Directory: lib64
Directory: sbin
Directory: afs
Directory: etc
Directory: lost+found
Directory: media
Directory: mnt
Directory: opt
Directory: srv
Directory: usr
Directory: var
File: .hcwd
File: system-update
`
### 1 argument
`python3 browser.py file:///var`
`
This is a Directory(/var/) with this contents:
Directory: lock
Directory: mail
Directory: run
Directory: account
Directory: adm
Directory: cache
Directory: crash
Directory: db
Directory: empty
Directory: ftp
Directory: games
Directory: kerberos
Directory: lib
Directory: local
Directory: log
Directory: nis
Directory: opt
Directory: preserve
Directory: spool
Directory: tmp
Directory: yp
File: .updated
`
### 1 argument
`python3 browser.py file:///proc/version`
`Linux version 6.12.15-200.fc41.x86_64 (mockbuild@c444002bca6b4b5181a31926b883aace) (gcc (GCC) 14.2.1 20250110 (Red Hat 14.2.1-7), GNU ld version 2.43.1-5.fc41) #1 SMP PREEMPT_DYNAMIC Tue Feb 18 15:24:05 UTC 2025`
### 1 argument
`python3 browser.py http://example.com`
### 1 argument
`python3 browser.py https://example.com`
## Troubleshooting
when run without any arguments:
  it show the content of your root direcory
when you run it with 1 argument 
  it is correct why to run the program
when run more than 1 argument 
  it show how to crrect use the command
other question contact me
## Changelog
can open url:
- http
- https
- files
- directories
## additional resources
https://browser.engineering
## License information
