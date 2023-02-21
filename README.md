# Flux Operator Validator

Sanity check your container to see that it has basic requirements for the flux operator.

## Usage

### Environment

```bash
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

We basically require Python with Jinja2.

### Check

And run the check. 

#### Example without PreCommand

Here is an example with one of our containers that doesn't require load
of any special environment:

```bash
$ python ./scripts/check.py ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
```
```console
    container: ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
   preCommand: None
         time: False
⚙️ Pulling ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
flux-sched-focal-v0.24.0: Pulling from rse-ops/lammps
Digest: sha256:fadec2d6bdacd5c10ab010ee3cf24f0a64065337eb801004fde70dd5c2dd931d
Status: Image is up to date for ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
Container: ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
🟢️ Found active user root
🟢️ sudo is installed
🟢️ flux is installed
```

#### Example with PreCommand

A dummy example with pre-command:

```bash
$ python ./scripts/check.py ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0 --pre-command ./example/dummy.txt
```
```console
    container: ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
   preCommand: ./example/dummy.txt
         time: False
⚙️ Pulling ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
flux-sched-focal-v0.24.0: Pulling from rse-ops/lammps
Digest: sha256:fadec2d6bdacd5c10ab010ee3cf24f0a64065337eb801004fde70dd5c2dd931d
Status: Image is up to date for ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
The present working directory...
/home/flux/examples/reaxff/HNS
Preparing environment...
Container: ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
🟢️ Found active user root
🟢️ sudo is installed
🟢️ flux is installed
```

And an example of a container that requires a pre command block to load a spack environment (⚠️ warning, large container! ⚠️):

```bash
$ python ./scripts/check.py ghcr.io/rse-ops/spack-ubuntu-libfabric-ssh:ubuntu-20.04 --pre-command ./example/preCommand.txt
```

#### Example with Multi-User

A container that will allow multi-user mode needs openssl. This should ship with Flux.

```bash
$ python ./scripts/check.py ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0 --multi-user
```
```console
...
ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
Container: ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
🟢️ Found active user root
🟢️ sudo is installed
🟢️ flux is installed
🟢️ openssl is installed
```

#### Example with Time

When you set logging->timed to true, we require the time command, and we can check for that too. Here is an example without
time - the check will fail:

```bash
$ python ./scripts/check.py ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0 --time
```
```console
...
ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
Container: ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
🟢️ Found active user root
🟢️ sudo is installed
🟢️ flux is installed
🔴️ time not found
```

Now if we add the install into a pre-command (which we could also do for the Flux Operator) it will pass.

```bash
$ python ./scripts/check.py ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0 --time --pre-command ./example/install-time.txt
```
```console
    container: ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
   preCommand: ./example/install-time.txt
         time: True
⚙️ Pulling ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
flux-sched-focal-v0.24.0: Pulling from rse-ops/lammps
<pull and pre-command install of time here>
Container: ghcr.io/rse-ops/lammps:flux-sched-focal-v0.24.0
🟢️ Found active user root
🟢️ sudo is installed
🟢️ flux is installed
🟢️ time is installed
```


❔️ Would you like to see this as a GitHub action? [Let us know](https://github.com/converged-computing/flux-operator-validator/issues)!
